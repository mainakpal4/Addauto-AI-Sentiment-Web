# app/camera_utils/deepface_camera.py

import cv2
import numpy as np
from deepface import DeepFace
from fastapi import UploadFile
from typing import Dict

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

async def analyze_camera_emotion(image: UploadFile) -> Dict:
    try:
        contents = await image.read()
        np_arr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # ✅ Only set detector_backend or enforce_detection
        result = DeepFace.analyze(
            frame,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv" 
        )

        emotions = result[0]["emotion"]
        dominant = result[0]["dominant_emotion"]

        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]

        top_emotions = [{
            "emotion": e,
            "confidence": float(c) / 100,
            "emoji": emoji_map.get(e, "")
        } for e, c in sorted_emotions]

        return {
            "text": "[Facial Input]",
            "emotion": dominant,
            "confidence": float(emotions[dominant]) / 100,
            "emoji": emoji_map.get(dominant, ""),
            "response": f"You seem to be {dominant}. Stay expressive!",
            "top_emotions": top_emotions
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"Emotion analysis failed: {str(e)}")
