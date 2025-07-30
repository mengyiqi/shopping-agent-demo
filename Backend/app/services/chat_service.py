import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.agent.chatbot_agent import ChatbotAgent
from app.models import ChatRequest, ChatResponse, ThreadInfo, ThreadHistory, ChatMessage
from fastapi import UploadFile
from app.services.file_service import FileService

class ChatService:
    """Service layer for chat operations"""
    
    def __init__(self):
        self.agent = ChatbotAgent()
        self._threads: Dict[str, ThreadInfo] = {}
        self.file_service = FileService()
    
    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat request and return response"""
        
        # Generate message ID
        message_id = str(uuid.uuid4())

        saved_images = await self.file_service.save_multiple_images([request.query_image]) if request.query_image else None
        
        # Process with agent
        result = await self.agent.chat(
            message=request.message,
            query_image_path=saved_images[0].file_path if saved_images else None,
            thread_id=request.thread_id,
            user_id=request.user_id,
            context=request.context
        )
        
        # Update thread info
        thread_id = result["thread_id"]
        await self._update_thread_info(thread_id, request.user_id)
        
        return ChatResponse(
            response=result["response"],
            thread_id=thread_id,
            message_id=message_id,
            timestamp=datetime.now(),
            metadata=result.get("metadata", {})
        )
    
    async def get_thread_history(self, thread_id: str) -> ThreadHistory:
        """Get conversation history for a thread"""
        
        # Get messages from agent
        messages_data = await self.agent.get_thread_history(thread_id)
        
        # Convert to ChatMessage objects
        messages = [
            ChatMessage(
                role=msg["role"],
                content=msg["content"],
                timestamp=datetime.fromisoformat(msg["timestamp"])
            )
            for msg in messages_data
        ]
        
        # Get thread info
        thread_info = self._threads.get(thread_id)
        metadata = {
            "user_id": thread_info.user_id if thread_info else None,
            "message_count": len(messages)
        }
        
        return ThreadHistory(
            thread_id=thread_id,
            messages=messages,
            metadata=metadata
        )
    
    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a conversation thread"""
        
        # Delete from agent memory
        success = await self.agent.delete_thread(thread_id)
        
        # Remove from local thread tracking
        if thread_id in self._threads:
            del self._threads[thread_id]
        
        return success
    
    async def list_threads(self, user_id: Optional[str] = None) -> List[ThreadInfo]:
        """List all threads, optionally filtered by user"""
        
        threads = list(self._threads.values())
        
        if user_id:
            threads = [t for t in threads if t.user_id == user_id]
        
        # Sort by last updated
        threads.sort(key=lambda x: x.last_updated, reverse=True)
        
        return threads
    
    async def _update_thread_info(self, thread_id: str, user_id: Optional[str] = None) -> None:
        """Update thread information"""
        
        if thread_id not in self._threads:
            # Create new thread
            self._threads[thread_id] = ThreadInfo(
                thread_id=thread_id,
                user_id=user_id,
                created_at=datetime.now(),
                last_updated=datetime.now(),
                message_count=1
            )
        else:
            # Update existing thread
            thread = self._threads[thread_id]
            thread.last_updated = datetime.now()
            thread.message_count += 1
            if user_id and not thread.user_id:
                thread.user_id = user_id 