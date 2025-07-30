from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from typing import List, Optional, Annotated
from datetime import datetime
from app.services.service_manager import get_product_service

from app.models import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductSearchRequest, ProductSearchResponse, ImageSearchRequest, MultiModalSearchRequest
)
from app.services.product_service import ProductService

# Create router
router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: Annotated[ProductCreate, Form()],
    product_service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """
    Create a new product with optional image uploads.
    
    - **title**: Product title (required)
    - **description**: Product description (required)
    - **price**: Product price (required)
    - **category**: Product category (optional)
    - **tags**: List of product tags (optional)
    - **images**: Uploaded image files (optional)
    """
    try:
        return await product_service.create_product(product_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """
    Get a product by ID.
    
    - **product_id**: The product identifier
    """
    try:
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get product: {str(e)}")


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """
    Update an existing product.
    
    - **product_id**: The product identifier
    - **product_data**: Updated product information
    """
    try:
        product = await product_service.update_product(product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service)
) -> dict:
    """
    Delete a product.
    
    - **product_id**: The product identifier to delete
    """
    try:
        success = await product_service.delete_product(product_id)
        if success:
            return {"message": "Product deleted successfully", "product_id": product_id}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")


@router.post("/search", response_model=ProductSearchResponse)
async def search_products(
    search_request: ProductSearchRequest,
    product_service: ProductService = Depends(get_product_service)
) -> ProductSearchResponse:
    """
    Search products using semantic similarity.
    
    - **query**: Search query (required)
    - **category**: Filter by category (optional)
    - **max_price**: Maximum price filter (optional)
    - **min_price**: Minimum price filter (optional)
    - **limit**: Maximum number of results (optional, default: 10)
    """
    try:
        return await product_service.search_products(search_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of products to return"),
    product_service: ProductService = Depends(get_product_service)
) -> List[ProductResponse]:
    """
    Get all products.
    
    - **limit**: Maximum number of products to return (default: 100, max: 1000)
    """
    try:
        return await product_service.get_all_products(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get products: {str(e)}")


@router.get("/category/{category}", response_model=List[ProductResponse])
async def get_products_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=500, description="Maximum number of products to return"),
    product_service: ProductService = Depends(get_product_service)
) -> List[ProductResponse]:
    """
    Get products by category.
    
    - **category**: Product category
    - **limit**: Maximum number of products to return (default: 50, max: 500)
    """
    try:
        return await product_service.get_products_by_category(category, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get products by category: {str(e)}")


@router.get("/search/simple")
async def simple_search(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    product_service: ProductService = Depends(get_product_service)
) -> ProductSearchResponse:
    """
    Simple search endpoint using query parameters.
    
    - **q**: Search query (required)
    - **category**: Filter by category (optional)
    - **max_price**: Maximum price filter (optional)
    - **min_price**: Minimum price filter (optional)
    - **limit**: Maximum number of results (optional, default: 10)
    """
    try:
        search_request = ProductSearchRequest(
            query=q,
            category=category,
            max_price=max_price,
            min_price=min_price,
            limit=limit
        )
        return await product_service.search_products(search_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/search/image", response_model=ProductSearchResponse)
async def image_search(
    search_request: ImageSearchRequest,
    product_service: ProductService = Depends(get_product_service)
) -> ProductSearchResponse:
    """
    Search products using image similarity.
    
    - **image**: Base64 encoded image (required)
    - **category**: Filter by category (optional)
    - **max_price**: Maximum price filter (optional)
    - **min_price**: Minimum price filter (optional)
    - **limit**: Maximum number of results (optional, default: 10)
    """
    try:
        product_search_request = ProductSearchRequest(
            image_query=search_request.image,
            category=search_request.category,
            max_price=search_request.max_price,
            min_price=search_request.min_price,
            limit=search_request.limit
        )
        return await product_service.search_products(product_search_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image search failed: {str(e)}")


@router.post("/search/multimodal", response_model=ProductSearchResponse)
async def multimodal_search(
    search_request: MultiModalSearchRequest,
    product_service: ProductService = Depends(get_product_service)
) -> ProductSearchResponse:
    """
    Multi-modal search combining text and image queries.
    
    - **text_query**: Text search query (optional)
    - **image_query**: Base64 encoded image for visual search (optional)
    - **category**: Filter by category (optional)
    - **max_price**: Maximum price filter (optional)
    - **min_price**: Minimum price filter (optional)
    - **limit**: Maximum number of results (optional, default: 10)
    - **weight_text**: Weight for text similarity (0-1, default: 0.5)
    - **weight_image**: Weight for image similarity (0-1, default: 0.5)
    """
    try:

        
        product_search_request = ProductSearchRequest(
            query=search_request.text_query,
            image_query=search_request.image_query,
            category=search_request.category,
            max_price=search_request.max_price,
            min_price=search_request.min_price,
            limit=search_request.limit
        )
        return await product_service.search_products(product_search_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-modal search failed: {str(e)}")


@router.post("/reset", tags=["admin"])
async def reset_vector_store(
    product_service: ProductService = Depends(get_product_service)
) -> dict:
    """
    Reset the entire product vector store.
    
    ⚠️ **WARNING**: This will delete ALL products and their embeddings from the vector store.
    This action cannot be undone.
    
    Use this endpoint to clear all data and start fresh.
    """
    try:
        success = await product_service.reset_vector_store()
        
        if success:
            return {
                "message": "Vector store reset successfully",
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "warning": "All products and embeddings have been deleted"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to reset vector store")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@router.get("/stats", tags=["admin"])
async def get_vector_store_stats(
    product_service: ProductService = Depends(get_product_service)
) -> dict:
    """
    Get statistics about the vector store.
    
    Returns information about:
    - Number of text documents
    - Number of image documents
    - Total documents
    - Collection names
    - Status
    """
    try:
        stats = await product_service.get_vector_store_stats()
        return {
            "vector_store_stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}") 