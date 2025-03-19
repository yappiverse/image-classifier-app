import os
import onnxruntime as ort
from transformers import CLIPProcessor

# Global variables for the model and processor
ort_session = None
processor = None

# File paths
MODEL_PATH = "models/clip_model_quantized.onnx"
SPLIT_PREFIX = "models/clip_model_part_"
CHUNK_SIZE = 90 * 1024 * 1024  # 90MB


def split_model():
    """Splits the ONNX model into 90MB chunks for GitHub compatibility."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file {MODEL_PATH} not found!")

    with open(MODEL_PATH, "rb") as f:
        index = 0
        while chunk := f.read(CHUNK_SIZE):
            with open(f"{SPLIT_PREFIX}{index}.part", "wb") as chunk_file:
                chunk_file.write(chunk)
            index += 1
    print(f"Model split into {index} parts.")


def combine_model():
    """Combines the split model files back into a single ONNX model."""
    with open(MODEL_PATH, "wb") as f:
        index = 0
        while os.path.exists(f"{SPLIT_PREFIX}{index}.part"):
            with open(f"{SPLIT_PREFIX}{index}.part", "rb") as chunk_file:
                f.write(chunk_file.read())
            index += 1
    print(f"Model reassembled from {index} parts.")


def load_model():
    """Loads the ONNX model and CLIP processor at startup."""
    global ort_session, processor
    if ort_session is None:
        ort_session = ort.InferenceSession(MODEL_PATH)
    if processor is None:
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def get_model():
    """Returns the loaded ONNX model and processor."""
    if ort_session is None or processor is None:
        load_model()
    return ort_session, processor
