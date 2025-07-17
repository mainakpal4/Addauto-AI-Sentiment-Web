import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router as app_router

# ✅ Define frontend path (React build)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Sentiverse Emotion API",
    description="Backend API for Sentiverse - supports text, voice, and camera-based sentiment analysis.",
    version="1.0.0"
)

# ✅ CORS Middleware (add your production domain below when ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",         # React dev server
        "http://localhost:8000",         # Backend dev serving React
        "https://sentiverse-qqzz.vercel.app"  # 🔁 Replace with actual frontend domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static files from React build
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# ✅ Include backend API routes
app.include_router(app_router)

# ✅ React router fallback — serves index.html for all unknown routes (e.g., /register, /dashboard)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_file = os.path.join(frontend_path, "index.html")
    return FileResponse(index_file)