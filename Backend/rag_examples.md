# RAG-Enhanced Chatbot API Examples

This document provides examples for the enhanced chatbot with RAG (Retrieval-Augmented Generation) capabilities and product management.

## Base URL
```
http://localhost:8888
```

## 🛍️ Product Management APIs

### 1. Create a Product

**Endpoint:** `POST /api/v1/products/`

```bash
curl -X POST "http://localhost:8888/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Wireless Bluetooth Headphones",
    "description": "High-quality wireless headphones with noise cancellation, 30-hour battery life, and premium sound quality. Perfect for music lovers and professionals.",
    "price": 129.99,
    "category": "Electronics",
    "tags": ["wireless", "bluetooth", "noise-cancellation", "audio"],
    "images": [
      "https://example.com/headphones1.jpg",
      "https://example.com/headphones2.jpg"
    ]
  }'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Wireless Bluetooth Headphones",
  "description": "High-quality wireless headphones with noise cancellation, 30-hour battery life, and premium sound quality. Perfect for music lovers and professionals.",
  "price": 129.99,
  "category": "Electronics",
  "tags": ["wireless", "bluetooth", "noise-cancellation", "audio"],
  "images": [
    "https://example.com/headphones1.jpg",
    "https://example.com/headphones2.jpg"
  ],
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

### 2. Add More Products

```bash
# Smartphone
curl -X POST "http://localhost:8888/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15 Pro",
    "description": "Latest iPhone with A17 Pro chip, 48MP camera, titanium design, and all-day battery life. Available in multiple colors.",
    "price": 999.99,
    "category": "Electronics",
    "tags": ["smartphone", "iphone", "camera", "titanium"],
    "images": ["https://example.com/iphone15.jpg"]
  }'

# Laptop
curl -X POST "http://localhost:8888/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MacBook Air M2",
    "description": "Ultra-thin laptop with M2 chip, 13.6-inch Liquid Retina display, up to 18 hours battery life, and fanless design.",
    "price": 1199.99,
    "category": "Electronics",
    "tags": ["laptop", "macbook", "m2", "ultrabook"],
    "images": ["https://example.com/macbook-air.jpg"]
  }'

# Coffee Maker
curl -X POST "http://localhost:8888/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Programmable Coffee Maker",
    "description": "12-cup programmable coffee maker with auto-shutoff, pause-and-serve, and permanent coffee filter. Perfect for home or office.",
    "price": 49.99,
    "category": "Home & Kitchen",
    "tags": ["coffee", "programmable", "12-cup", "auto-shutoff"],
    "images": ["https://example.com/coffee-maker.jpg"]
  }'
```

### 3. Search Products

**Semantic Search:**
```bash
curl -X POST "http://localhost:8888/api/v1/products/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "wireless audio devices",
    "category": "Electronics",
    "max_price": 200.00,
    "limit": 5
  }'
```

**Simple Search:**
```bash
curl -X GET "http://localhost:8888/api/v1/products/search/simple?q=bluetooth&category=Electronics&max_price=150&limit=5"
```

### 4. Get Products by Category

```bash
curl -X GET "http://localhost:8888/api/v1/products/category/Electronics?limit=10"
```

### 5. Get All Products

```bash
curl -X GET "http://localhost:8888/api/v1/products/?limit=20"
```

## 🤖 RAG-Enhanced Chat Examples

Now that we have products in the system, the chatbot can answer questions about them using RAG!

### 1. Product Information Queries

```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What wireless headphones do you have?",
    "user_id": "user123"
  }'
```

**Expected Response:**
```json
{
  "response": "I have Wireless Bluetooth Headphones available for $129.99. These are high-quality wireless headphones with noise cancellation, 30-hour battery life, and premium sound quality. They're perfect for music lovers and professionals. The headphones come with features like noise cancellation and are tagged as wireless, bluetooth, noise-cancellation, and audio devices.",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "timestamp": "2024-01-15T10:30:00.123456",
  "metadata": {
    "user_id": "user123",
    "timestamp": "2024-01-15T10:30:00.123456",
    "context": {}
  }
}
```

### 2. Price Comparison

```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What electronics do you have under $1000?",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123"
  }'
```

### 3. Product Recommendations

```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a laptop for work, what do you recommend?",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123"
  }'
```

### 4. Specific Product Details

```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more about the iPhone 15 Pro",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123"
  }'
```

### 5. Category-Based Questions

```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What kitchen appliances do you have?",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123"
  }'
```

## 🔍 Advanced RAG Features

### 1. Context-Aware Conversations

The chatbot remembers previous interactions and can provide contextual responses:

```bash
# First message
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I'm looking for a good laptop",
    "user_id": "user123"
  }'

# Follow-up (using the returned thread_id)
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about the battery life?",
    "thread_id": "RETURNED_THREAD_ID",
    "user_id": "user123"
  }'
