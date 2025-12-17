import os
import json
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from mcp import ClientSession

from .agent_component import allowed_tools, sys_prompt

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
async def get_tools(session: ClientSession) -> list:
    """Fetch tool from open metadata"""
    
    tools = await session.list_tools()
        
    print(f"\n[ TOOLS AVAILABLE ] : {len(tools.tools)}")
    
    filtered_mcp_tools = [tool for tool in tools.tools if tool.name in allowed_tools]
    print(f"[ TOOLS FILTERED ] : {len(filtered_mcp_tools)}\n ")
    
    # แปลง tools ตาม openai format
    openai_tools = []
    for tool in filtered_mcp_tools:
        openai_tools.append({
            "type": "function", "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
        
    return openai_tools

def should_continue(state: AgentState) -> str:
    if not state["messages"][-1].tool_calls:
        return END
    else:
        return "continue"
    
async def build_agent_app(session: ClientSession):
    """Build agent application"""
    
    tools = await get_tools(session)
    
    model = AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    ).bind_tools(tools)
    
    system_prompt = SystemMessage(content=sys_prompt)
    
    async def call_model(state: AgentState):
        messages_with_system = [system_prompt] + state["messages"]
        response = await model.ainvoke(messages_with_system)
        # print(f"[AGENT RESPONSE]: {response.content}")
        return {"messages": [response]}
    
    async def call_mcp_tools(state: AgentState):
        last_message = state["messages"][-1]
        tool_calls = last_message.tool_calls
        tool_messages = []
        
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # print(f"\n[AGENT DEBUG] Calling tool: {tool_name}")
            # print(f"[AGENT DEBUG] With args: {tool_args}\n")
            
            if "tool_call_id" not in tool_args:
                    tool_args["tool_call_id"] = tool_call["id"]
            
            try:
                # 'session.call_tool' จะได้รับ args ที่มี 'tool_call_id' แล้ว
                result = await session.call_tool(tool_name, tool_args)
                
                # (โค้ดแปลงผลลัพธ์ JSON เหมือนเดิม)
                content_obj = result.content
                content_str = ""
                if isinstance(content_obj, list) and content_obj:
                    # print(f"[AGENT DEBUG] 'content_obj' is a list with {len(content_obj)} items.")
                    content_obj = content_obj[0] 
                if hasattr(content_obj, 'text'):
                    content_str = content_obj.text 
                elif hasattr(content_obj, 'data'):
                    content_str = json.dumps(content_obj.data)
                else:
                    content_str = str(content_obj)
                
                tool_messages.append(ToolMessage(
                    content=content_str, 
                    tool_call_id=tool_call["id"]
                ))
            
            except Exception as e:
                print(f"\n[MCP TOOL ERROR] Failed to call {tool_name}: {e}\n")
                tool_messages.append(ToolMessage(
                    content=f"Error excuting tool: {e}",
                    tool_call_id=tool_call["id"]
                ))
            
        return {"messages": tool_messages}
    
    # ----- Graph -----
    graph = StateGraph(AgentState)
    
    graph.add_node("agent", call_model)
    graph.add_node("tools", call_mcp_tools)
    
    graph.set_entry_point("agent")
    
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            END: END
        }
    )
    
    graph.add_edge("tools", "agent")
    
    return graph.compile()