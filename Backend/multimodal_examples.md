# Multi-Modal Product Search Examples

This document provides examples for the enhanced chatbot with multi-modal capabilities including image uploads, CLIP embeddings, and visual search.

## Base URL
```
http://localhost:8888
```

## 🖼️ Product Creation with Image Uploads

### 1. Create Product with Images

**Endpoint:** `POST /api/v1/products/`

```bash
curl -X POST "http://localhost:8888/api/v1/products/" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Wireless Bluetooth Headphones" \
  -F "description=High-quality wireless headphones with noise cancellation, 30-hour battery life, and premium sound quality." \
  -F "price=129.99" \
  -F "category=Electronics" \
  -F "tags=wireless,bluetooth,noise-cancellation,audio" \
  -F "images=@headphones1.jpg" \
  -F "images=@headphones2.jpg"
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Wireless Bluetooth Headphones",
  "description": "High-quality wireless headphones with noise cancellation, 30-hour battery life, and premium sound quality.",
  "price": 129.99,
  "category": "Electronics",
  "tags": ["wireless", "bluetooth", "noise-cancellation", "audio"],
  "images": [
    {
      "id": "img-123",
      "filename": "headphones1.jpg",
      "file_path": "./uploads/images/img-123.jpg",
      "file_url": "/uploads/images/img-123.jpg",
      "file_size": 245760,
      "mime_type": "image/jpeg",
      "created_at": "2024-01-15T10:30:00.123456"
    },
    {
      "id": "img-124",
      "filename": "headphones2.jpg",
      "file_path": "./uploads/images/img-124.jpg",
      "file_url": "/uploads/images/img-124.jpg",
      "file_size": 198432,
      "mime_type": "image/jpeg",
      "created_at": "2024-01-15T10:30:01.234567"
    }
  ],
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

### 2. Create Product without Images

```bash
curl -X POST "http://localhost:8888/api/v1/products/" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Smart Coffee Maker" \
  -F "description=Programmable coffee maker with smartphone control and built-in grinder." \
  -F "price=299.99" \
  -F "category=Home & Kitchen" \
  -F "tags=coffee,smart,programmable,grinder"
```

## 🔍 Multi-Modal Search

### 1. Text Search (Traditional)

**Endpoint:** `POST /api/v1/products/search`

```bash
curl -X POST "http://localhost:8888/api/v1/products/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "wireless audio devices",
    "category": "Electronics",
    "max_price": 200.00,
    "limit": 5,
    "search_type": "text"
  }'
```

### 2. Image Search

**Endpoint:** `POST /api/v1/products/search/image`

```bash
curl -X POST "http://localhost:8888/api/v1/products/search/image" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
    "category": "Electronics",
    "max_price": 500.00,
    "limit": 10
  }'
```

### 3. Multi-Modal Search (Text + Image)

**Endpoint:** `POST /api/v1/products/search/multimodal`

```bash
curl -X POST "http://localhost:8888/api/v1/products/search/multimodal" \
  -H "Content-Type: application/json" \
  -d '{
    "text_query": "wireless headphones",
    "image_query": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=",
    "category": "Electronics",
    "max_price": 300.00,
    "limit": 5,
    "weight_text": 0.6,
    "weight_image": 0.4
  }'
```

## 📱 JavaScript Examples

### 1. Upload Product with Images

```javascript
async function createProductWithImages(productData, imageFiles) {
  const formData = new FormData();
  
  // Add product data
  formData.append('title', productData.title);
  formData.append('description', productData.description);
  formData.append('price', productData.price);
  formData.append('category', productData.category);
  formData.append('tags', JSON.stringify(productData.tags));
  
  // Add images
  if (imageFiles) {
    for (let file of imageFiles) {
      formData.append('images', file);
    }
  }
  
  const response = await fetch('http://localhost:8888/api/v1/products/', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// Usage
const productData = {
  title: "Gaming Mouse",
  description: "High-precision gaming mouse with RGB lighting",
  price: 79.99,
  category: "Electronics",
  tags: ["gaming", "mouse", "rgb", "precision"]
};

const imageFiles = document.getElementById('imageInput').files;
const result = await createProductWithImages(productData, imageFiles);
console.log('Created product:', result);
```

### 2. Image Search

```javascript
async function searchByImage(imageFile, filters = {}) {
  // Convert image to base64
  const base64 = await fileToBase64(imageFile);
  
  const response = await fetch('http://localhost:8888/api/v1/products/search/image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      image: base64,
      ...filters
    })
  });
  
  return await response.json();
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

// Usage
const imageFile = document.getElementById('searchImage').files[0];
const results = await searchByImage(imageFile, {
  category: "Electronics",
  max_price: 200
});
console.log('Image search results:', results);
```

### 3. Multi-Modal Search

```javascript
async function multimodalSearch(textQuery, imageFile, filters = {}) {
  const payload = {
    text_query: textQuery,
    ...filters
  };
  
  if (imageFile) {
    payload.image_query = await fileToBase64(imageFile);
  }
  
  const response = await fetch('http://localhost:8888/api/v1/products/search/multimodal', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  });
  
  return await response.json();
}

