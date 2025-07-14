// frontend/src/components/Dashboard.jsx
import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeText, analyzeVoice, analyzeCamera } from "../api";
import Webcam from "react-webcam";
import "../styles/dashboard.css";

const Dashboard = () => {
  const [mode, setMode] = useState("text");
  const [inputText, setInputText] = useState("");
  const [audioFile, setAudioFile] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const handleTextSubmit = async () => {
    if (!inputText.trim()) return alert("Please enter some text.");
    try {
      const response = await analyzeText(inputText);
      navigate("/result", { state: response });
    } catch (error) {
      console.error("Text Analysis Failed", error);
    }
  };

  const handleVoiceSubmit = async () => {
    if (!audioFile) return alert("Please upload a voice file (.wav or .mp3)");
    const formData = new FormData();
    formData.append("audio", audioFile);
    try {
      const response = await analyzeVoice(formData);
      navigate("/result", { state: response });
    } catch (error) {
      console.error("Voice Analysis Failed", error);
    }
  };

  const captureImage = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
  };

const handleCameraSubmit = async () => {
  if (!capturedImage) return alert("Please capture an image first.");
  const blob = await fetch(capturedImage).then((res) => res.blob());
  const formData = new FormData();
  formData.append("image", blob, "capture.jpg");  // ✅ Corrected key
  try {
    const response = await analyzeCamera(formData);
    navigate("/result", { state: response });
  } catch (error) {
    console.error("Camera Analysis Failed", error);
  }
};

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-card">
        <h2 className="dashboard-title">Sentiverse Emotion Detector</h2>

        <div className="mode-toggle">
          <button
            className={mode === "text" ? "active" : ""}
            onClick={() => setMode("text")}
          >
            Text Input
          </button>
          <button
            className={mode === "voice" ? "active" : ""}
            onClick={() => setMode("voice")}
          >
            Voice Upload
          </button>
          <button
            className={mode === "camera" ? "active" : ""}
            onClick={() => setMode("camera")}
          >
            Camera
          </button>
        </div>

        {mode === "text" && (
          <div className="input-section">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your feelings here..."
            />
            <button onClick={handleTextSubmit}>Submit</button>
          </div>
        )}

        {mode === "voice" && (
          <div className="input-section">
            <input
              type="file"
              accept=".wav,.mp3"
              onChange={(e) => setAudioFile(e.target.files[0])}
            />
            <button onClick={handleVoiceSubmit}>Submit</button>
          </div>
        )}

        {mode === "camera" && (
          <div className="input-section camera-section">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="webcam-preview"
            />
            <button onClick={captureImage}>Capture</button>
            {capturedImage && (
              <>
                <img
                  src={capturedImage}
                  alt="Captured"
                  className="captured-preview"
                />
                <button onClick={handleCameraSubmit}>Submit</button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
