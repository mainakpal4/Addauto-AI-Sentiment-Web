from transformers import pipeline
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os

sentiment_pipeline = pipeline(
    "text-classification",
    model="joeddav/distilbert-base-uncased-go-emotions-student",
    top_k=None
)

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

responses = {
    "joy": "That's wonderful to hear!",
    "sadness": "I'm here for you.",
    "anger": "Take a deep breath, you're not alone.",
    "neutral": "Thanks for sharing."
}

def process_emotion(text):
    scores = sentiment_pipeline(text)[0]
    top = [e for e in scores if e["score"] >= 0.1]
    top.sort(key=lambda x: x["score"], reverse=True)
    return top, top[0] if top else {"label": "neutral", "score": 0.0}

def generate_response(emotion):
    return responses.get(emotion.lower(), "Thanks for sharing.")

def text_to_speech(text, path):
    tts = gTTS(text=text, lang="en")
    tts.save(path)
    return path

def transcribe_audio(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio_file.file.read())
    r = sr.Recognizer()
    try:
        with sr.AudioFile(temp.name) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
    finally:
        os.unlink(temp.name)
    return text
