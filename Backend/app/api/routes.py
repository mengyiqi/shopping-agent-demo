from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Annotated
from fastapi import Form
from PIL import Image
import io

from app.models import ChatRequest, ChatResponse, ThreadInfo, ThreadHistory
from app.services.chat_service import ChatService
from app.services.service_manager import get_chat_service
# Create router
router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Annotated[ChatRequest, Form()],
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    """
    Send a message to the chatbot and get a response.
    
    - **message**: The user's message content
    - **thread_id**: Optional thread ID for conversation continuity
    - **user_id**: Optional user identifier
    - **context**: Optional additional context
    """    

    try:
        return await chat_service.process_chat(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.get("/threads", response_model=List[ThreadInfo])
async def list_threads(
    user_id: Optional[str] = None,
    chat_service: ChatService = Depends(get_chat_service)
) -> List[ThreadInfo]:
    """
    List all conversation threads.
    
    - **user_id**: Optional filter by user ID
    """
    try:
        return await chat_service.list_threads(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list threads: {str(e)}")


@router.get("/threads/{thread_id}/history", response_model=ThreadHistory)
async def get_thread_history(
    thread_id: str,
    chat_service: ChatService = Depends(get_chat_service)
) -> ThreadHistory:
    """
    Get conversation history for a specific thread.
    
    - **thread_id**: The thread identifier
    """
    try:
        return await chat_service.get_thread_history(thread_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get thread history: {str(e)}")


@router.delete("/threads/{thread_id}")
async def delete_thread(
    thread_id: str,
    chat_service: ChatService = Depends(get_chat_service)
) -> dict:
    """
    Delete a conversation thread.
    
    - **thread_id**: The thread identifier to delete
    """
    try:
        success = await chat_service.delete_thread(thread_id)
        if success:
            return {"message": "Thread deleted successfully", "thread_id": thread_id}
        else:
            raise HTTPException(status_code=404, detail="Thread not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete thread: {str(e)}")


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "chatbot-api"} 