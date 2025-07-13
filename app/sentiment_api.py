# app/sentiment_api.py

from transformers import pipeline
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import langid
import logging
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emotion classification pipeline (GoEmotions model)
sentiment_pipeline = pipeline(
    "text-classification",
    model="joeddav/distilbert-base-uncased-go-emotions-student",
    top_k=None
)

# Whisper for voice-to-text transcription
whisper_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    device=-1  # Use CPU; change to 0 for GPU
)

# Extended emoji map for 38+ emotions
emoji_map = {
    "admiration": "👏", "amusement": "😂", "anger": "😠", "annoyance": "😒",
    "approval": "👍", "caring": "🤗", "confusion": "😕", "curiosity": "🧐",
    "desire": "😍", "disappointment": "😞", "disapproval": "👎", "disgust": "🤢",
    "embarrassment": "😳", "excitement": "🤩", "fear": "😨", "gratitude": "🙏",
    "grief": "😭", "joy": "😊", "love": "❤️", "nervousness": "😬", "optimism": "😃",
    "pride": "😌", "realization": "💡", "relief": "😮‍💨", "remorse": "😔",
    "sadness": "😢", "surprise": "😲", "neutral": "😐", "boredom": "🥱",
    "shame": "🙈", "loneliness": "😔", "anticipation": "⌛", "hope": "🌈",
    "frustration": "😤", "resentment": "😡", "trust": "🫱", "envy": "😒",
    "enthusiasm": "😄", "jealousy": "🟢", "compassion": "💞"
}

# Chatbot tone-based replies
responses = {
    "joy": "That's wonderful to hear!",
    "sadness": "I'm here for you.",
    "anger": "Take a deep breath, you're not alone.",
    "disappointment": "I'm sorry you're feeling that way.",
    "fear": "It's okay to feel scared. You're not alone.",
    "love": "Love makes everything brighter!",
    "neutral": "Thanks for sharing.",
    "surprise": "Interesting! That sounds unexpected.",
    "gratitude": "You're welcome! 😊",
    "confusion": "Let’s try to understand it together."
}

# Pydantic models
class SentimentRequest(BaseModel):
    text: str

class EmotionItem(BaseModel):
    emotion: str
    confidence: float
    emoji: str

# FastAPI Router
router = APIRouter()

# Analyze emotion from given text
def process_emotion(text: str):
    try:
        scores = sentiment_pipeline(text)[0]
        scores.sort(key=lambda x: x["score"], reverse=True)
        top3 = scores[:3]
        main = top3[0] if top3 else {"label": "neutral", "score": 0.0}
        return top3, main
    except Exception as e:
        logger.error(f"[❌] Emotion processing failed: {e}")
        raise

# Generate AI response based on main emotion
def generate_response(emotion: str) -> str:
    return responses.get(emotion.lower(), "Thanks for sharing.")

# ✅ POST route for analyzing text input
@router.post("/analyze/")
async def analyze_sentiment(input: SentimentRequest):
    try:
        top_emotions, main = process_emotion(input.text)
        lang = langid.classify(input.text)[0]
        response = generate_response(main["label"])

        return {
            "text": input.text,
            "language": lang,
            "emotion": main["label"],
            "confidence": main["score"],
            "emoji": emoji_map.get(main["label"], "❓"),
            "response": response,
            "top_emotions": [
                {
                    "emotion": e["label"],
                    "confidence": e["score"],
                    "emoji": emoji_map.get(e["label"], "❓")
                }
                for e in top_emotions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Transcribe WAV/MP3 using Whisper
def whisper_pipeline_wrapper(wav_path: str):
    try:
        result = whisper_pipeline(wav_path)
        return result["text"]
    except Exception as e:
        logger.error(f"[❌] Whisper transcription error: {e}")
        raise
