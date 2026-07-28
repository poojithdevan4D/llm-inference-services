import os
import logging                                              # NEW
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO,                     # NEW: set up logging
                    format="%(asctime)s  %(levelname)s  %(message)s")
logger = logging.getLogger("inference-service")             # NEW

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/v1/chat/completions")
MODEL = "qwen2.5:1.5b"

app = FastAPI(title="Inference Service")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")                                           # NEW: what am I serving?
def info():
    return {"model": MODEL, "backend": "ollama", "endpoint": OLLAMA_URL}

@app.post("/chat")
def chat(req: ChatRequest):
    logger.info(f"/chat request: {req.message[:60]!r}")     # NEW: log the request
    payload = {"model": MODEL, "messages": [{"role": "user", "content": req.message}]}
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=30.0)
        response.raise_for_status()
    except httpx.HTTPError:
        logger.error("Ollama unreachable")                  # NEW: log the failure
        raise HTTPException(status_code=503, detail="Model server unavailable (is Ollama running?)")
    reply = response.json()["choices"][0]["message"]["content"]
    logger.info(f"/chat reply: {len(reply)} chars")         # NEW: log the result
    return {"reply": reply}
