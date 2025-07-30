from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.api.routes import router
from app.api.product_routes import router as product_router
from app.config import settings

# Validate settings on startup
try:
    settings.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your environment variables.")
    exit(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting Chatbot API...")
    print(f"📝 Model: {settings.MODEL_NAME}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Chatbot API...")


# Create FastAPI app
app = FastAPI(
    title="Palona AI API",
    description="Demo API for Palona AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)
app.include_router(product_router)

# Mount static files for uploaded images
if os.path.exists(settings.MEDIA_UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.MEDIA_UPLOAD_DIR), name="uploads")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to LangGraph Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development,
        log_level="info"
    ) 