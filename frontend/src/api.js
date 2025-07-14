// frontend/src/api.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // ✅ Update if backend URL changes

// ✅ Voice emotion analysis using uploaded audio (.wav or .mp3)
export const analyzeVoice = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze/voice/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("❌ Voice Analysis Error:", error);
    throw error;
  }
};

// ✅ Text emotion analysis
export const analyzeText = async (text) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze/`, { text });
    return response.data;
  } catch (error) {
    console.error("❌ Text Analysis Error:", error);
    throw error;
  }
};

// ✅ frontend/src/api.js
export const analyzeCamera = async (formData) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/analyze/camera/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("❌ Camera Analysis Error:", error);
    throw error;
  }
};

