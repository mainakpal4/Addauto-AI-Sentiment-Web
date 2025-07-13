from pydantic import BaseModel
from typing import List

# ✅ Define request schema for incoming text
class SentimentRequest(BaseModel):
    text: str

# ✅ Each emotion item in top_emotions
class EmotionItem(BaseModel):
    emotion: str
    confidence: float
    emoji: str

# ✅ Response schema for the sentiment API
class EmotionResponse(BaseModel):
    text: str
    language: str
    emotion: str
    confidence: float
    emoji: str
    response: str
    top_emotions: List[EmotionItem]
