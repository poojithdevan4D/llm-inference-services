# LLM Inference Service

A small **OpenAI-compatible LLM inference microservice** built with **FastAPI**, serving a
**local quantized model** (Qwen2.5-1.5B) through **Ollama** on a 4 GB RTX 3050.

Takes a user message over HTTP, runs it through a locally-hosted model, and returns the reply —
with request logging and graceful error handling.

## Architecture
```
  Client ──HTTP──▶  FastAPI service  ──HTTP──▶  Ollama (local model server)  ──▶  Qwen2.5-1.5B on GPU
                    (this repo)                  OpenAI-compatible endpoint
```
The service is **backend-agnostic**: because both Ollama and hosted APIs (Groq, etc.) speak the
OpenAI-compatible format, the model backend can be swapped by changing one URL.

## Endpoints
- `GET /health` — liveness check → `{"status": "ok"}`
- `GET /info` — which model / backend is being served
- `POST /chat` — send `{"message": "..."}`, get back `{"reply": "..."}`

## Run locally
```bash
# 1. serve a local model
ollama pull qwen2.5:1.5b

# 2. run the service
pip install -r requirements.txt
fastapi dev app.py

# 3. open the interactive docs
#    http://127.0.0.1:8000/docs
```

## Features
- Local model inference on a consumer GPU (4 GB)
- Structured request / error logging
- Graceful failure handling (clean 503 if the model server is down)
- Auto-generated interactive API docs (FastAPI `/docs`)

## Stack
FastAPI · pydantic · httpx · Ollama · Qwen2.5-1.5B (GGUF)
