from fastapi import APIRouter
from utils.logging_utils import LOGS

router = APIRouter()

@router.get("/logs/")
def get_logs():
    """Retrieves classification logs."""
    return {"logs": LOGS}

@router.delete("/logs/")
def clear_logs():
    """Clears the classification logs."""
    global LOGS
    LOGS = []
    return {"message": "Logs cleared."}
