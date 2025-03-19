# Image Classifier Desktop Application

A desktop application for automatically sorting uploaded photos using AI classification. Built with Electron for the frontend and Python for the backend.

## Features

- **Automatic Photo Sorting**: Upload photos and they'll be automatically sorted into categories
- **Desktop Interface**: Native desktop experience with Electron
- **AI-Powered Classification**: Backend uses CLIP model for accurate image classification
- **Custom Categories**: Define your own classification categories
- **File Management**: View and manage sorted photos through the interface

## Project Structure

```
image-classifier-app/
├── backend/               # Python backend
│   ├── models/            # AI model files
│   ├── routes/            # API endpoints
│   ├── utils/             # Utility functions
│   ├── main.py            # Backend entry point
│   ├── requirements.txt   # Python dependencies
│   └── readme.md          # Backend documentation
|
├── frontend/              # Electron frontend
│   └── readme.md          # Frontend documentation
└── readme.md              # This file
```

## Installation

1. **Backend Setup**

   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

2. **Frontend Setup**

## Usage

1. Launch both backend and frontend
2. In the Electron app:
   - Click "Upload Photos" to select images
   - Photos will be automatically sorted into categories
   - View sorted photos in the file explorer interface

## Technology Stack

- **Frontend**: Electron, React, TypeScript
- **Backend**: Python, FastAPI, CLIP model
- **AI**: OpenAI's CLIP for image classification

## License

MIT License - See [LICENSE](LICENSE) for details
