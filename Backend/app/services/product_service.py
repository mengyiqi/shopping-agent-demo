import uuid
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from fastapi import UploadFile

from app.rag.vector_store import ProductVectorStore
from app.services.file_service import FileService
from app.models import Product, ProductCreate, ProductUpdate, ProductResponse, ProductSearchRequest, ProductSearchResponse, ProductImage


class ProductService:
    """Service layer for product operations"""
    
    def __init__(self):
        self.vector_store = ProductVectorStore()
        self.file_service = FileService()
    
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product with optional image uploads"""
        
        # Save uploaded images if provided
        product_images = []
        if product_data.images:
            product_images = await self.file_service.save_multiple_images(product_data.images)
        
        # Create Product object
        product = Product(
            id=str(uuid.uuid4()),
            title=product_data.title,
            description=product_data.description,
            price=product_data.price,
            images=product_images,
            category=product_data.category,
            tags=product_data.tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Add to vector store
        product_id = self.vector_store.add_product(product)
        
        # Get the created product
        created_product = self.vector_store.get_product_by_id(product_id)
        
        if not created_product:
            raise ValueError("Failed to create product")
        
        return ProductResponse(**created_product)
    
    async def get_product(self, product_id: str) -> Optional[ProductResponse]:
        """Get a product by ID"""
        
        product_data = self.vector_store.get_product_by_id(product_id)
        
        if not product_data:
            return None
        
        return ProductResponse(**product_data)
    
    async def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[ProductResponse]:
        """Update an existing product"""
        
        # Get existing product
        existing_product = self.vector_store.get_product_by_id(product_id)
        
        if not existing_product:
            return None
        
        # Create updated product
        updated_product = Product(
            id=product_id,
            title=product_data.title or existing_product["title"],
            description=product_data.description or existing_product["description"],
            price=product_data.price or existing_product["price"],
            images=product_data.images or existing_product["images"],
            category=product_data.category or existing_product["category"],
            tags=product_data.tags or existing_product["tags"],
            created_at=datetime.fromisoformat(existing_product["created_at"]),
            updated_at=datetime.now()
        )
        
        # Update in vector store
        success = self.vector_store.update_product(updated_product)
        
        if not success:
            raise ValueError("Failed to update product")
        
        # Get the updated product
        updated_product_data = self.vector_store.get_product_by_id(product_id)
        
        if not updated_product_data:
            raise ValueError("Failed to retrieve updated product")
        
        return ProductResponse(**updated_product_data)
    
    async def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        
        return self.vector_store.delete_product(product_id)
    
    async def search_products(self, search_request: Dict[str, Any]) -> ProductSearchResponse:
        """Search products using semantic similarity with multi-modal support"""
        
        # Perform search
        products_data = self.vector_store.search_products(
            query=search_request.query,
            image_query_path=search_request.image_query_path,
            category=search_request.category,
            max_price=search_request.max_price,
            min_price=search_request.min_price,
            limit=search_request.limit
        )
        
        print(f"Found #{len(products_data)} product")

        # Convert to ProductResponse objects
        products = [ProductResponse(**product_data) for product_data in products_data]
        
        return ProductSearchResponse(
            products=products,
            total_count=len(products),
            query=search_request.query
        )
    
    async def get_all_products(self, limit: int = 100) -> List[ProductResponse]:
        """Get all products"""
        
        products_data = self.vector_store.get_all_products(limit=limit)
        
        return [ProductResponse(**product_data) for product_data in products_data]
    
    async def get_products_by_category(self, category: str, limit: int = 50) -> List[ProductResponse]:
        """Get products by category"""
        
        products_data = self.vector_store.search_products(
            query=category,
            category=category,
            limit=limit
        )
        
        return [ProductResponse(**product_data) for product_data in products_data]
    
    async def get_relevant_context(self, query: str, limit: int = 3) -> str:
        """Get relevant product context for RAG"""
        
        return self.vector_store.get_relevant_context(query, limit)
    
    async def reset_vector_store(self) -> bool:
        """Reset the entire vector store"""
        
        return self.vector_store.reset_vector_store()
    
    async def get_vector_store_stats(self) -> dict:
        """Get vector store statistics"""
        
        return self.vector_store.get_vector_store_stats() 