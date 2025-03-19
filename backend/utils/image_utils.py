import os
import asyncio
import numpy as np
from PIL import Image
import rawpy
from utils.model_utils import get_model
from utils.logging_utils import log_event

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp", ".cr2", ".nef", ".arw", ".dng"}

async def classify_images(image_paths, labels, websocket=None):
    """Classifies images in dynamically determined batches and updates progress in real-time."""
    ort_session, processor = get_model()
    total_images = len(image_paths)
    
    BATCH_SIZE = min(max(8, total_images // 10), 128)
    log_event(f"🔍 Using batch size: {BATCH_SIZE} for {total_images} images.")

    results = []
    
    for i in range(0, total_images, BATCH_SIZE):
        batch_paths = image_paths[i:i + BATCH_SIZE]
        images = await asyncio.to_thread(lambda: [load_image(p) for p in batch_paths])
        images = [img for img in images if img is not None]

        if not images:
            continue

        batch_results = await asyncio.to_thread(classify_batch, images, batch_paths, labels, ort_session, processor)
        results.extend(batch_results)

        progress = int(((i + len(batch_paths)) / total_images) * 100)
        log_event(f"📊 Progress: {progress}% - Processed {len(batch_paths)} images")
        
        if websocket:
            await websocket.send_json({"progress": progress})

    if websocket:
        await websocket.send_json({"message": "Classification completed.", "results": results})

    return results


def classify_batch(images, image_paths, labels, ort_session, processor):
    """Classify a batch of images."""
    inputs = processor(text=labels, images=images, return_tensors="np", padding=True)
    onnx_inputs = {
        "input_ids": inputs["input_ids"].astype(np.int64),
        "pixel_values": inputs["pixel_values"].astype(np.float32),
        "attention_mask": inputs["attention_mask"].astype(np.int64),
    }
    onnx_outputs = ort_session.run(None, onnx_inputs)

    logits_per_image = onnx_outputs[0]
    probs = np.exp(logits_per_image) / np.sum(np.exp(logits_per_image), axis=1, keepdims=True)
    predicted_indices = np.argmax(probs, axis=1).tolist()

    results = []
    for image_path, pred_idx, prob in zip(image_paths, predicted_indices, probs):
        predicted_label = labels[pred_idx]
        prob_log = " (" + " ".join([f"{labels[i]} {p:.0%}" for i, p in enumerate(prob)]) + ")"
        results.append({"filename": os.path.basename(image_path), "label": predicted_label, "confidence": prob_log})

        log_event(f"✅ Processed {os.path.basename(image_path)} -> {predicted_label} {prob_log}")

    return results


def load_image(image_path):
    """Load and preprocess an image efficiently."""
    ext = os.path.splitext(image_path)[1].lower()
    try:
        if ext in {".cr2", ".nef", ".arw", ".dng"}:
            with rawpy.imread(image_path) as raw:
                img = raw.postprocess()
            image = Image.fromarray(img)
        else:
            image = Image.open(image_path)
            if image.mode != "RGB":
                image = image.convert("RGB")

        image.thumbnail((224, 224))
        return image
    except Exception as e:
        log_event(f"❌ Error loading {image_path}: {e}")
        return None
