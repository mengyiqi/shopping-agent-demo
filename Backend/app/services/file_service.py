import os
import uuid
import shutil
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

from app.models import ProductImage
from app.config import settings


class FileService:
    """Service for handling file uploads and storage"""
    
    def __init__(self):
        self.upload_dir = Path(settings.MEDIA_UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.images_dir = self.upload_dir / "images"
        self.images_dir.mkdir(exist_ok=True)
    
    async def save_image(self, file: UploadFile) -> ProductImage:
        """Save an uploaded image file"""
        
        # Validate file type
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not allowed. Allowed types: {settings.ALLOWED_IMAGE_TYPES}"
            )
        
        # Validate file size
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file.size} exceeds maximum allowed size of {settings.MAX_FILE_SIZE}"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix if file.filename else ".jpg"
        filename = f"{file_id}{file_extension}"
        
        # Create file path
        file_path = self.images_dir / filename
        
        try:
            # Read and validate image
            contents = await file.read()
            
            # Open with PIL to validate and potentially convert
            with Image.open(io.BytesIO(contents)) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Save optimized image
                img.save(file_path, 'JPEG', quality=85, optimize=True)
            
            # Get file size
            file_size = file_path.stat().st_size
            
            # Create ProductImage object
            product_image = ProductImage(
                id=file_id,
                filename=file.filename or filename,
                file_path=str(file_path),
                file_url=f"/uploads/images/{filename}",
                file_size=file_size,
                mime_type="image/jpeg",
                created_at=datetime.now()
            )
            
            return product_image
            
        except Exception as e:
            # Clean up if something goes wrong
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")
    
    async def save_multiple_images(self, files: List[UploadFile]) -> List[ProductImage]:
        """Save multiple uploaded image files"""
        images = []
        
        for file in files:
            try:
                image = await self.save_image(file)
                images.append(image)
            except Exception as e:
                # Continue with other files if one fails
                print(f"Error saving image {file.filename}: {e}")
                continue
        
        return images
    
    async def delete_image(self, image_id: str) -> bool:
        """Delete an image file"""
        try:
            # Find image file
            for file_path in self.images_dir.glob(f"{image_id}.*"):
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting image {image_id}: {e}")
            return False
    
    async def delete_product_images(self, images: List[ProductImage]) -> bool:
        """Delete multiple product images"""
        success = True
        for image in images:
            if not await self.delete_image(image.id):
                success = False
        return success
    
    def get_image_path(self, filename: str) -> Optional[Path]:
        """Get the full path to an image file"""
        file_path = self.images_dir / filename
        return file_path if file_path.exists() else None
    
    def get_image_url(self, filename: str) -> str:
        """Get the public URL for an image"""
        return f"/uploads/images/{filename}"
    
    async def validate_image(self, file: UploadFile) -> bool:
        """Validate an image file without saving it"""
        try:
            contents = await file.read()
            with Image.open(io.BytesIO(contents)) as img:
                # Basic validation - check if it's a valid image
                img.verify()
            return True
        except Exception:
            return False
    
    def get_storage_info(self) -> dict:
        """Get storage information"""
        total_size = sum(f.stat().st_size for f in self.images_dir.rglob('*') if f.is_file())
        file_count = len(list(self.images_dir.rglob('*')))
        
        return {
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_count": file_count,
            "upload_directory": str(self.upload_dir)
        } 