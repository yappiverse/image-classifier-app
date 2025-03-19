# Image Classifier Backend

A FastAPI-based backend for image classification using CLIP (Contrastive Language-Image Pretraining) model.

## Features

- Image classification API
- File upload and management
- Health check endpoints
- Logging and monitoring
- Model inference optimization

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/image-classifier-app.git
cd image-classifier-app/backend
```

2. Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download CLIP model parts and place them in `backend/models/`

## API Documentation

### Endpoints

- `POST /classify` - Classify an image
- `POST /upload` - Upload an image
- `GET /files` - List uploaded files
- `GET /health` - Health check
- `GET /labels` - Get available classification labels

### Example Requests

Classify an image:

```bash
curl -X POST "http://localhost:8000/classify" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

Upload an image:

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

## File Structure

```
backend/
├── main.py                # Application entry point
├── requirements.txt       # Dependencies
├── models/                # CLIP model parts
├── routes/                # API endpoints
│   ├── classify.py        # Image classification
│   ├── files.py           # File management
│   ├── health.py          # Health checks
│   ├── labels.py          # Label management
│   ├── logs.py            # Logging
│   └── uploads.py         # File uploads
├── utils/                 # Utility functions
│   ├── image_utils.py     # Image processing
│   ├── logging_utils.py   # Logging configuration
│   └── model_utils.py     # Model loading and inference
└── test/                  # Test files
    ├── test.py
    └── test2.py
```

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Testing

Run tests:

```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
