from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import logging
import os

# Import Agents
from .nexus_1_harvester.core import Nexus1Harvester
from .nexus_2_scout.core import Nexus2Scout
from .nexus_3_integrator.core import Nexus3Integrator
from .nexus_4_strategist.core import Nexus4Strategist
from .nexus_5_mathematician.core import Nexus5Mathematician
from .nexus_6_senior_partner.core import Nexus6SeniorPartner
from .nexus_7_architect.core import Nexus7Architect
from .nexus_8_guardian.core import Nexus8Guardian
from .nexus_8_guardian.core import Nexus8Guardian
from .nexus_8_archivist.core import Nexus8Archivist
from .nexus_9_inspector.core import Nexus9Inspector

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-GATEWAY")

app = FastAPI(title="NEXUS-360 API", version="1.0.0")

# Mount Static Files (Frontend)
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/dashboard", StaticFiles(directory=static_path, html=True), name="static")

# Request Models
class IngestRequest(BaseModel):
    source_name: str
    content_text: str

class FolderIngestRequest(BaseModel):
    folder_id: str
    access_token: Optional[str] = None
    product_description: Optional[str] = ""

class WorkflowResponse(BaseModel):
    pipeline_id: str
    final_report_url: str
    steps_completed: List[str]

@app.on_event("startup")
async def startup_event():
    logger.info("NEXUS-360 API Gateway Initialized.")

@app.get("/health")
async def health_check():
    return {"status": "online", "agents": 8}

# Endpoint to fetch latest agent activity report
from .shared.utils import LOG_PATH
import json

@app.get("/reports/latest")
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

