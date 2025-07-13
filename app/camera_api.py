# ✅ File: app/camera_api.py

from fastapi import APIRouter, HTTPException, UploadFile, File
from app.camera_utils.deepface_camera import analyze_camera_emotion

router = APIRouter()

@router.post("/")
async def analyze_camera(image: UploadFile = File(...)):  # ✅ Accept uploaded file
    try:
        result = await analyze_camera_emotion(image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Camera analysis failed: {str(e)}")
