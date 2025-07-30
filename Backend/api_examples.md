# Chatbot API Examples

This document provides sample API requests for interacting with the LangGraph Chatbot API.

## Base URL
```
http://localhost:8000
```

## API Endpoints

### 1. Chat with the Bot

**Endpoint:** `POST /api/v1/chat`

#### Basic Chat Request
```bash
curl -X POST "http://localhost:8888/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you today?",
    "user_id": "user123"
  }'
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
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

#### Continue Conversation (with thread_id)
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just ask you?",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123"
  }'
```

#### Chat with Context
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about Python programming",
    "user_id": "user123",
    "context": {
      "user_level": "beginner",
      "topic": "programming",
      "preferred_language": "Python"
    }
  }'
```

### 2. Get Thread History

**Endpoint:** `GET /api/v1/threads/{thread_id}/history`

```bash
curl -X GET "http://localhost:8000/api/v1/threads/550e8400-e29b-41d4-a716-446655440000/history"
```

**Response:**
```json
{
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "Hello! How are you today?",
      "timestamp": "2024-01-15T10:30:00.123456"
    },
    {
      "role": "assistant",
      "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
      "timestamp": "2024-01-15T10:30:01.234567"
    },
    {
      "role": "user",
      "content": "What did I just ask you?",
      "timestamp": "2024-01-15T10:30:05.345678"
    },
    {
      "role": "assistant",
      "content": "You just asked me 'Hello! How are you today?' and I responded that I'm doing well.",
      "timestamp": "2024-01-15T10:30:06.456789"
    }
  ],
  "metadata": {
    "user_id": "user123",
    "message_count": 4
  }
}
```

### 3. List All Threads

**Endpoint:** `GET /api/v1/threads`

#### List All Threads
```bash
curl -X GET "http://localhost:8000/api/v1/threads"
```

#### List Threads for Specific User
```bash
curl -X GET "http://localhost:8000/api/v1/threads?user_id=user123"
```

**Response:**
```json
[
  {
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123",
    "created_at": "2024-01-15T10:30:00.123456",
    "last_updated": "2024-01-15T10:30:06.456789",
    "message_count": 4
  },
  {
    "thread_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "user_id": "user456",
    "created_at": "2024-01-15T09:15:00.123456",
    "last_updated": "2024-01-15T09:20:00.234567",
    "message_count": 2
  }
]
```

### 4. Delete Thread

**Endpoint:** `DELETE /api/v1/threads/{thread_id}`

```bash
curl -X DELETE "http://localhost:8000/api/v1/threads/550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "message": "Thread deleted successfully",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 5. Health Check

**Endpoint:** `GET /api/v1/health`

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

**Response:**
```json
{
  "status": "healthy",
  "service": "chatbot-api"
}
```

## JavaScript/Node.js Examples

### Using fetch API
```javascript
// Basic chat request
async function chatWithBot(message, threadId = null, userId = null) {
  const payload = {
    message: message,
    user_id: userId
  };
  
  if (threadId) {
    payload.thread_id = threadId;
  }
  
  const response = await fetch('http://localhost:8000/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  });
  
  return await response.json();
}

// Usage examples
const response1 = await chatWithBot("Hello!", null, "user123");
console.log(response1.thread_id); // Save this for continuation

const response2 = await chatWithBot("Continue our conversation", response1.thread_id, "user123");
```

### Using axios
```javascript
const axios = require('axios');

async function chatWithBot(message, threadId = null, userId = null) {
  const payload = {
    message: message,
    user_id: userId
  };
  
  if (threadId) {
    payload.thread_id = threadId;
  }
  
  const response = await axios.post('http://localhost:8000/api/v1/chat', payload);
  return response.data;
}
```

## Python Examples

### Using requests
```python
import requests
import json

def chat_with_bot(message, thread_id=None, user_id=None):
    url = "http://localhost:8000/api/v1/chat"
    payload = {
        "message": message,
        "user_id": user_id
    }
    
    if thread_id:
        payload["thread_id"] = thread_id
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage examples
response1 = chat_with_bot("Hello!", user_id="user123")
print(f"Thread ID: {response1['thread_id']}")

response2 = chat_with_bot("Continue our conversation", 
                         thread_id=response1['thread_id'], 
                         user_id="user123")
```

### Using aiohttp (async)
```python
import aiohttp
import asyncio

async def chat_with_bot(message, thread_id=None, user_id=None):
    url = "http://localhost:8000/api/v1/chat"
    payload = {
        "message": message,
        "user_id": user_id
    }
    
    if thread_id:
        payload["thread_id"] = thread_id
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

# Usage
async def main():
    response1 = await chat_with_bot("Hello!", user_id="user123")
    print(f"Thread ID: {response1['thread_id']}")
    
    response2 = await chat_with_bot("Continue our conversation", 
                                   thread_id=response1['thread_id'], 
                                   user_id="user123")

asyncio.run(main())
```

## Request Body Schema

### ChatRequest
```json
{
  "message": "string (required) - The user's message",
  "thread_id": "string (optional) - Thread ID for conversation continuity",
  "user_id": "string (optional) - User identifier",
  "context": {
    "key": "value (optional) - Additional context information"
  }
}
```

## Response Schema

### ChatResponse
```json
{
  "response": "string - The assistant's response",
  "thread_id": "string - Thread ID for conversation continuity",
  "message_id": "string - Unique message identifier",
  "timestamp": "datetime - When the response was generated",
  "metadata": {
    "user_id": "string - User identifier",
    "timestamp": "datetime - Request timestamp",
    "context": "object - Request context"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Chat processing failed: Error message"
}
```

## Testing with the Provided Test Script

You can also use the included test script:

```bash
python test_api.py
```

This will run a series of tests demonstrating all the API functionality. 