from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    stream: bool = True
    
    
class ChatResponse(BaseModel):
    response: str
    
    
class StreamChunk(BaseModel):
    type: str  # "token", "tool_use", "error"
    content: str
    metadata: Optional[Dict[str, Any]] = None