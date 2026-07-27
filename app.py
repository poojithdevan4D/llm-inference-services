import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

# --- config: read the key from the environment, fail loudly if it's missing ---
API_KEY = os.environ.get("GROQ_API_KEY", "")
if not API_KEY:
    raise SystemExit("GROQ_API_KEY is not set.  Run:  export GROQ_API_KEY='your_key'")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# --- the app ---
app = FastAPI(title="Inference Service")


# --- request schema: a /chat request MUST contain a string called "message" ---
class ChatRequest(BaseModel):
    message: str


# --- health check: a simple "am I alive?" endpoint every service has ---
@app.get("/health")
def health():
    return {"status": "ok"}


# --- chat: take a user message, ask the model, return the reply ---
@app.post("/chat")
def chat(req: ChatRequest):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": req.message}],
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = httpx.post(GROQ_URL, json=payload, headers=headers, timeout=30.0)
    data = response.json()
    reply = data["choices"][0]["message"]["content"]

    return {"reply": reply}
