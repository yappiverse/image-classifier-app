import os
import uvicorn
import socket
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import classify, labels, logs, uploads, health, files
from utils.model_utils import MODEL_PATH, SPLIT_PREFIX, combine_model, load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure the models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    # Check if the ONNX model exists; if not, check for split parts and combine
    if not os.path.exists(MODEL_PATH):
        split_files = [f for f in os.listdir("models") if f.startswith(os.path.basename(SPLIT_PREFIX))]
        
        if split_files:
            print("🛠️ Detected split model parts. Reassembling...")
            combine_model()
        else:
            print(f"❌ ERROR: Model file '{MODEL_PATH}' is missing and no split parts found.")
            raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found!")

    print("🚀 Loading model on startup...")
    load_model()
    
    yield
    
    print("🛑 Shutting down...")

# Initialize FastAPI with lifespan
app = FastAPI(title="CLIP Image Classifier API", lifespan=lifespan)

# Register routes
app.include_router(uploads.router)
app.include_router(classify.router)
app.include_router(labels.router)
app.include_router(logs.router)
app.include_router(health.router)
app.include_router(files.router)


if __name__ == "__main__":
    # Get user-defined port (if any), else default to 8000
    port = int(os.getenv("PORT", 8000))

    # Check if the port is available
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("0.0.0.0", port)) == 0:
            print(f"⚠️ Port {port} is in use. Finding a free port...")
            port = 0  # Let the OS find a free port

    # If port is 0, find a free one
    if port == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 0))
            port = s.getsockname()[1]

    print(f"🚀 Server starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
