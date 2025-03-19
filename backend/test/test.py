import requests
import asyncio
import websockets
import json
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
IMAGE_DIR = "C:/project/image-classifier-app/backend/train"  # Folder with images
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp", ".cr2", ".nef", ".arw", ".dng"}

# ✅ Step 1: Send labels
def send_labels(labels):
    for label in labels:
        response = requests.post(f"{BASE_URL}/labels/", data={"label": label})
        if response.status_code == 200:
            print(f"✅ Label added: {label}")
        else:
            print(f"❌ Failed to add label: {response.json()}")

# ✅ Step 2: Read all image paths from the folder
def get_all_images(folder):
    return [str(p) for p in Path(folder).glob("*") if p.suffix.lower() in VALID_EXTENSIONS]

# ✅ Step 3: Upload image paths
def upload_images(image_paths):
    response = requests.post(f"{BASE_URL}/uploads/", json=image_paths)
    if response.status_code == 200:
        print(f"✅ Uploaded {len(image_paths)} images.")
    else:
        print(f"❌ Failed to upload images: {response.json()}")

# ✅ Step 4: WebSocket classification
async def classify_images(image_paths):
    uri = f"ws://127.0.0.1:8000/classify/"
    
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to WebSocket server.")

        # Send image paths
        await websocket.send(json.dumps({"image_paths": image_paths}))

        while True:
            response = await websocket.recv()
            print("📩 Received:", response)

            # ✅ Close WebSocket when classification is done
            if "Classification completed" in response:
                print("✅ Closing WebSocket connection.")
                await websocket.close()
                break  # Exit loop


# 🔹 Define labels
LABELS = ["cat", "dog", "unknown"]

# 🚀 Execute workflow
send_labels(LABELS)  # Step 1
IMAGE_PATHS = get_all_images(IMAGE_DIR)  # Step 2
print(f"🔍 Found {len(IMAGE_PATHS)} images in {IMAGE_DIR}")

if IMAGE_PATHS:
    upload_images(IMAGE_PATHS)  # Step 3
    asyncio.run(classify_images(IMAGE_PATHS))  # Step 4
else:
    print("⚠️ No valid images found!")
