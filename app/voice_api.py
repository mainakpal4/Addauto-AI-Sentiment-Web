import os
import uuid
import whisper
import subprocess
from fastapi import UploadFile
from app.sentiment_api import analyze_sentiment
from app.schemas import SentimentRequest

# Load Whisper model
whisper_model = whisper.load_model("base")

async def analyze_voice(audio: UploadFile):
    # Generate unique file names
    temp_id = str(uuid.uuid4())
    webm_path = f"temp_{temp_id}.webm"
    wav_path = f"temp_{temp_id}.wav"

    # Save uploaded file to .webm
    with open(webm_path, "wb") as f:
        content = await audio.read()
        f.write(content)

    # # Convert to .wav using FFmpeg
    # ffmpeg_cmd = [
    #     "ffmpeg", "-y", "-i", webm_path,
    #     "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path
    # ]

    # Convert to .wav using FFmpeg
    ffmpeg_cmd = [
        r"D:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",  # full path to ffmpeg.exe
        "-y", "-i", webm_path,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",wav_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Transcribe audio to text
        result = whisper_model.transcribe(wav_path)
        text = result.get("text", "").strip()

        if not text:
            return {"error": "No speech detected in the audio file."}

        # Perform sentiment analysis on transcribed text
        input_data = SentimentRequest(text=text)
        return await analyze_sentiment(input_data)

    finally:
        # Cleanup
        if os.path.exists(webm_path):
            os.remove(webm_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
