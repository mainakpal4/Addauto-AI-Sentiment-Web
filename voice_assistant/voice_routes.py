from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, validator
from datetime import datetime
from voice_assistant.audio_utils import (
    process_emotion, generate_response, text_to_speech,
    transcribe_audio, emoji_map
)
import langid
import uuid
import os

router = APIRouter()

class RequestText(BaseModel):
    text: str = Field(..., min_length=1)
    
    @validator("text")
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError("Text cannot be empty")
        return value

@router.post("/analyze/")
async def analyze(req: RequestText):
    top, main = process_emotion(req.text)
    lang = langid.classify(req.text)[0]
    reply = generate_response(main["label"])
    audio_path = f"response_{uuid.uuid4().hex}.mp3"
    text_to_speech(reply, audio_path)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "text": req.text,
        "language": lang,
        "emotion": main["label"],
        "confidence": main["score"],
        "emoji": emoji_map.get(main["label"], "❓"),
        "response": reply,
        "audio_file": audio_path
    }

@router.post("/analyze/voice/")
async def analyze_voice(audio: UploadFile = File(...)):
    if not audio.filename.endswith(".wav"):
        raise HTTPException(400, "Only .wav files supported.")
    
    text = transcribe_audio(audio)
    top, main = process_emotion(text)
    reply = generate_response(main["label"])
    audio_path = f"response_{uuid.uuid4().hex}.mp3"
    text_to_speech(reply, audio_path)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "transcribed_text": text,
        "emotion": main["label"],
        "confidence": main["score"],
        "emoji": emoji_map.get(main["label"], "❓"),
        "response": reply,
        "audio_file": audio_path
    }
