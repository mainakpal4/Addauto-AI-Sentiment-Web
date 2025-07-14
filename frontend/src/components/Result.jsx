import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Bar } from "react-chartjs-2";
import "../styles/result.css";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);



const Result = () => {
  const location = useLocation();
  const data = location.state;
  const [isDarkMode, setIsDarkMode] = useState(true);

  useEffect(() => {
    document.body.classList.add("theme-transition");
    setTimeout(() => {
      document.body.classList.remove("theme-transition");
    }, 1000);
  }, [isDarkMode]);

  const chartData = {
    labels: data?.top_emotions?.map((e) => e.emotion.toUpperCase()) || [],
    datasets: [
      {
        label: "Confidence (%)",
        data: data?.top_emotions?.map((e) =>
          parseFloat((e.confidence * 100).toFixed(2))
        ),
        backgroundColor: ["#ff4d4d", "#4da6ff", "#ffd11a"],
        borderRadius: 8,
        barThickness: 50,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
    },
    scales: {
      x: {
        ticks: {
          color: isDarkMode ? "#ffffff" : "#222222",
          font: {
            size: 14,
            weight: "bold",
          },
        },
      },
      y: {
        ticks: {
          color: isDarkMode ? "#ffffff" : "#222222",
          callback: (val) => `${val}%`,
        },
        grid: {
          color: isDarkMode ? "#555" : "#ccc",
        },
      },
    },
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: isDarkMode
          ? "linear-gradient(to right, #0f2027, #203a43, #2c5364)"
          : "linear-gradient(to right,rgb(101, 19, 19), #ebedee)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        transition: "background 1s ease",
        padding: "20px",
      }}
    >
      <div
        style={{
          background: isDarkMode
            ? "rgba(0,0,0,0.65)"
            : "rgba(255,255,255,0.8)",
          borderRadius: "20px",
          backdropFilter: "blur(14px)",
          WebkitBackdropFilter: "blur(14px)",
          padding: "35px",
          width: "95%",
          maxWidth: "850px",
          maxHeight: "90vh",
          overflowY: "auto",
          border: `2px solid ${
            isDarkMode ? "rgba(0, 255, 255, 0.4)" : "rgba(62, 27, 78, 0.2)"
          }`,
          boxShadow: "0 0 30px rgba(0,255,255,0.3)",
          color: isDarkMode ? "#f1f1f1" : "#222222",
          textAlign: "center",
          animation: "fadeIn 1s ease-in-out",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "15px",
          }}
        >
          <h2
            style={{
              fontSize: "24px",
              fontWeight: "bold",
              color: "#00f5ff",
            }}
          >
            📩 YOU SUBMITTED:
          </h2>
          <label style={{ fontSize: "14px", color: "#fff" }}>
            <span role="img" aria-label="sun">🌞</span> Light Mode
            <input
              type="checkbox"
              checked={!isDarkMode}
              onChange={() => setIsDarkMode((prev) => !prev)}
              style={{ marginLeft: "8px" }}
            />
          </label>
        </div>

        {data?.text ? (
          <p
            style={{
              fontSize: "20px",
              marginTop: "10px",
              marginBottom: "25px",
              wordWrap: "break-word",
              color: "#eeeeee",
            }}
          >
            "{data.text}"
          </p>
        ) : (
          <p
            style={{
              fontSize: "20px",
              marginTop: "10px",
              marginBottom: "25px",
              color: "#aaa",
              fontStyle: "italic",
            }}
          >
            (Input was from voice or camera)
          </p>
        )}

        <h3 style={{ fontSize: "20px", color: "#ff9aa2", marginBottom: "8px" }}>
          🧠 DETECTED EMOTION:
        </h3>
        <p
          style={{
            fontSize: "28px",
            fontWeight: "bold",
            color: "#ff4da6",
            marginBottom: "25px",
          }}
        >
          {data?.emotion?.toUpperCase()}{" "}
          <span
            style={{
              fontSize: "36px",
              animation: "fadeIn 1s ease-in",
            }}
          >
            {data?.emoji}
          </span>
        </p>

        <h3
          style={{ fontSize: "18px", color: "#ffc3a0", marginBottom: "5px" }}
        >
          🔍 CONFIDENCE:
        </h3>
        <p
          style={{
            fontSize: "22px",
            fontWeight: "bold",
            color: isDarkMode ? "#f6e58d" : "#e17055",
            marginBottom: "25px",
          }}
        >
          {(data?.confidence * 100).toFixed(2)}%
        </p>

        <h3
          style={{ fontSize: "18px", color: "#fbc531", marginBottom: "5px" }}
        >
          💬 AI RESPONSE:
        </h3>
        <p
          style={{
            fontStyle: "italic",
            color: isDarkMode ? "#dcdde1" : "#444",
            marginBottom: "35px",
          }}
        >
          {data?.response}
        </p>

        <h3
          style={{
            fontSize: "20px",
            color: "#6effe8",
            marginBottom: "20px",
          }}
        >
          📊 TOP 3 EMOTIONS:
        </h3>
        <Bar data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

export default Result;