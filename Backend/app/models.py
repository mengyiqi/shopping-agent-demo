from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from fastapi import UploadFile, File
from PIL import Image, ImageFile


class ChatMessage(BaseModel):
    """Individual chat message model"""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: Optional[str] = Field(None, description="User message content")
    thread_id: Optional[str] = Field(None, description="Thread ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="User identifier")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    query_image: Optional[UploadFile] = File(None, description="Product search image")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Assistant response")
    thread_id: str = Field(..., description="Thread ID for conversation continuity")
    message_id: str = Field(..., description="Unique message identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ThreadInfo(BaseModel):
    """Thread information model"""
    thread_id: str = Field(..., description="Thread identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    message_count: int = Field(default=0, description="Number of messages in thread")


class ThreadHistory(BaseModel):
    """Thread history model"""
    thread_id: str = Field(..., description="Thread identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="List of messages in thread")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Thread metadata")


class ProductImage(BaseModel):
    """Product image model"""
    id: str = Field(..., description="Image identifier")
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="Local file path")
    file_url: str = Field(..., description="Public URL for the image")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of the image")
    created_at: datetime = Field(default_factory=datetime.now)


class Product(BaseModel):
    """Product model for RAG system"""
    id: Optional[str] = Field(None, description="Product identifier")
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    images: Optional[List[ProductImage]] = Field(default_factory=list, description="List of product images")
    category: Optional[str] = Field(None, description="Product category")
    tags: Optional[List[str]] = Field(default_factory=list, description="Product tags")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class ProductCreate(BaseModel):
    """Request model for creating a product"""
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    category: Optional[str] = Field(None, description="Product category")
    images: Optional[List[UploadFile]] = File(None, description="Product images"),
    tags: Optional[List[str]] = Field(default_factory=list, description="Product tags")


class ProductUpdate(BaseModel):
    """Request model for updating a product"""
    title: Optional[str] = Field(None, description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[float] = Field(None, description="Product price")
    category: Optional[str] = Field(None, description="Product category")
    tags: Optional[List[str]] = Field(None, description="Product tags")


class ProductResponse(BaseModel):
    """Response model for product operations"""
    id: str = Field(..., description="Product identifier")
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    images: List[str] = Field(default_factory=list, description="List of product images")
    category: Optional[str] = Field(None, description="Product category")
    tags: List[str] = Field(default_factory=list, description="Product tags")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ProductSearchRequest(BaseModel):
    """Request model for product search"""
    query: Optional[str] = Field(None, description="Text search query")
    image_query_path: Optional[str] = Field(None, description="Query image path")
    category: Optional[str] = Field(None, description="Filter by category")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    limit: Optional[int] = Field(10, description="Maximum number of results")


class ProductSearchResponse(BaseModel):
    """Response model for product search"""
    products: List[ProductResponse] = Field(..., description="List of matching products")
    total_count: int = Field(..., description="Total number of matching products")
    query: Optional[str] = Field(None, description="Original search query")


class ImageSearchRequest(BaseModel):
    """Request model for image-based search"""
    image: str = Field(..., description="Base64 encoded image")
    category: Optional[str] = Field(None, description="Filter by category")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    limit: Optional[int] = Field(10, description="Maximum number of results")


class MultiModalSearchRequest(BaseModel):
    """Request model for multi-modal search"""
    text_query: Optional[str] = Field(None, description="Text search query")
    image_query: Optional[str] = Field(None, description="Base64 encoded image for visual search")
    category: Optional[str] = Field(None, description="Filter by category")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    limit: Optional[int] = Field(10, description="Maximum number of results")
    weight_text: float = Field(0.5, description="Weight for text similarity (0-1)")
    weight_image: float = Field(0.5, description="Weight for image similarity (0-1)") 