@app.post("/workflow/folder_ingestion")
async def run_folder_workflow(request: FolderIngestRequest):
    """
    Triggers the NEXUS-360 pipeline starting from a Google Drive Folder.
    """
    try:
        # Helper to save artifacts
        import json
        
        def save_artifact(agent_name, data):
            filename = f"artifact_{agent_name}_{generate_uuid()}.json"
            filepath = os.path.join(static_path, "reports", filename)
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return f"/dashboard/reports/{filename}"

        # Import UUID generator helper locally to avoid messing with imports at top if simpler
        from uuid import uuid4 as generate_uuid

        harvester = Nexus1Harvester()
        # Pass access_token if available
        ingestion_result = await harvester.ingest_from_folder(request.folder_id, request.access_token)
        
        # Handle new dict return format
        if isinstance(ingestion_result, dict):
            ingested_ids = ingestion_result.get("ids", [])
            ingestion_mode = ingestion_result.get("mode", "UNKNOWN")
            ingestion_msg = ingestion_result.get("message", "")
        else:
             # Fallback for legacy list return
            ingested_ids = ingestion_result
            ingestion_mode = "LEGACY"
            ingestion_msg = ""
        
        if not ingested_ids:
            return {"status": "error", "message": "No files found or ingestion failed."}
        
        # Save Harvester Artifact
        harvester_url = save_artifact("harvester", {
            "ingested_ids": ingested_ids,
            "mode": ingestion_mode,
            "debug_msg": ingestion_msg
        })

        # For the prototype, we process the batch and create one report
        # In real life, this might trigger 8 instances or a consolidated analysis
        
        # 2. Guardian Validation (Batch)
        guardian = Nexus8Guardian()
        validation_results = []
        for doc_id in ingested_ids:
            res = await guardian.validate_input(doc_id, {"raw_content": "batch_processing"})
            validation_results.append({"doc_id": doc_id, "valid": res})
        guardian_url = save_artifact("guardian", validation_results)

        # 3. Continue the chain with the first doc as a representative or combine them
        # Logic: Integrator combines them
        scout = Nexus2Scout()
        # Use product_description as primary anchor if provided
        scout_input = request.product_description if request.product_description else f"Batch Analysis for Folder {request.folder_id}"
        
        # CRITICAL: Pass POE data to Scout (NO DATA INVENTION)
        poe_xray_data = ingestion_result.get("xray_data") if isinstance(ingestion_result, dict) else None
        findings = await scout.perform_osint_scan(scout_input, poe_data=poe_xray_data)
        scout_url = save_artifact("scout", findings)

        integrator = Nexus3Integrator()
        ssot = await integrator.consolidate_data(ingested_ids + [findings['id']])
        integrator_url = save_artifact("integrator", ssot)

        strategist = Nexus4Strategist()
        strategy = await strategist.analyze_gaps(ssot)
        strategist_url = save_artifact("strategist", strategy)

        math_agent = Nexus5Mathematician()
        models = await math_agent.calculate_roi_models(strategy)
        # Math agent usually doesn't output distinct large JSON but we can save models
        # (Skipping explicit artifact for math for brevity or save strictly)
        
        # 6. SENIOR PARTNER
        partner = Nexus6SeniorPartner()
        summary = await partner.synthesize_executive_summary(models, strategy)
        senior_url = save_artifact("senior_partner", summary)

        # 7. GUARDIAN COMPLIANCE AUDIT
        guardian_audit = await guardian.perform_compliance_audit(strategy)
        guardian_url = save_artifact("guardian_compliance", guardian_audit)

        # 8. ARCHITECT
        full_data = {
            "harvester": {"source": f"Carpeta Drive: {request.folder_id}", "files": len(ingested_ids)},
            "scout": findings,
            "integrator": ssot,
            "strategist": strategy,
            "mathematician": models,
            "senior_partner": summary,
            "guardian": guardian_audit
        }
        
        architect = Nexus7Architect()
        report = await architect.generate_report_artifacts(full_data)
        
        # 9. ARCHIVIST - Archive case for longitudinal studies
        archivist = Nexus8Archivist()
        archive_result = archivist.archive_case(
            case_id=report.get("pdf_url", "").split("/")[-1].replace(".html", ""),
            product_query=request.product_description or f"Drive Folder: {request.folder_id}",
            ssot=ssot,
            report_html=report.get("html_content", ""),
            verdict=strategy.get("dynamic_verdict", {}),
            metadata={"ingestion_mode": ingestion_mode, "files_count": len(ingested_ids)}
        )
        # 10. INSPECTOR (BLUEPRINT)
        inspector = Nexus9Inspector()
        blueprint_result = await inspector.generate_blueprint(full_data)
        blueprint_url = blueprint_result["blueprint_url"]
        logger.info(f"[INSPECTOR] Blueprint generated: {blueprint_url}")

        logger.info(f"[ARCHIVIST] Case archived: {archive_result.get('case_id')}")

        return {
            "folder_id": request.folder_id,
            "files_processed": len(ingested_ids),
            "ingestion_mode": ingestion_mode,
            "ingestion_msg": ingestion_msg,
            "final_report_url": report["pdf_url"],
            "archive_status": archive_result.get("status", "unknown"),
            "product_hash": archive_result.get("product_hash"),
            "artifacts": {
                "harvester": harvester_url,
                "guardian": guardian_url,
                "scout": scout_url,
                "integrator": integrator_url,
                "strategist": strategist_url,
                "strategist": strategist_url,
                "senior_partner": senior_url,
                "inspector": blueprint_url
            },
            "steps_completed": ["Multi-File Harvester", "Guardian", "Scout", "Integrator (Batch)", "Strategist", "Mathematician", "Senior Partner", "Architect", "Archivist"]
        }

    except Exception as e:
        logger.error(f"Folder Workflow Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- STEP-BY-STEP API ENDPOINTS ---

class StepRequest(BaseModel):
    prev_output: Optional[dict] = None
    context: Optional[dict] = None

@app.post("/workflow/step/1_harvester")
async def step_1_harvester(request: FolderIngestRequest):
    """Executes ONLY the Harvester Step"""
    harvester = Nexus1Harvester()
    ingestion_result = await harvester.ingest_from_folder(request.folder_id, request.access_token)
    
    # Normalize Output
    if isinstance(ingestion_result, dict):
        data = ingestion_result
    else:
        data = {"ids": ingestion_result, "mode": "LEGACY", "message": ""}
    
    return {
        "step": "harvester",
        "data": data,
        "status": "success" if data["ids"] else "warning",
        "report": {
            "input": {
                "folder_id": request.folder_id,
                "access_token": request.access_token
            },
            "action": "Ingesting files from Google Drive folder"
        }
    }

@app.post("/workflow/step/2_guardian")
async def step_2_guardian(payload: dict):
    """Executes ONLY the Guardian Step (Batch Validation)"""
    ingested_ids = payload.get("data", {}).get("ids", [])
    guardian = Nexus8Guardian()
    results = []
    for doc_id in ingested_ids:
        is_valid = await guardian.validate_input(doc_id, {"raw_content": "batch"})
        results.append({"id": doc_id, "valid": is_valid})
    
    return {"step": "guardian", "data": results, "status": "success", "report": {"input": {"ingested_ids": ingested_ids}, "action": "Validating ingested documents in batch"}}

@app.post("/workflow/step/3_scout")
async def step_3_scout(payload: dict):
    """Executes ONLY the Scout Step (OSINT) - NO DATA INVENTION"""
    logger.info("Executing Scout Step Endpoint...")
    
    filenames = payload.get("filenames") or []
    data_stats = payload.get("data_stats") or {}
    product_desc = payload.get("product_description") or ""
    folder_name = data_stats.get("folder_name", "Niche")
    
    # CRITICAL: Get POE X-Ray data from Harvester result
    xray_data = payload.get("xray_data") or {}
    
    # Priority: User Description > Folder Name + Filenames
    context_str = product_desc if product_desc else (f"{folder_name} " + " ".join(filenames))
        
    scout = Nexus2Scout()
    # MANDAMIENTO: Pass POE data - Scout NO INVENTA datos cuantitativos
    findings = await scout.perform_osint_scan(context_str, poe_data=xray_data)
    return {"step": "scout", "data": findings, "status": "success"}

@app.post("/workflow/step/4_integrator")
async def step_4_integrator(payload: dict):
    """Executes ONLY the Integrator Step"""
    logger.info("Executing Integrator Step Endpoint...")
    
    ids = payload.get("harvester_ids") or []
    filenames_override = payload.get("filenames") or []
    data_stats = payload.get("data_stats") or {}
    scout_id = payload.get("scout_id")
    
    integrator = Nexus3Integrator()
    # Ensure IDs is a list
    if not isinstance(ids, list):
        ids = [ids] if ids else []
        
    fs_ids = ids + ([scout_id] if scout_id else [])
    
    ssot = await integrator.consolidate_data(fs_ids, filenames_override, data_stats)
    return {"step": "integrator", "data": ssot, "status": "success"}

@app.post("/workflow/step/5_strategist")
async def step_5_strategist(payload: dict):
    """Executes ONLY the Strategist Step"""
    logger.info("Executing Strategist Step Endpoint...")
    ssot = payload.get("ssot_data") or {}
    strategist = Nexus4Strategist()
    strategy = await strategist.analyze_gaps(ssot)
    return {"step": "strategist", "data": strategy, "status": "success"}

@app.post("/workflow/step/6_mathematician")
async def step_6_mathematician(payload: dict):
    """Executes ONLY the Mathematician Step"""
    logger.info("Executing Mathematician Step Endpoint...")
    strategy = payload.get("strategy_data") or {}
    mathematician = Nexus5Mathematician()
    models = await mathematician.calculate_roi_models(strategy)
    return {"step": "mathematician", "data": models, "status": "success"}

@app.post("/workflow/step/7_senior_partner")
async def step_7_senior_partner(payload: dict):
    """Executes ONLY the Senior Partner Step"""
    logger.info("Executing Senior Partner Step Endpoint...")
    models = payload.get("models_data") or {}
    strategy = payload.get("strategy_data") or {}
    partner = Nexus6SeniorPartner()
    summary = await partner.synthesize_executive_summary(models, strategy)
    return {"step": "senior_partner", "data": summary, "status": "success"}

@app.post("/workflow/step/8_architect")
async def step_8_architect(payload: dict):
    """Executes ONLY the Architect Step (Final Report)"""
    logger.info("Executing Architect Step Endpoint...")
    # CRITICAL: Handle both direct and wrapped payloads
    full_data = payload.get("full_data") or payload
    
    architect = Nexus7Architect()
    report = await architect.generate_report_artifacts(full_data)
    return {"step": "architect", "data": report, "status": "success"}

@app.post("/workflow/step/9_inspector")
async def step_9_inspector(payload: dict):
    """Executes ONLY the Inspector Step (Blueprint)"""
    logger.info("Executing Inspector Step Endpoint...")
    full_data = payload.get("full_data") or payload
    
    inspector = Nexus9Inspector()
    blueprint_result = await inspector.generate_blueprint(full_data)
    return {"step": "inspector", "data": blueprint_result, "status": "success"}

# --- END STEP-BY-STEP ---

@app.post("/workflow/full_cycle", response_model=WorkflowResponse)
async def run_full_cycle(request: IngestRequest):
    """
    Triggers the complete NEXUS-360 pipeline from Ingestion to Report Generation.
    """
    try:
        # 1. HARVESTER
        harvester = Nexus1Harvester()
        input_id = harvester.ingest_mock_data(request.source_name, request.content_text)
        if not input_id:
            raise HTTPException(status_code=500, detail="Ignition Failed during Harvester step")

        # 2. GUARDIAN (Validate Input)
        guardian = Nexus8Guardian()
        # Mock payload construction
        is_valid = await guardian.validate_input(input_id, {"raw_content": request.content_text})
        if not is_valid:
             raise HTTPException(status_code=400, detail="Input Validation Failed by Guardian")

        # 3. SCOUT (Parallel Enrichment) - NO DATA INVENTION
        scout = Nexus2Scout()
        # Sin POE data = campos cuantitativos PENDIENTE
        findings = await scout.perform_osint_scan(f"Analysis for {request.source_name}", poe_data=None)

        # 4. INTEGRATOR (SSOT)
        integrator = Nexus3Integrator()
        ssot = await integrator.consolidate_data([input_id, findings['id']])

        # 5. STRATEGIST
        strategist = Nexus4Strategist()
        strategy = await strategist.analyze_gaps(ssot)

        # 6. MATHEMATICIAN
        math_agent = Nexus5Mathematician()
        models = await math_agent.calculate_roi_models(strategy)

        # 7. SENIOR PARTNER
        partner = Nexus6SeniorPartner()
        summary = await partner.synthesize_executive_summary(models, strategy)

        # 8. ARCHITECT
        full_data = {
            "harvester": {"source": request.source_name, "content": request.content_text},
            "scout": findings,
            "integrator": ssot,
            "strategist": strategy,
            "mathematician": models,
            "senior_partner": summary
        }
        
        architect = Nexus7Architect()
        report = await architect.generate_report_artifacts(full_data)

        return {
            "pipeline_id": input_id,
            "final_report_url": report["pdf_url"],
            "steps_completed": ["Harvester", "Guardian", "Scout", "Integrator", "Strategist", "Mathematician", "Senior Partner", "Architect"]
        }
    except Exception as e:
        logger.error(f"Workflow Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

