import uuid
from pathlib import Path
from fastapi import HTTPException, status

MAX_IMAGE_SIZE = 5 * 1024 * 1024 # 5 MB

def set_unique_image_filename(original : str)-> str:
    ext = Path(original).suffix.lower()
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid file extension"
        )

    unique_filename = f"{uuid.uuid4().hex}{ext}"
    return unique_filename

def validate_image_size(content):
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code= status.HTTP_413_CONTENT_TOO_LARGE,
            detail="File too large"
        )