from fastapi import APIRouter, HTTPException
from pathlib import Path
from utils.logging_utils import log_event

router = APIRouter()

UPLOADED_FILES = []  # Global list to store uploaded file paths
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp", ".cr2", ".nef", ".arw", ".dng"}

@router.post("/uploads/")
async def process_images(image_paths: list[str]):
    """Processes images given their file paths."""
    global UPLOADED_FILES  # Use global variable
    valid_paths = []

    for path in image_paths:
        file_path = Path(path)

        if not file_path.exists():
            raise HTTPException(status_code=400, detail=f"File not found: {file_path}")
        
        if file_path.suffix.lower() not in VALID_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_path}")

        valid_paths.append(str(file_path))

    # ✅ Store uploaded file paths
    UPLOADED_FILES.extend(valid_paths)
    log_event(f"Received {len(valid_paths)} images for processing.")

    return {"message": f"Received {len(valid_paths)} images.", "files": valid_paths}
