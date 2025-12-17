from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    type: str
    content: str
    
class ChatRequest(BaseModel):
    prompt: str
    # history: List[ChatMessage]
    sessionid: str
    
class ChatResponse(BaseModel):
    history: List[ChatMessage]
    
class GetHistory(BaseModel):
    sessionid: str