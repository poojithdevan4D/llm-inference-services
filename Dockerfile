# Start from a clean, small Python image (note: 3.12, not your 3.14 — the container is isolated)
FROM python:3.12-slim

# Everything runs inside /app in the container
WORKDIR /app

# Install dependencies first (this layer is cached unless requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app in
COPY app.py .

# The service listens on port 8000
EXPOSE 8000

# Run the server with uvicorn, bound to 0.0.0.0 so it's reachable from outside the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
