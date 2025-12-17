from fastapi import APIRouter, HTTPException
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import List, Sequence

from .conversation_DB.history_conversation_DB import HistoryConversationDB
from .schemas import ChatMessage, ChatRequest, ChatResponse, GetHistory
from .state import STATE

router = APIRouter()

async def get_conversations(session_id: str) -> List[ChatMessage]:
    """get conversation history from database"""
    try:
        with HistoryConversationDB() as db:
            result = db.fetch_conversations(session_id)
            if result and "history" in result:
                history_data = result["history"]
                history_messages = []
                for item in history_data:
                    history_messages.append(ChatMessage(type=item["type"], content=item["content"]))
                return history_messages
            else:
                return None
    except Exception as e:
        print(f"Error fetching conversations: {e}")
        return None
    
async def save_conversation(session_id: str, conversation: List[ChatMessage]) -> bool:
    """save conversation to database"""
    try:
        with HistoryConversationDB() as db:
            question = conversation[0].content
            answer = conversation[1].content
            save_status = db.create_conversation(session_id=session_id, 
                                   question=question, 
                                   answer=answer)
            return save_status
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False
    
# Helper Function
def parse_history_to_messages(history: List[ChatMessage]) -> List[BaseMessage]:
    """แปลง JSON history เป็น Langchain Messages"""
    messages = []
    for msg in history:
        if msg.type == "human" and msg.content:
            messages.append(HumanMessage(content=msg.content))
        elif msg.type == "ai" and msg.content:
            messages.append(AIMessage(content=msg.content))
    return messages

def serialize_messages_to_history(messages: Sequence[BaseMessage]) -> List[ChatMessage]:
    """แปลง Langchain Messages กลับเป็น JSON history"""
    history = []
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage)) and msg.content:
            history.append(ChatMessage(type=msg.type, content=msg.content))
    return history

# API Endpoint
@router.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint"""
    
    # ดึง graph ที่ compile แล้วจาก STATE
    langgraph_app = STATE.get("app")
    if not langgraph_app:
        raise HTTPException(status_code=503, detail="Service not ready, please wait.")
    
    try:
        # get conversation history based on sessionid frontend
        conversation_history = await get_conversations(request.sessionid)
            
        # convert langchain messages 
        conversation_messages = parse_history_to_messages(conversation_history)
        
        conversation_messages.append(HumanMessage(content=request.prompt))
        inputs = {"messages": conversation_messages}
        final_state = await langgraph_app.ainvoke(inputs)
        
        # convert langchain messages to JSON
        final_history_serializable = serialize_messages_to_history(final_state["messages"])
        chat_response = ChatResponse(history=final_history_serializable)
        
        # save conversation to database (current prompt + answer)
        if not await save_conversation(request.sessionid, chat_response.history[-2:]):
            raise HTTPException(status_code=500, detail="Failed to save conversation")
        
        return chat_response
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/api/v1/health")
async def health():
    return {"status": "ok"}

@router.post("/api/v1/get_history_conversations")
async def get_history_conversations(request: GetHistory):
    """Get conversation history from database based on sessionid"""
    conversations = await get_conversations(request.sessionid)
    return ChatResponse(history=conversations)