import os
import uvicorn
import socket
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import classify, labels, logs, uploads, health, files
from utils.model_utils import start_model_loading

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles FastAPI startup and shutdown efficiently."""

    # Ensure models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    # Start model loading in a separate thread
    start_model_loading()

    yield  # Let FastAPI run while the model loads in the background

    print("🛑 Shutting down...")


# Initialize FastAPI with lifespan
app = FastAPI(title="CLIP Image Classifier API", lifespan=lifespan)

# Configure CORS for Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
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
