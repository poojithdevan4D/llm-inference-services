import os
import logging
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s  %(message)s")
logger = logging.getLogger("inference-service")

# --- config (all from env, so the SAME code runs local-GPU or cloud) ---
# local default = Ollama on your machine; override for a hosted backend (e.g. Groq)
MODEL_URL = os.environ.get("MODEL_URL", "http://localhost:11434/v1/chat/completions")
MODEL = os.environ.get("MODEL", "qwen2.5:1.5b")
API_KEY = os.environ.get("API_KEY", "")        # optional; hosted backends (Groq) need this


def auth_headers():
    """Send an Authorization header only if an API key is configured."""
    return {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}


app = FastAPI(title="Inference Service")


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info():
    return {"model": MODEL, "endpoint": MODEL_URL, "uses_auth": bool(API_KEY)}


@app.post("/chat")
def chat(req: ChatRequest):
    logger.info(f"/chat request: {req.message[:60]!r}")
    payload = {"model": MODEL, "messages": [{"role": "user", "content": req.message}]}
    try:
        response = httpx.post(MODEL_URL, json=payload, headers=auth_headers(), timeout=60.0)
        response.raise_for_status()
    except httpx.HTTPError:
        logger.error("model backend unreachable")
        raise HTTPException(status_code=503, detail="Model backend unavailable")
    reply = response.json()["choices"][0]["message"]["content"]
    logger.info(f"/chat reply: {len(reply)} chars")
    return {"reply": reply}