```

### 2. Product Comparison

```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Compare the iPhone and MacBook for me",
    "user_id": "user123"
  }'
```

## 🛠️ Product Management Operations

### Update a Product

```bash
curl -X PUT "http://localhost:8888/api/v1/products/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 119.99,
    "tags": ["wireless", "bluetooth", "noise-cancellation", "audio", "sale"]
  }'
```

### Delete a Product

```bash
curl -X DELETE "http://localhost:8888/api/v1/products/550e8400-e29b-41d4-a716-446655440000"
```

### Get Product by ID

```bash
curl -X GET "http://localhost:8888/api/v1/products/550e8400-e29b-41d4-a716-446655440000"
```

## 📊 JavaScript Examples

### Product Management

```javascript
// Create a product
async function createProduct(productData) {
  const response = await fetch('http://localhost:8888/api/v1/products/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData)
  });
  return await response.json();
}

// Search products
async function searchProducts(query, filters = {}) {
  const response = await fetch('http://localhost:8888/api/v1/products/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      ...filters
    })
  });
  return await response.json();
}

// Chat with RAG
async function chatWithRAG(message, threadId = null) {
  const payload = {
    message,
    user_id: 'user123'
  };
  
  if (threadId) {
    payload.thread_id = threadId;
  }
  
  const response = await fetch('http://localhost:8888/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  });
  return await response.json();
}

// Usage example
async function demo() {
  // Create a product
  const product = await createProduct({
    title: "Gaming Mouse",
    description: "High-precision gaming mouse with RGB lighting and programmable buttons",
    price: 79.99,
    category: "Electronics",
    tags: ["gaming", "mouse", "rgb", "programmable"]
  });
  
  // Chat about the product
  const chatResponse = await chatWithRAG("Tell me about gaming accessories");
  console.log(chatResponse.response);
}
```

## 🐍 Python Examples

### Complete RAG Workflow

```python
import requests
import json

class RAGChatbotClient:
    def __init__(self, base_url="http://localhost:8888"):
        self.base_url = base_url
    
    def create_product(self, product_data):
        """Create a new product"""
        response = requests.post(
            f"{self.base_url}/api/v1/products/",
            json=product_data
        )
        return response.json()
    
    def search_products(self, query, **filters):
        """Search products"""
        response = requests.post(
            f"{self.base_url}/api/v1/products/search",
            json={"query": query, **filters}
        )
        return response.json()
    
    def chat(self, message, thread_id=None, user_id="user123"):
        """Chat with RAG-enhanced bot"""
        payload = {
            "message": message,
            "user_id": user_id
        }
        if thread_id:
            payload["thread_id"] = thread_id
        
        response = requests.post(
            f"{self.base_url}/api/v1/chat",
            json=payload
        )
        return response.json()

# Usage example
def demo_rag_workflow():
    client = RAGChatbotClient()
    
    # 1. Add products to the system
    products = [
        {
            "title": "Wireless Earbuds",
            "description": "True wireless earbuds with active noise cancellation and 24-hour battery life",
            "price": 89.99,
            "category": "Electronics",
            "tags": ["wireless", "earbuds", "noise-cancellation"]
        },
        {
            "title": "Smart Watch",
            "description": "Fitness tracking smartwatch with heart rate monitor and GPS",
            "price": 199.99,
            "category": "Electronics",
            "tags": ["smartwatch", "fitness", "gps", "heart-rate"]
        }
    ]
    
    for product in products:
        result = client.create_product(product)
        print(f"Created product: {result['title']}")
    
    # 2. Chat about products
    response = client.chat("What wireless devices do you have?")
    print(f"Bot response: {response['response']}")
    
    # 3. Continue conversation
    thread_id = response['thread_id']
    follow_up = client.chat("Tell me more about the earbuds", thread_id)
    print(f"Follow-up response: {follow_up['response']}")

if __name__ == "__main__":
    demo_rag_workflow()
```

## 🎯 Key RAG Features

1. **Semantic Search**: Products are indexed using embeddings for natural language queries
2. **Context Retrieval**: Relevant product information is automatically retrieved based on user queries
3. **Conversational Memory**: Thread-based conversations maintain context across interactions
4. **Product Knowledge**: The bot can answer specific questions about products, prices, and features
5. **Real-time Updates**: Product information is immediately available to the chatbot after creation

## 🚀 Getting Started

1. **Start the server**: `python main.py`
2. **Add products**: Use the product creation APIs
3. **Chat with RAG**: Ask questions about products using natural language
4. **Explore features**: Try different types of queries and see how RAG enhances responses

The RAG system automatically retrieves relevant product information and provides it to the chatbot, enabling intelligent product recommendations and detailed responses about your inventory! 