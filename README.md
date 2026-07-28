# LLM Inference Service

An **OpenAI-compatible LLM inference microservice** (FastAPI + Docker). The *same code* serves
either a **local quantized model** on a 4 GB GPU (via Ollama) or a **hosted model** (Groq) in the
cloud — the backend is chosen entirely by environment config.

🔗 **Live demo:** https://llm-inference-services.onrender.com/docs

Built from scratch to learn applied inference engineering: serving models behind an API,
containerization, cloud deployment, and the OpenAI-compatible standard that makes backends swappable.

## Architecture
```
Client ──HTTP──▶ FastAPI service ──HTTP──▶ model backend
                 (this repo)               ├─ local:  Ollama → Qwen2.5-1.5B on RTX 3050 (4 GB)
                                           └─ cloud:  Groq  → Llama-3.3-70B
```
Both backends speak the OpenAI-compatible API, so switching between "my GPU" and "the cloud" is a
single env var — no code change. `MODEL_URL`, `MODEL`, and `API_KEY` drive everything.

## Endpoints
- `GET /health` — liveness → `{"status": "ok"}`
- `GET /info` — active model + backend
- `POST /chat` — `{"message": "..."}` → `{"reply": "..."}`

## Measurements (live, Groq-backed, Render free tier)
| Metric | Value |
|---|---|
| `/health` latency (warm) | ~0.35 s |
| `/chat` latency (warm) | ~0.9–1.1 s end-to-end |
| Cold start (after ~15 min idle) | ~30–60 s (free tier spins down) |
| Memory footprint | thin proxy — small (see Render metrics) |

*`/chat` latency is dominated by network hops (client → Render → Groq → back), not raw generation.*

## Run locally (your own GPU)
```bash
ollama pull qwen2.5:1.5b
pip install -r requirements.txt
fastapi dev app.py            # → http://127.0.0.1:8000/docs
```

## Run in Docker (local model)
```bash
docker build -t inference-service .
docker run --rm -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  -e MODEL_URL=http://host.docker.internal:11434/v1/chat/completions \
  inference-service
```

## Deploy (cloud, Groq-backed)
Set env vars and deploy the Docker image to any host (Render free tier used here):
```
MODEL_URL = https://api.groq.com/openai/v1/chat/completions
MODEL     = llama-3.3-70b-versatile
API_KEY   = <your Groq key>
```

## Features
- One codebase runs a **local GPU model** or a **cloud model** (OpenAI-compatible backend swap)
- **Containerized** (Docker) and **deployed** to a public URL
- Structured logging + graceful error handling (clean `503` on backend failure)
- Auto-generated interactive API docs (`/docs`)

## Stack
FastAPI · pydantic · httpx · Docker · Ollama · Groq

## Notes / what I learned
Built while learning applied inference engineering. Key takeaways: the OpenAI-compatible API as a
backend-swap layer; container↔host networking (why `localhost` inside a container isn't the host);
and honest debugging — a single "model unavailable" error that turned out to be **three stacked bugs**
(hardcoded URL, wrong Ollama bind address, a broken run command).
