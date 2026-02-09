#!/bin/bash

# Nexus-360 Local Launcher
# Starts the backend server locally. The frontend is served at /dashboard/

echo "🚀 Starting Nexus-360 Locally..."

# 1. Activate Virtual Environment (if exists)
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Activated virtual environment."
else
    echo "⚠️ 'venv' directory not found. Trying global python..."
fi

# 2. Check Dependencies
if ! pip show fastapi &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# 3. Start Server
echo "✅ Server starting..."
echo "👉 Application URL: http://127.0.0.1:8000/dashboard/"
echo "   (Press Ctrl+C to stop)"

# Force load .env variables
export $(grep -v '^#' .env | xargs)

# Run uvicorn with hot reload
# Using nohup to prevent Hangup if terminal closes, but normally direct run is fine for local
uvicorn agents.main:app --reload --host 127.0.0.1 --port 8000
