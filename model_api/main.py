from fastapi import FastAPI
from transformers import pipeline
from model_api.schemas import RequestText
from datetime import datetime
import langid

# -------------------------------
# 🔤 Language Code → Name Mapping
# -------------------------------
lang_code_to_name = {
    "en": "English", "hi": "Hindi", "bn": "Bengali", "es": "Spanish",
    "fr": "French", "de": "German", "ru": "Russian", "zh": "Chinese",
    "ar": "Arabic", "pt": "Portuguese", "id": "Indonesian", "ja": "Japanese",
    "ko": "Korean", "unknown": "Unknown"
}

# -------------------
# 😊 Emoji per Emotion
# -------------------
emoji_map = {
    "joy": "😊",
    "sadness": "😢",
    "anger": "😠",
    "neutral": "😐",
    "disappointment": "😞",  # ✅ added
    "surprise": "😲",
    "fear": "😨",
    "love": "❤️",
    "approval": "👍",
    "disapproval": "👎",
    "realization": "💡",
    "remorse": "😔",
    "grief": "😭",
    "confusion": "😕",
    "desire": "😍",
    "curiosity": "🤔",
    "nervousness": "😬",
    "annoyance": "😒",
    "embarrassment": "😳",
    "pride": "😌"
}

def get_emoji(emotion: str) -> str:
    return emoji_map.get(emotion.lower(), "❓")

# ---------------------
# 🚀 Initialize FastAPI
# ---------------------
app = FastAPI()

# -----------------------------
# 🤖 Load GoEmotions HF Model
# -----------------------------
sentiment_pipeline = pipeline(
    "text-classification",
    model="joeddav/distilbert-base-uncased-go-emotions-student",
    top_k=None
)

# -----------------------------
# 📥 Endpoint for Emotion Analysis
# -----------------------------
@app.post("/analyze/")
def analyze(req: RequestText):
    raw_scores = sentiment_pipeline(req.text)[0]
    threshold = 0.1

    # 🎯 Filter top emotions
    top_emotions = [
        {
            "emotion": item["label"],
            "confidence": round(item["score"], 3),
            "emoji": get_emoji(item["label"])
        }
        for item in raw_scores if item["score"] >= threshold
    ]

    # 🔽 Sort by confidence
    top_emotions.sort(key=lambda x: x["confidence"], reverse=True)

    # ⭐ Main emotion
    main_emotion = top_emotions[0] if top_emotions else {
        "emotion": "neutral", "confidence": 0.0, "emoji": get_emoji("neutral")
    }

    # 🌐 Language detection (langid + full name)
    # 🌐 Language detection with fallback for short or unidentifiable text
    try:
        if len(req.text.strip()) < 25:
            language = "English"
        else:
            code, _ = langid.classify(req.text)
            language = lang_code_to_name.get(code, "Unknown")
    except:
        language = "Unknown"

    # ✅ Final API response
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "text": req.text,
        "language": language,
        "emotion": main_emotion["emotion"],
        "confidence": main_emotion["confidence"],
        "emoji": main_emotion["emoji"],
        "top_emotions": top_emotions
    }
