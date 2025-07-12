import json
import logging
from typing import AsyncGenerator
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from artemis.api.models import ChatRequest, ChatResponse
from artemis.chatbot.chatbot import ArtemisChatbot

logger = logging.getLogger(__name__)
router = APIRouter()

# Lazy initialization of chatbot
_chatbot = None

def get_chatbot():
    global _chatbot
    if _chatbot is None:
        _chatbot = ArtemisChatbot()
    return _chatbot


def get_timestamp() -> str:
    """Get current ISO timestamp."""
    return datetime.now(timezone.utc).isoformat()


async def stream_response(request: ChatRequest) -> AsyncGenerator[str, None]:
    """Stream chat response as Server-Sent Events."""
    try:
        # Convert messages to format expected by chatbot
        messages = [(msg.role, msg.content) for msg in request.messages]
        
        # Get chatbot and stream the response
        chatbot = get_chatbot()
        async for chunk in chatbot.astream(messages):
            # Format as SSE
            data = json.dumps({
                "type": "token",
                "content": chunk,
                "timestamp": get_timestamp()
            })
            yield f"data: {data}\n\n"
            
        # Send completion signal
        yield f"data: {json.dumps({'type': 'done', 'timestamp': get_timestamp()})}\n\n"
        
    except Exception as e:
        logger.error(f"Error in stream_response: {str(e)}")
        error_data = json.dumps({
            "type": "error",
            "content": str(e),
            "timestamp": get_timestamp()
        })
        yield f"data: {error_data}\n\n"


@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint that supports both streaming and non-streaming responses."""
    if request.stream:
        return StreamingResponse(
            stream_response(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
                "Transfer-Encoding": "chunked",  # Enable chunked transfer
            },
        )
    else:
        # Non-streaming response
        try:
            messages = [(msg.role, msg.content) for msg in request.messages]
            chatbot = get_chatbot()
            response = await chatbot.ainvoke(messages)
            return ChatResponse(response=response)
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))