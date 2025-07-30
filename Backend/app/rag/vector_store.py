import uuid
import chromadb
import numpy as np
import torch
from typing import List, Dict, Any, Optional, Union
from chromadb.config import Settings
from transformers import CLIPProcessor, CLIPModel
from PIL import Image, ImageFile


from app.models import Product, ProductImage
from app.config import settings
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction


class ProductVectorStore:
    """ChromaDB-based vector store for product search and RAG"""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        model_id = "openai/clip-vit-large-patch14-336"
        # Initialize CLIP embeddings for multi-modal
        self.clip_model = CLIPModel.from_pretrained(model_id)
        self.clip_processor = CLIPProcessor.from_pretrained(model_id)
        
        # Create or get collections
        self.product_collection_name = "products_multimodal"
        
        self.product_collection = self.client.get_or_create_collection(
            name=self.product_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def get_text_embedding(self, text):
        inputs = self.clip_processor(text=[text], return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            emb = self.clip_model.get_text_features(**inputs)
        return emb[0].cpu().numpy()

    def get_image_embedding(self, image_path:Optional[str] = '', image: Optional[ImageFile.ImageFile] = None):
        if(image is None):
            image = Image.open(image_path).convert("RGB")
        
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            emb = self.clip_model.get_image_features(**inputs)
        return emb[0].cpu().numpy()
    
    def add_product(self, product: Product) -> str:
        """Add a product to the vector store with multi-modal support"""
        # Generate product ID if not provided
        if not product.id:
            product.id = str(uuid.uuid4())

        ids=[product.id]
        documents= []
        embeddings= []
        metadatas= []
        
        # Create document embeddings for text search
        content = f"Title: {product.title}\nDescription: {product.description}"
        if product.category:
            content += f"\nCategory: {product.category}"
        if product.tags:
            content += f"\nTags: {', '.join(product.tags)}"
        content += f"\nPrice: ${product.price}"

        documents.append(content)
        embeddings.append(self.get_text_embedding(content).tolist())

        # Create metadata
        metadata = {
            "product_id": product.id,
            "title": product.title,
            "description": product.description,
            "price": str(product.price),
            "category": product.category or "",
            "images": ",".join([image.file_path for image in product.images]) if product.images else "",
            "tags": ",".join(product.tags) if product.tags else "",
            "created_at": product.created_at.isoformat() if product.created_at else "",
            "updated_at": product.updated_at.isoformat() if product.updated_at else ""
        }

        metadatas.append(metadata)

        #  Create image embeddings for image search
        for image in product.images:
            image_embedding = self.get_image_embedding(image.file_path)
            ids.append(f"{product.id}_{image.id}")
            documents.append(f"Image for product: {product.id} and path: {image.file_path}")
            embeddings.append(image_embedding.tolist())
            metadatas.append(metadata)
        
        # Add text content to text collection
        self.product_collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Added product {product.id} to vector store")
        
        return product.id
    
    def update_product(self, product: Product) -> bool:
        """Update a product in the vector store"""
        if not product.id:
            return False
        
        # Delete existing product
        self.delete_product(product.id)
        
        # Add updated product
        self.add_product(product)
        return True
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product from the vector store"""
        success = True
        
        try:            # Delete from product collection
            self.product_collection.delete(ids=[product_id])

            return success
        except Exception as e:
            print(f"Error deleting product {product_id}: {e}")
            return False
    
    def search_products(
        self, 
        query: Optional[str] = None,
        image_query_path: Optional[str] = None,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        min_price: Optional[float] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search products using semantic similarity with multi-modal support"""

        embeddings= []

        if(query):
            embeddings.append(self.get_text_embedding(query).tolist())
        
        if(image_query_path):
            embeddings.append(self.get_image_embedding(image_query_path).tolist())
        
        if not embeddings:
            return [];


        results = self.product_collection.query(
            query_embeddings=embeddings,
            n_results=limit * 2
        )

        product_metadatas = []
        # if(len(results['distances']) > 0):
        #     for query_dist, query_meta in zip(results['distances'], results['metadatas'][0]):
        #         if(np.mean(query_dist) < settings.AGENT_SIMILARITY_DISTANCE):
        #             product_metadatas.append(query_meta)

        for query_dist, query_meta in zip(results['distances'], results['metadatas']):
            for dist, meta in zip(query_dist, query_meta):
                if dist < settings.AGENT_SIMILARITY_DISTANCE:
                    product_metadatas.append(meta)


        products = []

        for metadata in product_metadatas:                            
                # Convert price back to float for filtering
                try:
                    price = float(metadata.get("price", "0"))
                except ValueError:
                    price = 0.0
                
                # Apply price filters
                if max_price is not None and price > max_price:
                    continue
                if min_price is not None and price < min_price:
                    continue
                
                # Convert back to Product-like structure
                product_data = {
                    "id": metadata.get("product_id"),
                    "title": metadata.get("title"),
                    "description": metadata.get("description"),
                    "price": price,
                    "category": metadata.get("category"),
                    "tags": metadata.get("tags", "").split(",") if metadata.get("tags") else [],
                    "created_at": metadata.get("created_at"),
                    "updated_at": metadata.get("updated_at")
                }
                
                products.append(product_data)
        
        return products[:limit]
        
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific product by ID"""
        try:
            results = self.product_collection.get(
                ids=[product_id]
            )
            
            if results['metadatas'] and results['metadatas'][0]:
                metadata = results['metadatas'][0]
                
                return {
                    "id": metadata.get("product_id"),
                    "title": metadata.get("title"),
                    "description": metadata.get("description"),
                    "price": float(metadata.get("price", "0")),
                    "category": metadata.get("category"),
                    "tags": metadata.get("tags", "").split(",") if metadata.get("tags") else [],
                    "images": metadata.get("images", "").split(",") if metadata.get("images") else [],
                    "created_at": metadata.get("created_at"),
                    "updated_at": metadata.get("updated_at")
                }
            return None
        except Exception as e:
            print(f"Error getting product by id: {e}")
            return None
    
    def get_all_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all products from the vector store"""
        try:
            results = self.product_collection.get(
                limit=limit,
                include=["metadatas"]
            )
            
            products = []
            for metadata in results['metadatas']:
                product_data = {
                    "id": metadata.get("product_id"),
                    "title": metadata.get("title"),
                    "description": metadata.get("description"),
                    "price": float(metadata.get("price", "0")),
                    "category": metadata.get("category"),
                    "tags": metadata.get("tags", "").split(",") if metadata.get("tags") else [],
                    "images": metadata.get("images", "").split(",") if metadata.get("images") else [],
                    "created_at": metadata.get("created_at"),
                    "updated_at": metadata.get("updated_at")
                }
                products.append(product_data)
            
            return products
        except Exception:
            return []
    

    def reset_vector_store(self) -> bool:
        """Reset the entire vector store by deleting all collections"""
        try:
            # Delete text collection
            self.client.delete_collection(name=self.product_collection_name)

            self.product_collection = self.client.get_or_create_collection(
                name=self.product_collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            print(f"Successfully reset vector store: {self.product_collection_name}")
            return True
            
        except Exception as e:
            print(f"Error resetting vector store: {e}")
            return False
    
    def get_vector_store_stats(self) -> dict:
        """Get statistics about the vector store"""
        try:
            # Get product collection stats
            product_count = self.product_collection.count()
            
            return {
                "product_collection_name": self.product_collection_name,
                "product_documents_count": product_count,            
                "status": "active"
            }
        except Exception as e:
            print(f"Error getting vector store stats: {e}")
            return {                
                "error": str(e)
            } 