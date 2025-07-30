from typing import Optional
from app.services.chat_service import ChatService
from app.services.product_service import ProductService
from app.services.file_service import FileService


class ServiceManager:
    """Manager for service instances"""
    
    def __init__(self):
        self._chat_service: Optional[ChatService] = None
        self._product_service: Optional[ProductService] = None
        self._file_service: Optional[FileService] = None
    
    def get_chat_service(self) -> ChatService:
        """Get or create chat service instance"""
        if self._chat_service is None:
            self._chat_service = ChatService()
        return self._chat_service
    
    def get_product_service(self) -> ProductService:
        """Get or create product service instance"""
        if self._product_service is None:
            self._product_service = ProductService()
        return self._product_service
    
    def get_file_service(self) -> FileService:
        """Get or create file service instance"""
        if self._file_service is None:
            self._file_service = FileService()
        return self._file_service


# Global service manager instance
_service_manager = ServiceManager()


def get_chat_service() -> ChatService:
    """Get chat service instance"""
    return _service_manager.get_chat_service()


def get_product_service() -> ProductService:
    """Get product service instance"""
    return _service_manager.get_product_service()


def get_file_service() -> FileService:
    """Get file service instance"""
    return _service_manager.get_file_service()