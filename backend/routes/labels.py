from fastapi import APIRouter, Form, Query, HTTPException

router = APIRouter()

LABELS = []

@router.get("/labels/")
def get_labels():
    """Returns the list of labels."""
    return {"labels": LABELS}

@router.post("/labels/")
def add_label(label: str = Form(...)):
    """Adds a label for classification."""
    if label in LABELS:
        raise HTTPException(status_code=400, detail="Label already exists.")
    LABELS.append(label)
    return {"message": f"Added label: {label}", "labels": LABELS}

@router.delete("/labels/")
def remove_label(label: str = Query(...)):
    """Removes a label from classification."""
    if label not in LABELS:
        raise HTTPException(status_code=400, detail="Label not found.")
    LABELS.remove(label)
    return {"message": f"Removed label: {label}", "labels": LABELS}