// Usage
const textQuery = "wireless headphones";
const imageFile = document.getElementById('searchImage').files[0];
const results = await multimodalSearch(textQuery, imageFile, {
  category: "Electronics",
  max_price: 300,
  weight_text: 0.7,
  weight_image: 0.3
});
console.log('Multi-modal search results:', results);
```

## 🐍 Python Examples

### 1. Upload Product with Images

```python
import requests
from pathlib import Path

def create_product_with_images(product_data, image_paths=None):
    """Create a product with optional image uploads"""
    url = "http://localhost:8888/api/v1/products/"
    
    # Prepare form data
    files = {}
    data = {
        'title': product_data['title'],
        'description': product_data['description'],
        'price': product_data['price'],
        'category': product_data['category'],
        'tags': ','.join(product_data['tags'])
    }
    
    # Add images if provided
    if image_paths:
        for i, image_path in enumerate(image_paths):
            if Path(image_path).exists():
                files[f'images'] = open(image_path, 'rb')
    
    response = requests.post(url, data=data, files=files)
    
    # Close file handles
    for file in files.values():
        file.close()
    
    return response.json()

# Usage
product_data = {
    'title': 'Smart Watch',
    'description': 'Fitness tracking smartwatch with heart rate monitor',
    'price': 199.99,
    'category': 'Electronics',
    'tags': ['smartwatch', 'fitness', 'heart-rate', 'gps']
}

image_paths = ['watch1.jpg', 'watch2.jpg']
result = create_product_with_images(product_data, image_paths)
print(f"Created product: {result['title']}")
```

### 2. Image Search

```python
import requests
import base64
from PIL import Image
import io

def search_by_image(image_path, filters=None):
    """Search products using image similarity"""
    url = "http://localhost:8888/api/v1/products/search/image"
    
    # Convert image to base64
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
        base64_img = base64.b64encode(img_data).decode('utf-8')
        base64_img = f"data:image/jpeg;base64,{base64_img}"
    
    payload = {
        'image': base64_img
    }
    
    if filters:
        payload.update(filters)
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage
results = search_by_image('query_headphones.jpg', {
    'category': 'Electronics',
    'max_price': 200,
    'limit': 5
})
print(f"Found {len(results['products'])} similar products")
```

### 3. Multi-Modal Search

```python
def multimodal_search(text_query=None, image_path=None, filters=None):
    """Multi-modal search combining text and image queries"""
    url = "http://localhost:8888/api/v1/products/search/multimodal"
    
    payload = {}
    
    if text_query:
        payload['text_query'] = text_query
    
    if image_path:
        # Convert image to base64
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            base64_img = base64.b64encode(img_data).decode('utf-8')
            payload['image_query'] = f"data:image/jpeg;base64,{base64_img}"
    
    if filters:
        payload.update(filters)
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage
results = multimodal_search(
    text_query="wireless headphones",
    image_path="headphone_query.jpg",
    filters={
        'category': 'Electronics',
        'max_price': 300,
        'weight_text': 0.6,
        'weight_image': 0.4,
        'limit': 5
    }
)
print(f"Multi-modal search found {len(results['products'])} products")
```

## 🔧 Advanced Features

### 1. Batch Image Upload

```python
def batch_upload_products(products_data):
    """Upload multiple products with images"""
    results = []
    
    for product_data in products_data:
        try:
            result = create_product_with_images(
                product_data['data'], 
                product_data.get('images', [])
            )
            results.append(result)
            print(f"Uploaded: {result['title']}")
        except Exception as e:
            print(f"Failed to upload {product_data['data']['title']}: {e}")
    
    return results

# Example batch upload
products = [
    {
        'data': {
            'title': 'Laptop',
            'description': 'High-performance laptop for work and gaming',
            'price': 1299.99,
            'category': 'Electronics',
            'tags': ['laptop', 'gaming', 'performance']
        },
        'images': ['laptop1.jpg', 'laptop2.jpg']
    },
    {
        'data': {
            'title': 'Coffee Maker',
            'description': 'Programmable coffee maker with built-in grinder',
            'price': 149.99,
            'category': 'Home & Kitchen',
            'tags': ['coffee', 'programmable', 'grinder']
        },
        'images': ['coffee_maker.jpg']
    }
]

