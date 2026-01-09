---
description: Report input and task performed for each agent on human intervention
---

# Overview
This workflow adds a reporting mechanism that, on every human‑initiated action, captures:
1. **The raw input** provided by the human (e.g., command, form data, API payload).
2. **The task description** of the agent that will process that input.
3. **A formatted report** displayed in the UI and logged to the system.

The implementation touches three areas:
- **Agent core** – wrap each agent’s `run` method with a decorator that records the input and the agent’s declared task.
- **Utility module** – provide a helper to format and store the report (JSON + markdown).
- **Frontend component** – a lightweight overlay that shows the latest report after each human step.

# Steps
1. **Create a logging decorator** in `agents/shared/utils.py` called `@report_agent_activity`.
   - Capture `input_data` and `self.task_description`.
   - Append a JSON entry to `reports/agent_activity.log` (create the directory if missing).
   - Return the original result.
2. **Update each agent core** (`agents/nexus_4_strategist/core.py`, `agents/nexus_7_architect/core.py`, `agents/nexus_8_guardian/core.py`, etc.) to import and apply the decorator to their main execution method.
3. **Add a UI component** (e.g., `static/report_panel.html` and accompanying JS) that reads the latest log entry via an endpoint (`/reports/latest`) and renders it in a modal.
4. **Expose an endpoint** in `agents/main.py` (FastAPI) at `/reports/latest` that returns the most recent JSON entry.
5. **Test** by performing a manual human action (e.g., clicking a button) and verify the report appears.

# Detailed Instructions
## 1. Decorator in `utils.py`
```python
import json
import os
from functools import wraps
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)
LOG_PATH = os.path.join(REPORTS_DIR, "agent_activity.log")

def report_agent_activity(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        # Assume the first positional arg is the human input payload
        input_data = args[0] if args else kwargs.get("payload")
        task_desc = getattr(self, "task_description", func.__name__)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": self.__class__.__name__,
            "task": task_desc,
            "input": input_data,
        }
        # Append to log file (one JSON per line)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        result = await func(self, *args, **kwargs)
        return result
    return wrapper
```

## 2. Apply Decorator
In each agent core file, add:
```python
from agents.shared.utils import report_agent_activity

class StrategistAgent:
    task_description = "Generate strategic plan based on user goals"

    @report_agent_activity
    async def run(self, payload):
        ...
```
Repeat for other agents.

## 3. FastAPI endpoint
Add to `agents/main.py`:
```python
from fastapi import APIRouter
import json
router = APIRouter()

@router.get("/reports/latest")
async def latest_report():
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return {"message": "No reports yet"}
            last = json.loads(lines[-1])
            return last
    except FileNotFoundError:
        return {"message": "Report file not found"}
```
Register the router as usual.

## 4. Frontend panel
Create `static/report_panel.html` with a simple container and script that fetches `/reports/latest` every time a human action completes (you can hook into existing JS events). Example snippet:
```html
<div id="agent-report" style="position:fixed;bottom:10px;right:10px;background:rgba(0,0,0,0.7);color:#fff;padding:12px;border-radius:8px;z-index:1000;max-width:300px;display:none;">
  <pre id="report-content"></pre>
</div>
<script>
async function loadReport(){
  const res = await fetch('/reports/latest');
  const data = await res.json();
  if(data.agent){
    document.getElementById('report-content').textContent = JSON.stringify(data, null, 2);
    document.getElementById('agent-report').style.display = 'block';
    setTimeout(()=>{document.getElementById('agent-report').style.display='none';},5000);
  }
}
// Hook into your existing UI event, e.g., after a form submit:
document.addEventListener('human-action-complete', loadReport);
</script>
```
Adjust the event name to match your app.

# Validation
- Run the FastAPI server.
- Perform a human‑triggered action.
- Verify a new line appears in `reports/agent_activity.log`.
- Confirm the overlay shows the correct agent, task, and input.

# Notes
- The decorator works for async `run` methods; if any agent uses sync methods, adjust accordingly.
- Keep the log file rotation simple for now; you can add a cron job later.
- Ensure the UI component respects dark/light mode for visual consistency.

---

**Result**: After following these steps, every human‑initiated step will automatically produce a clear, formatted report of the input and the task performed by the corresponding agent, visible both in the UI and in a persistent log.
