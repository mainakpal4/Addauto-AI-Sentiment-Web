# app/routes.py

import traceback
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas import SentimentRequest
from app.sentiment_api import analyze_sentiment
from app.voice_api import analyze_voice
from app.camera_api import router as camera_router  # ✅ Use absolute path for clarity

# Create primary router
router = APIRouter()

# ✅ Mount the camera router under '/analyze/camera'
router.include_router(camera_router, prefix="/analyze/camera", tags=["Camera"])

# ✅ Text Sentiment Analysis
@router.post("/analyze")
@router.post("/analyze/")
async def analyze_text(input_text: SentimentRequest):
    try:
        return await analyze_sentiment(input_text)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Voice Sentiment Analysis
@router.post("/analyze/voice/")
async def analyze_voice_route(audio: UploadFile = File(...)):
    try:
        return await analyze_voice(audio)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
