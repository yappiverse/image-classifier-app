import os
import uvicorn
import socket
import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import classify, labels, logs, uploads, health, files
from utils.model_utils import MODEL_PATH, SPLIT_PREFIX, combine_model, load_model

# Track model status
model_loaded = False  

def load_model_in_background():
    """Loads the model in a separate thread to avoid blocking FastAPI startup."""
    global model_loaded
    print("🚀 Loading model in background...")
    
    if not os.path.exists(MODEL_PATH):
        split_files = [f for f in os.listdir("models") if f.startswith(os.path.basename(SPLIT_PREFIX))]
        
        if split_files:
            print("🛠️ Detected split model parts. Reassembling...")
            combine_model()
        else:
            print(f"❌ ERROR: Model file '{MODEL_PATH}' is missing and no split parts found.")
            return
    
    load_model()
    model_loaded = True  # Mark model as loaded
    print("✅ Model loaded successfully!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles app startup and shutdown without blocking FastAPI."""
    
    # Ensure models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    # Load model in a separate thread
    threading.Thread(target=load_model_in_background, daemon=True).start()

    yield  # Hand over control to FastAPI while model loads in the background
    
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
    port = int(os.getenv("PORT", 8000))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("0.0.0.0", port)) == 0:
            print(f"⚠️ Port {port} is in use. Finding a free port...")
            port = 0  # Let the OS find a free port

    if port == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 0))
            port = s.getsockname()[1]

    print(f"🚀 Server starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
