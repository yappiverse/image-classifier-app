from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
from routes.uploads import UPLOADED_FILES
from utils.logging_utils import log_event

router = APIRouter()

# Supported image formats
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp", ".cr2", ".nef", ".arw", ".dng"}

@router.get("/files/")
def get_uploaded_files():
    """
    Returns the list of uploaded image file paths.
    """
    if not UPLOADED_FILES:
        raise HTTPException(status_code=404, detail="No uploaded image files found")

    log_event(f"📂 Returning {len(UPLOADED_FILES)} uploaded images.")

    return {"total_files": len(UPLOADED_FILES), "files": UPLOADED_FILES}
