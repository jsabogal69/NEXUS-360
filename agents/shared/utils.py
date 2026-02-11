import os
import re
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import uuid

import logging

# --- CONFIGURATION ---
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger("SHARED-UTILS")
PROJECT_ID = "nexus-360-suite" 

# Robust Path Resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CRED_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", DEFAULT_CRED_PATH)

logger.info(f"[SHARED-UTILS] Resolved Credentials Path: {CREDENTIALS_PATH}")
logger.info(f"[SHARED-UTILS] CWD: {os.getcwd()}")

# --- FIREBASE INIT ---
# --- MOCK FIRESTORE FOR DEV ---
class MockDocument:
    def __init__(self, data): self.data = data; self.exists = True
    def to_dict(self): return self.data

class MockCollection:
    def __init__(self, storage, name): self.storage = storage; self.name = name
    def document(self, doc_id):
        class DocRef:
            def __init__(self, s, n, i): self.s = s; self.n = n; self.i = i
            def set(self, data): 
                if self.n not in self.s: self.s[self.n] = {}
                self.s[self.n][self.i] = data
            def update(self, data):
                if self.n not in self.s: self.s[self.n] = {}
                if self.i not in self.s[self.n]:
                     self.s[self.n][self.i] = data
                else:
                    if isinstance(self.s[self.n][self.i], dict):
                        self.s[self.n][self.i].update(data)
                    else:
                        self.s[self.n][self.i] = data
            def get(self):
                data = self.s.get(self.n, {}).get(self.i)
                return MockDocument(data) if data else type('EmptyDoc', (), {'exists': False})()
        return DocRef(self.storage, self.name, doc_id)

class MockFirestore:
    def __init__(self):
        self._storage = {}  # Instance-level: each new MockFirestore starts CLEAN
    def collection(self, name): return MockCollection(self._storage, name)

_MOCK_DB_INSTANCE = None

def clear_mock_db():
    """Reset the in-memory MockDB singleton. MUST be called at the start of every pipeline run."""
    global _MOCK_DB_INSTANCE
    if isinstance(_MOCK_DB_INSTANCE, MockFirestore):
        _MOCK_DB_INSTANCE = MockFirestore()  # Fresh instance with empty _storage
        logger.info("[MOCK-DB] 🧹 In-memory database CLEARED — fresh analysis starts now")
    # If using real Firestore, no action needed (data is isolated by document IDs)

def get_db():
    global _MOCK_DB_INSTANCE
    if _MOCK_DB_INSTANCE: return _MOCK_DB_INSTANCE

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        if not _MOCK_DB_INSTANCE:
             logger.error(f"[FIREBASE] Init Failed: {e}. Falling back to In-Memory MockDB.")
             _MOCK_DB_INSTANCE = MockFirestore()
        return _MOCK_DB_INSTANCE

# --- SHARED TYPES ---
class AgentRole(Enum):
    HARVESTER = "NEXUS-1"
    GUARDIAN = "NEXUS-8"

class ValidationStatus(Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"

def generate_id() -> str:
    return str(uuid.uuid4())

def timestamp_now():
    return datetime.utcnow()
# --- AGENT ACTIVITY REPORTING ---
import json
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)
LOG_PATH = os.path.join(REPORTS_DIR, "agent_activity.log")

import inspect

def sanitize_text_field(text: str) -> str:
    """Cleans common LLM artifacts, cutoffs, and stutters from string fields."""
    if not isinstance(text, str):
        return text
    
    s = text.strip().replace('""', '"')
    
    # Common cutoffs/stutters observed
    cutoffs = [" fall primaril", " primaril", " fall", " primarily", " lead to"]
    for cutoff in cutoffs:
        if s.endswith(cutoff):
            s = s[:-len(cutoff)].strip()
            
    # Remove hanging quotes or partial words at the very end
    s = re.sub(r'\s+[a-zA-Z]{1,2}$', '', s) 
    return s

def report_agent_activity(func):
    """Decorator to log human input and agent task description. Makes the function async."""
    async def wrapper(self, *args, **kwargs):
        input_data = args[0] if args else kwargs.get("payload")
        task_desc = getattr(self, "task_description", func.__name__)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": self.__class__.__name__,
            "task": task_desc,
            "input": input_data,
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
            
        if inspect.iscoroutinefunction(func):
            return await func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)
    return wrapper

# --- GOOGLE DRIVE INIT ---
# --- GOOGLE DRIVE INIT ---
from googleapiclient.discovery import build
from google.oauth2 import service_account

def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    logger.info(f"[DRIVE] Attempting to init Drive Service with path: {CREDENTIALS_PATH}")
    if not os.path.exists(CREDENTIALS_PATH):
        logger.warning(f"[DRIVE] Credentials file NOT FOUND at {CREDENTIALS_PATH}")
        return None
    
    try:
        cred = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES)
        service = build('drive', 'v3', credentials=cred)
        logger.info("[DRIVE] Service created successfully.")
        return service
    except Exception as e:
        logger.error(f"[DRIVE] Init Failed: {e}", exc_info=True)
        return None
