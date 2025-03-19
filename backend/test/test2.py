import requests
import asyncio
import websockets
import json

BASE_URL = "http://127.0.0.1:8000"

# ✅ Step 1: Send labels
def send_labels(labels):
    for label in labels:
        response = requests.post(f"{BASE_URL}/labels/", data={"label": label})
        if response.status_code == 200:
            print(f"✅ Label added: {label}")
        else:
            print(f"❌ Failed to add label: {response.json()}")

# ✅ Step 2: Trigger classification
async def classify_images():
    uri = f"ws://127.0.0.1:8000/classify/"
    
    async with websockets.connect(uri) as websocket:
        print("✅ Connected to WebSocket server.")

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
asyncio.run(classify_images())  # Step 2
