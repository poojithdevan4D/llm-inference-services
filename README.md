# Inference Service

An OpenAI-style LLM inference microservice built with **FastAPI**.
Takes a user message over HTTP and returns a model's reply.

> Project 1 of my applied-inference portfolio. Currently backed by a hosted model;
> being upgraded to serve a **local quantized model** (llama.cpp) next.

## Endpoints
- `GET /health` — service health check
- `POST /chat` — send `{"message": "..."}`, get back the model's reply

## Run locally
```bash
pip install -r requirements.txt
cp .env.example .env      # then put your real key in .env
fastapi dev app.py
```
Open http://127.0.0.1:8000/docs to try it.

## Stack
FastAPI · pydantic · httpx · (llama.cpp — coming)

## Results / notes
_(fill in: latency, what you learned, screenshots)_
