from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any
from dirt_detector import DirtDetector
from config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Industrial Dirt Detection API",
    description="Microservice for detecting dirt in images for automated cleaning robots",
    version="1.0.0"
)

# Initialize settings and dirt detector
settings = Settings()
dirt_detector = DirtDetector(settings)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Dirt Detection API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "dirt-detection-api",
        "version": "1.0.0"
    }


@app.post("/detect-dirt")
async def detect_dirt(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analyze uploaded image for dirt detection

    Returns:
        - is_clean: Boolean indicating if surface is clean
        - confidence: Confidence score (0-1)
        - dirt_percentage: Percentage of image containing dirt
        - processing_time: Time taken for analysis in seconds
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Convert PIL image to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform dirt detection
        result = dirt_detector.analyze_image(cv_image)

        logger.info(f"Processed image: {file.filename}, Clean: {result['is_clean']}")

        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/batch-detect")
async def batch_detect_dirt(files: list[UploadFile] = File(...)) -> Dict[str, Any]:
    """
    Analyze multiple images for dirt detection
    """
    try:
        results = []

        for file in files:
            if not file.content_type.startswith('image/'):
                continue

            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            result = dirt_detector.analyze_image(cv_image)
            result['filename'] = file.filename
            results.append(result)

        # Calculate overall cleanliness
        clean_count = sum(1 for r in results if r['is_clean'])
        overall_clean = clean_count == len(results)

        return JSONResponse(content={
            "overall_clean": overall_clean,
            "clean_images": clean_count,
            "total_images": len(results),
            "individual_results": results
        })

    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in batch processing: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)