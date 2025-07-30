# ⚙️ dirt-detector

A production-ready **FastAPI microservice** for industrial dirt detection. This service uses computer vision techniques to analyze images and determine cleanliness with high precision. Designed for integration into automated cleaning robots.

---

## 🚀 Features

- ✅ Real-time dirt detection (~0.1–0.3s per image)
- 📷 Advanced analysis using:
  - Color-based filtering
  - Texture and surface irregularities
  - Edge detection
- 🔢 Returns:
  - `is_clean`: `true/false`
  - `confidence`: score (0.0–1.0)
  - `dirt_percentage`: % of dirt in image
  - `processing_time`: time taken in seconds
- 🧪 Batch image analysis supported
- 🐳 Docker-compatible and lightweight
- 📊 Logging and health check endpoints

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – REST API
- [OpenCV](https://opencv.org/) – image processing
- [scikit-image](https://scikit-image.org/) – feature extraction
- [Pillow](https://python-pillow.org/) – image handling
- [Docker](https://www.docker.com/) – containerization

---

## 📁 Project Structure

dirt-detector/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI routes
│ ├── dirt_detector.py # Dirt detection logic
│ └── config.py # Configuration class
├── .env # Optional env variables
├── requirements.txt # Python dependencies
├── Dockerfile # Docker setup
└── README.md # You're here!

## 📦 Installation

### Option 1: Local Development

```bash
git clone https://github.com/your-username/dirt-detector.git
cd dirt-detector
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


### Option 2: Docker
docker build -t dirt-detector .
docker run -p 8000:8000 dirt-detector


📡 API Endpoints

🩺 Health Check
http

GET /
GET /health


📤 Dirt Detection
http

POST /detect-dirt
Content-Type: multipart/form-data
Body: image file


Returns:
{
  "is_clean": false,
  "confidence": 0.82,
  "dirt_percentage": 8.3,
  "processing_time": 0.21
}


🔁 Batch Detection
http

POST /batch-detect
Content-Type: multipart/form-data
Body: multiple image files


🧪 Example Usage (cURL)
curl -X POST http://localhost:8000/detect-dirt \
  -F "file=@sample.jpg"


📘 Documentation
Access the Swagger UI at:

http
http://localhost:8000/docs
