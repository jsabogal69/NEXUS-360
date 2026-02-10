# NEXUS-360 Backend Instructions

## Overview
The NEXUS-360 backend is a multi-agent BI system built with Python and FastAPI. It currently runs in a prototype mode with mocked Firebase persistence (due to missing credentials).

## Prerequisites
- Python 3.9+
- `pip`

## Installation
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn firebase-admin google-cloud-firestore google-cloud-storage
   ```

## Running the System

### Option 1: Full Pipeline Test (Script)
Run the integration test script to see all 8 agents interact sequentially.
```bash
python3 test_pipeline.py
```

### Option 2: API Gateway (Server)
Start the FastAPI orchestrator.
```bash
python3 -m uvicorn agents.main:app --reload
```
**Endpoints:**
- `GET /health`: Check system status.
- `POST /workflow/full_cycle`: Trigger the full intelligence pipeline.

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/workflow/full_cycle" \
     -H "Content-Type: application/json" \
     -d '{"source_name": "Q3_Report.pdf", "content_text": "Revenue: 10M..."}'
```

## Project Structure
- `agents/`: Source code for all agents.
  - `nexus_1_harvester`: Ingestion.
  - `nexus_10_guardian`: Validation.
  - ... (and so on)
- `nexus-rules.md`: Operational protocols.

## Known Issues
- **Dashboard**: The Next.js dashboard could not be initialized due to missing Node.js in the environment.
- **Persistence**: Data is currently mocked or logged to console if `serviceAccountKey.json` is missing.
- **OAuth Error**: If you see `Error 400: redirect_uri_mismatch`, ensure you are accessing the dashboard via `http://localhost:8000/dashboard/` and NOT `http://127.0.0.1:8000/...`.
