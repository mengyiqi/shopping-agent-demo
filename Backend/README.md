# LangGraph Chatbot API

A powerful Python backend for an LLM chatbot built with LangGraph, featuring agentic workflows, thread management, and memory capabilities.

## Features

- 🤖 **LangGraph Agentic Workflow**: Advanced conversation processing with state management
- 🧵 **Thread Management**: Persistent conversation threads with memory
- 💾 **Memory Capabilities**: Long-term conversation memory using LangGraph checkpoints
- 🔄 **Async API**: FastAPI-based REST API with async processing
- 📝 **Google Gemini Integration**: Powered by Google's Gemini models
- 🛡️ **Type Safety**: Full Pydantic model validation
- 📚 **Auto-generated Docs**: Interactive API documentation
- 🔍 **RAG (Retrieval-Augmented Generation)**: Semantic search and context retrieval using ChromaDB
- 🛍️ **Product Management**: Complete CRUD operations for product catalog
- 🧠 **Semantic Search**: Vector-based product search with embeddings

## Architecture

```
app/
├── agent/
│   └── chatbot_agent.py    # LangGraph agent implementation with RAG
├── api/
│   ├── routes.py          # FastAPI route definitions
│   └── product_routes.py  # Product management routes
├── services/
│   ├── chat_service.py    # Business logic layer
│   └── product_service.py # Product management service
├── rag/
│   └── vector_store.py    # ChromaDB vector store implementation
├── models.py              # Pydantic data models
└── config.py              # Configuration management
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Copy the environment example and configure your settings:

```bash
cp env_example.txt .env
```

**Get a Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key to your `.env` file

Edit `.env` with your configuration:

```env
# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# LangGraph Configuration
MAX_TOKENS=1000
TEMPERATURE=0.7
MODEL_NAME=gemini-pro
```

### 3. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Root Endpoint**: http://localhost:8000/

## API Endpoints

### Chat Endpoints

#### POST `/api/v1/chat`
Send a message to the chatbot with RAG capabilities.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "thread_id": "optional-thread-id",
  "user_id": "optional-user-id",
  "context": {
    "additional_info": "any context data"
  }
}
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "thread_id": "generated-thread-id",
  "message_id": "unique-message-id",
  "timestamp": "2024-01-01T12:00:00",
  "metadata": {
    "user_id": "user-123",
    "timestamp": "2024-01-01T12:00:00",
    "context": {}
  }
}
```

### Product Management

#### POST `/api/v1/products/`
Create a new product.

#### GET `/api/v1/products/`
Get all products.

#### GET `/api/v1/products/{product_id}`
Get a specific product by ID.

#### PUT `/api/v1/products/{product_id}`
Update an existing product.

#### DELETE `/api/v1/products/{product_id}`
Delete a product.

#### POST `/api/v1/products/search`
Search products using semantic similarity.

#### GET `/api/v1/products/search/simple`
Simple search with query parameters.

#### GET `/api/v1/products/category/{category}`
Get products by category.

### Thread Management

#### GET `/api/v1/threads`
List all conversation threads.

**Query Parameters:**
- `user_id` (optional): Filter threads by user ID

#### GET `/api/v1/threads/{thread_id}/history`
Get conversation history for a specific thread.

#### DELETE `/api/v1/threads/{thread_id}`
Delete a conversation thread.

### Health Check

#### GET `/api/v1/health`
Check API health status.

## LangGraph Features

### Agentic Workflow

The chatbot uses LangGraph's state graph to process messages through multiple stages:

1. **Message Processing**: Analyze and prepare the incoming message
2. **RAG Context Retrieval**: Get relevant product information from vector store
3. **Response Generation**: Generate response using the LLM with retrieved context
4. **Memory Update**: Store the interaction in conversation memory

### RAG Capabilities

- **Semantic Search**: Products are indexed using embeddings for natural language queries
- **Context Retrieval**: Relevant product information is automatically retrieved based on user queries
- **Vector Store**: ChromaDB provides efficient similarity search and storage
- **Real-time Updates**: Product information is immediately available to the chatbot after creation

### Thread Management

- **Persistent Threads**: Each conversation thread maintains its own state
- **Memory Checkpoints**: LangGraph's memory saver persists conversation history
- **Thread Isolation**: Conversations are isolated by thread ID

### Memory Capabilities

- **Conversation Memory**: Full conversation history is maintained
- **Context Awareness**: The agent remembers previous interactions
- **State Persistence**: Memory is persisted across API calls

## Development

### Project Structure

```
Backend/
├── app/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   └── chatbot_agent.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── chat_service.py
│   ├── config.py
│   └── models.py
├── main.py
├── requirements.txt
├── env_example.txt
└── README.md
```

### Adding Custom Tools

To add custom tools to the agent, modify `app/agent/chatbot_agent.py`:

```python
from langchain_core.tools import tool

@tool
def custom_tool(input: str) -> str:
    """Description of what this tool does."""
    # Your tool logic here
    return "Tool result"

# Add to the agent graph
workflow.add_node("custom_tool", custom_tool)
```

### Configuration

Key configuration options in `app/config.py`:

- `MODEL_NAME`: Google Gemini model to use (e.g., gemini-pro, gemini-pro-vision, gemini-1.5-pro)
- `TEMPERATURE`: Response creativity (0.0-1.0)
- `MAX_TOKENS`: Maximum output tokens
- `MEMORY_K`: Number of recent messages to keep in memory

## Production Deployment

### Environment Variables

For production, ensure these environment variables are set:

```env
GOOGLE_API_KEY=your_production_api_key
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Security Considerations

1. **API Key Security**: Store API keys securely using environment variables
2. **CORS Configuration**: Configure CORS origins properly for production
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Authentication**: Add authentication/authorization as needed

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **Google API Key Error**: Ensure your API key is valid and has sufficient credits
2. **Import Errors**: Make sure all dependencies are installed
3. **Memory Issues**: Check LangGraph memory configuration
4. **Thread Not Found**: Verify thread ID exists before accessing

### Logs

Enable debug logging by setting `DEBUG=True` in your environment variables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 