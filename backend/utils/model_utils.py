import os
import threading
import onnxruntime as ort
from transformers import CLIPProcessor

# Global variables for the model and processor
ort_session = None
processor = None

MODEL_STATUS = {"loaded": False}
# File paths
MODEL_PATH = "models/clip_model_quantized.onnx"
SPLIT_PREFIX = "models/clip_model_part_"
CHUNK_SIZE = 90 * 1024 * 1024


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
    print(f"✅ Model split into {index} parts.")


def combine_model():
    """Combines the split model files back into a single ONNX model."""
    with open(MODEL_PATH, "wb") as f:
        index = 0
        while os.path.exists(f"{SPLIT_PREFIX}{index}.part"):
            with open(f"{SPLIT_PREFIX}{index}.part", "rb") as chunk_file:
                f.write(chunk_file.read())
            index += 1
    print(f"✅ Model reassembled from {index} parts.")


def load_model_in_background():
    """Loads the ONNX model and CLIP processor in a separate thread."""
    global ort_session, processor
    try:
        print("🚀 Loading ONNX model in background...")

        if not os.path.exists(MODEL_PATH):
            split_files = [f for f in os.listdir("models") if f.startswith(os.path.basename(SPLIT_PREFIX))]

            if split_files:
                print("🛠️ Detected split model parts. Reassembling...")
                combine_model()
            else:
                print(f"❌ ERROR: Model file '{MODEL_PATH}' is missing and no split parts found.")
                return

        ort_session = ort.InferenceSession(MODEL_PATH)
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        MODEL_STATUS["loaded"] = True

        print("✅ Model loaded successfully!")

    except Exception as e:
        print(f"⚠️ Model loading failed: {e}")



def start_model_loading():
    """Starts the model loading in a separate thread to prevent blocking startup."""
    threading.Thread(target=load_model_in_background, daemon=True).start()


def get_model():
    """Returns the loaded ONNX model and processor."""
    if ort_session is None or processor is None:
        load_model_in_background()
    return ort_session, processor
