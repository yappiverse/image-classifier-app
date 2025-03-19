from fastapi import APIRouter, WebSocket
import asyncio
from routes.uploads import UPLOADED_FILES
from utils.image_utils import classify_images
from utils.logging_utils import log_event
from routes.labels import LABELS

router = APIRouter()

@router.websocket("/classify/")
async def classify(websocket: WebSocket):
    """Classifies images and provides real-time progress updates via WebSocket. Auto-cleans files & labels after completion."""
    await websocket.accept()

    if not LABELS:
        await websocket.send_json({"error": "No labels defined for classification."})
        await websocket.close()  # ✅ Close connection
        return

    if not UPLOADED_FILES:
        await websocket.send_json({"error": "No images found for classification."})
        await websocket.close()  # ✅ Close connection
        return

    try:
        log_event(f"🔍 Starting classification for {len(UPLOADED_FILES)} images.")

        results = await classify_images(UPLOADED_FILES, LABELS, websocket)

        # ✅ Send final message before cleanup
        await websocket.send_json({"message": "Classification completed.", "results": results})
        log_event("✅ Classification completed.")

        # ✅ Perform cleanup after a short delay (to allow final messages to be processed)
        await asyncio.sleep(2)
        delete_all_files_and_labels()

    except Exception as e:
        log_event(f"❌ WebSocket Error: {e}")
        await websocket.send_json({"error": f"Failed to process images: {e}"})

def delete_all_files_and_labels():
    """Clears the list of image paths and labels without deleting actual files."""
    try:
        log_event("🗑️ Clearing stored image paths (but keeping files intact).")

        UPLOADED_FILES.clear()
        log_event("🗑️ Cleared all file paths.")
        
        LABELS.clear()
        log_event("🗑️ Cleared all labels.")

    except Exception as e:
        log_event(f"❌ Cleanup failed: {e}")
