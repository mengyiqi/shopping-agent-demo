import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # Google Gemini Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-pro")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    SAFETY_SETTINGS: str = os.getenv("SAFETY_SETTINGS", "BLOCK_MEDIUM_AND_ABOVE")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # LangGraph Configuration
    MAX_CONVERSATION_LENGTH: int = int(os.getenv("MAX_CONVERSATION_LENGTH", "50"))
    MEMORY_K: int = int(os.getenv("MEMORY_K", "10"))
    
    # Multi-modal Configuration
    MEDIA_UPLOAD_DIR: str = os.getenv("MEDIA_UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    CLIP_MODEL_NAME: str = os.getenv("CLIP_MODEL_NAME", "openai/clip-vit-base-patch32")
    CLIP_DEVICE: str = os.getenv("CLIP_DEVICE", "cpu")

    AGENT_SIMILARITY_DISTANCE: float = float(os.getenv("AGENT_SIMILARITY_DISTANCE", "0.2"))
    
    # Validation
    def validate(self) -> None:
        """Validate required settings"""
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required")
        
        # Create media upload directory if it doesn't exist
        os.makedirs(self.MEDIA_UPLOAD_DIR, exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.DEBUG


# Global settings instance
settings = Settings() 