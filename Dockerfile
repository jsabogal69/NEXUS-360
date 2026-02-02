# Base Image
FROM python:3.9-slim

# Working Directory
WORKDIR /app

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Code
COPY agents/ ./agents/
COPY nexus-rules.md .

# Expose Port (Optional, Cloud Run ignores this but good for local)
EXPOSE 8080

# Start Command
CMD ["sh", "-c", "uvicorn agents.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