batch_results = batch_upload_products(products)
```

### 2. Visual Similarity Analysis

```python
def analyze_visual_similarity(product_id1, product_id2):
    """Analyze visual similarity between two products"""
    # Get product images
    product1 = get_product(product_id1)
    product2 = get_product(product_id2)
    
    if not product1['images'] or not product2['images']:
        return None
    
    # Compare first images of each product
    img1_path = product1['images'][0]['file_path']
    img2_path = product2['images'][0]['file_path']
    
    # Use CLIP to compute similarity
    similarity = compute_image_similarity(img1_path, img2_path)
    
    return {
        'product1': product1['title'],
        'product2': product2['title'],
        'similarity_score': similarity
    }
```

## 🎯 Key Multi-Modal Features

1. **CLIP Embeddings**: Uses OpenAI's CLIP model for image and text understanding
2. **Dual Vector Stores**: Separate collections for text and image embeddings
3. **File Upload Support**: Direct image upload with validation and optimization
4. **Multi-Modal Search**: Combine text and image queries for better results
5. **Visual Similarity**: Find visually similar products using image embeddings
6. **Real-time Indexing**: Images are immediately available for search after upload
7. **Vector Store Management**: Reset and monitor vector store operations

## 🔧 Admin Operations

### 1. Reset Vector Store

**⚠️ WARNING: This will delete ALL products and embeddings!**

**Endpoint:** `POST /api/v1/products/reset`

```bash
curl -X POST "http://localhost:8888/api/v1/products/reset" \
  -H "Content-Type: multipart/form-data" \
  -F "confirm=RESET"
```

**Response:**
```json
{
  "message": "Vector store reset successfully",
  "status": "success",
  "timestamp": "2024-01-15T10:30:00.123456",
  "warning": "All products and embeddings have been deleted",
  "confirmation": "RESET"
}
```

**Error Response (if confirmation is missing or incorrect):**
```json
{
  "detail": "Confirmation required. Set 'confirm' parameter to 'RESET' to proceed."
}
```

### 2. Get Vector Store Statistics

**Endpoint:** `GET /api/v1/products/stats`

```bash
curl -X GET "http://localhost:8888/api/v1/products/stats"
```

**Response:**
```json
{
  "vector_store_stats": {
    "text_collection_name": "products_text",
    "image_collection_name": "products_images",
    "text_documents_count": 15,
    "image_documents_count": 8,
    "total_documents": 23,
    "status": "active"
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 3. JavaScript Examples

```javascript
// Reset vector store
async function resetVectorStore() {
  const formData = new FormData();
  formData.append('confirm', 'RESET');
  
  const response = await fetch('http://localhost:8888/api/v1/products/reset', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log('Reset result:', result);
  
  if (result.status === 'success') {
    alert('⚠️ Vector store has been reset! All products deleted.');
  } else {
    alert('❌ Reset failed: ' + result.detail);
  }
}

// Get vector store stats
async function getVectorStoreStats() {
  const response = await fetch('http://localhost:8888/api/v1/products/stats');
  const result = await response.json();
  
  console.log('Vector store stats:', result.vector_store_stats);
  return result.vector_store_stats;
}

// Usage
const stats = await getVectorStoreStats();
console.log(`Total documents: ${stats.total_documents}`);
console.log(`Text documents: ${stats.text_documents_count}`);
console.log(`Image documents: ${stats.image_documents_count}`);
```

### 4. Python Examples

```python
import requests

def reset_vector_store():
    """Reset the entire vector store"""
    url = "http://localhost:8888/api/v1/products/reset"
    
    # Use form-data with confirmation
    data = {'confirm': 'RESET'}
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            print("✅ Vector store reset successfully!")
            print("⚠️  All products and embeddings have been deleted")
        else:
            print("❌ Failed to reset vector store")
        return result
    else:
        error_detail = response.json().get('detail', 'Unknown error')
        print(f"❌ Reset failed: {error_detail}")
        return None

def get_vector_store_stats():
    """Get vector store statistics"""
    url = "http://localhost:8888/api/v1/products/stats"
    
    response = requests.get(url)
    result = response.json()
    
    stats = result['vector_store_stats']
    print(f"📊 Vector Store Statistics:")
    print(f"   Total documents: {stats['total_documents']}")
    print(f"   Text documents: {stats['text_documents_count']}")
    print(f"   Image documents: {stats['image_documents_count']}")
    print(f"   Status: {stats['status']}")
    
    return stats

# Usage
stats = get_vector_store_stats()

# Reset if needed
if stats['total_documents'] > 1000:
    print("Too many documents, resetting...")
    reset_vector_store()
```

## 🚀 Getting Started

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Start the Server**: `python main.py`
3. **Upload Products**: Use the product creation API with images
4. **Search by Image**: Upload an image to find similar products
5. **Multi-Modal Search**: Combine text and image queries for better results
6. **Monitor Usage**: Use stats API to track vector store usage
7. **Reset When Needed**: Use reset API to clear all data and start fresh

The multi-modal system provides powerful visual search capabilities using CLIP embeddings, enabling users to find products by uploading images or combining text and visual queries! 