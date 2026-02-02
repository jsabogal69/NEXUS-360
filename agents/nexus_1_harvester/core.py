from ..shared.utils import get_db, generate_id, timestamp_now, AgentRole, report_agent_activity
from ..shared.data_expert import DataExpert
import logging
import io
import re

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-1")

# POE Guide Detection Keywords
POE_GUIDE_KEYWORDS = ["GUIA CONTENIDO POE", "GUIA_CONTENIDO_POE", "POE_GUIDE", "CONTENT_GUIDE", "INDICE_POE"]

class Nexus1Harvester:
    task_description = "Ingest files from a Google Drive folder using POE Content Guide as master index"
    
    def __init__(self):
        self.db = get_db()
        self.role = AgentRole.HARVESTER.value
        self.poe_guide = None  # Will hold parsed guide if found
        self.file_instructions = {}  # Per-file instructions from guide

    def ingest_mock_data(self, source_name: str, content_text: str):
        """
        Simulates ingesting a single file from Google Drive or manual input.
        """
        logger.info(f"[{self.role}] Ingesting data from {source_name}...")
        
        data_packet = {
            "id": generate_id(),
            "project_id": "default-project",
            "source": "google_drive",
            "file_name": source_name,
            "raw_content": content_text,
            "ingested_at": timestamp_now(),
            "validation_status": "pending",
            "ingested_by": self.role
        }
        
        doc_id = self._save_to_raw_inputs(data_packet)
        return doc_id

    def _detect_poe_guide(self, files: list) -> dict:
        """
        Detect if a GUIA CONTENIDO POE exists in the folder.
        Returns the file metadata if found, None otherwise.
        """
        for f in files:
            name_upper = f['name'].upper()
            for keyword in POE_GUIDE_KEYWORDS:
                if keyword in name_upper:
                    logger.info(f"[{self.role}] 📋 POE GUIDE DETECTED: {f['name']}")
                    return f
        return None

    def _parse_poe_guide(self, guide_content: str, structured_data: list = None) -> dict:
        """
        Parse the POE Content Guide to extract file instructions.
        
        Expected columns:
        - Nombre del Archivo (File Name)
        - Fuente de Datos (Data Source)
        - Tipo de Archivo (File Type)
        - Definición Funcional (Functional Definition)
        - Columnas / Datos Clave (Key Columns)
        - Instrucción para el Agente (Agent Instruction)
        """
        file_instructions = {}
        
        # If we have structured data (from CSV/Excel), use it directly
        if structured_data:
            for row in structured_data:
                # Normalize column names (handle variations)
                file_name = row.get("Nombre del Archivo", row.get("nombre_del_archivo", row.get("file_name", "")))
                if not file_name:
                    # Try to find any column that looks like a filename
                    for key, val in row.items():
                        if isinstance(val, str) and ("." in val or "_" in key.lower()):
                            file_name = val
                            break
                
                if file_name:
                    instruction = {
                        "source": row.get("Fuente de Datos", row.get("fuente", row.get("source", "Unknown"))),
                        "file_type": row.get("Tipo de Archivo", row.get("tipo", row.get("type", "Unknown"))),
                        "definition": row.get("Definición Funcional", row.get("definicion", row.get("definition", ""))),
                        "key_columns": row.get("Columnas / Datos Clave a Leer", row.get("columnas", row.get("columns", ""))),
                        "agent_instruction": row.get("Instrucción para el Agente", row.get("instruccion", row.get("instruction", "")))
                    }
                    # Match by partial filename (handle date variations)
                    file_instructions[file_name] = instruction
                    logger.info(f"[{self.role}] 📝 Guide entry: {file_name} -> {instruction.get('definition', 'N/A')[:50]}")
        
        # Also try to parse from text content (fallback)
        elif guide_content:
            lines = guide_content.strip().split('\n')
            for line in lines:
                # Try to detect table-like structure
                parts = [p.strip() for p in re.split(r'\t|,', line) if p.strip()]
                if len(parts) >= 3:
                    file_name = parts[0]
                    if "." in file_name or "_" in file_name:
                        file_instructions[file_name] = {
                            "source": parts[1] if len(parts) > 1 else "Unknown",
                            "file_type": parts[2] if len(parts) > 2 else "Unknown",
                            "definition": parts[3] if len(parts) > 3 else "",
                            "key_columns": parts[4] if len(parts) > 4 else "",
                            "agent_instruction": parts[5] if len(parts) > 5 else ""
                        }
        
        return file_instructions

    def _match_file_to_guide(self, filename: str) -> dict:
        """
        Match a filename to the POE guide entries (handles partial matches and date variations).
        """
        if not self.file_instructions:
            return None
        
        filename_upper = filename.upper()
        
        # Exact match first
        if filename in self.file_instructions:
            return self.file_instructions[filename]
        
        # Partial match (remove date patterns)
        for guide_name, instruction in self.file_instructions.items():
            guide_base = re.sub(r'_?\d{1,2}_\d{1,2}_\d{4}', '', guide_name.upper())
            file_base = re.sub(r'_?\d{1,2}_\d{1,2}_\d{4}', '', filename_upper)
            
            if guide_base and file_base and (guide_base in file_base or file_base in guide_base):
                return instruction
            
            # Also try without extension
            guide_no_ext = guide_base.rsplit('.', 1)[0] if '.' in guide_base else guide_base
            file_no_ext = file_base.rsplit('.', 1)[0] if '.' in file_base else file_base
            
            if guide_no_ext and file_no_ext and (guide_no_ext in file_no_ext or file_no_ext in guide_no_ext):
                return instruction
        
        return None

    @report_agent_activity
    async def ingest_from_folder(self, folder_id: str, access_token: str = None):
        """
        Connects to Google Drive, first looks for POE Content Guide,
        then ingests all files with context from the guide.
        """
        from ..shared.utils import get_drive_service
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        service = None
        if access_token:
            try:
                creds = Credentials(token=access_token)
                service = build('drive', 'v3', credentials=creds)
            except Exception as e:
                logger.error(f"Failed to build service from token: {e}")

        if not service:
            service = get_drive_service()
        
        if not service:
            error_msg = "AUTENTICACIÓN FALLIDA: No se proporcionó un Token de Usuario válido."
            return {"ids": [], "mode": "ERROR", "message": error_msg}

        try:
            folder_meta = service.files().get(fileId=folder_id, fields="name", supportsAllDrives=True).execute()
            folder_name = folder_meta.get('name', 'Unknown')
            
            query = f"'{folder_id}' in parents and trashed = false"
            results = service.files().list(
                q=query,
                fields="files(id, name, mimeType, size)",
                pageSize=100,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            if not files:
                return {"ids": [], "mode": "ERROR", "message": f"Carpeta '{folder_name}' está vacía."}

            # ═══════════════════════════════════════════════════════════════
            # STEP 1: DETECT AND PARSE POE CONTENT GUIDE
            # ═══════════════════════════════════════════════════════════════
            poe_guide_file = self._detect_poe_guide(files)
            poe_guide_summary = None
            
            if poe_guide_file:
                try:
                    f_id = poe_guide_file['id']
                    mime = poe_guide_file['mimeType']
                    
                    # Download and parse the guide
                    if "google-apps.spreadsheet" in mime:
                        export_request = service.files().export_media(fileId=f_id, mimeType='text/csv')
                        file_bytes = export_request.execute()
                        df = DataExpert.process_csv(file_bytes)
                        guide_content = df.to_string()
                        structured_guide = df.to_dict(orient='records')
                    elif "csv" in mime:
                        request = service.files().get_media(fileId=f_id)
                        file_bytes = request.execute()
                        df = DataExpert.process_csv(file_bytes)
                        guide_content = df.to_string()
                        structured_guide = df.to_dict(orient='records')
                    elif "spreadsheet" in mime or "excel" in mime:
                        request = service.files().get_media(fileId=f_id)
                        file_bytes = request.execute()
                        df = DataExpert.process_excel(file_bytes)
                        guide_content = df.to_string()
                        structured_guide = df.to_dict(orient='records')
                    else:
                        request = service.files().get_media(fileId=f_id)
                        file_bytes = request.execute()
                        guide_content = file_bytes.decode('utf-8', errors='ignore')
                        structured_guide = None
                    
                    # Parse the guide
                    self.file_instructions = self._parse_poe_guide(guide_content, structured_guide)
                    
                    poe_guide_summary = {
                        "detected": True,
                        "file_name": poe_guide_file['name'],
                        "entries_count": len(self.file_instructions),
                        "files_indexed": list(self.file_instructions.keys())
                    }
                    
                    logger.info(f"[{self.role}] ✅ POE GUIDE PARSED: {len(self.file_instructions)} file instructions loaded")
                    
                except Exception as ex:
                    logger.warning(f"[{self.role}] ⚠️ Failed to parse POE Guide: {ex}")
                    poe_guide_summary = {"detected": True, "error": str(ex)}
            else:
                logger.info(f"[{self.role}] ℹ️ No POE Content Guide found. Using default extraction.")
                poe_guide_summary = {"detected": False}

            # ═══════════════════════════════════════════════════════════════
            # STEP 2: INGEST ALL FILES WITH GUIDE CONTEXT
            # ═══════════════════════════════════════════════════════════════
            ingested_ids = []
            filenames = []
            file_lineage = {}
            
            for f in files:
                # Skip the guide file itself (we already processed it)
                if poe_guide_file and f['id'] == poe_guide_file['id']:
                    continue
                    
                filenames.append(f['name'])
                f_id = f['id']
                mime = f['mimeType']
                
                # Get instructions from POE Guide if available
                guide_instruction = self._match_file_to_guide(f['name'])
                
                if guide_instruction:
                    logger.info(f"[{self.role}] 📖 {f['name']} -> [{guide_instruction.get('definition', 'N/A')[:30]}]")
                else:
                    logger.info(f"[{self.role}] Processing: {f['name']} (no guide entry)")
                
                # --- EXPERT DOWNLOAD & EXTRACTION ---
                extracted_content = ""
                structured_data = None
                
                try:
                    # Download content
                    if "google-apps.spreadsheet" in mime:
                        export_request = service.files().export_media(fileId=f_id, mimeType='text/csv')
                        file_bytes = export_request.execute()
                        df = DataExpert.process_csv(file_bytes)
                        extracted_content = df.head(50).to_string()
                        structured_data = df.to_dict(orient='records')
                    else:
                        request = service.files().get_media(fileId=f_id)
                        file_bytes = request.execute()
                        
                        if "csv" in mime:
                            df = DataExpert.process_csv(file_bytes)
                            extracted_content = df.head(50).to_string()
                            structured_data = df.to_dict(orient='records')
                        elif "spreadsheet" in mime or "excel" in mime:
                            df = DataExpert.process_excel(file_bytes)
                            extracted_content = df.head(50).to_string()
                            structured_data = df.to_dict(orient='records')
                        elif "pdf" in mime:
                            extracted_content = DataExpert.process_pdf(file_bytes)
                        elif "word" in mime or "officedocument.wordprocessingml" in mime:
                            extracted_content = DataExpert.process_docx(file_bytes)
                        elif "image" in mime:
                            extracted_content = f"[IMAGE ASSET] {f['name']} - Ready for Vision Analysis"
                        elif "presentation" in mime or "powerpoint" in mime:
                            extracted_content = f"[PRESENTATION] {f['name']} - Visual reference for competitor analysis"
                        else:
                            extracted_content = file_bytes.decode('utf-8', errors='ignore')[:5000]
                except Exception as ex:
                    logger.warning(f"Failed expert extraction for {f['name']}: {ex}")
                    extracted_content = f"Error in expert extraction. Raw metadata: {f['name']}"

                # ═══════════════════════════════════════════════════════════════
                # X-RAY / HELIUM10 PRICE EXTRACTION (POE REAL DATA)
                # ═══════════════════════════════════════════════════════════════
                xray_pricing = None
                search_terms_data = None
                
                try:
                    if structured_data:
                        # Convert structured_data back to DataFrame for extraction
                        import pandas as pd
                        df_temp = pd.DataFrame(structured_data)
                        
                        # 1. Try X-Ray
                        if DataExpert.is_xray_file(f['name'], df_temp):
                            xray_pricing = DataExpert.extract_xray_pricing(df_temp, f['name'])
                            if xray_pricing.get("has_real_data"):
                                logger.info(f"[{self.role}] 💰 X-RAY PRICING EXTRACTED: {xray_pricing['total_products']} products")
                        
                        # 2. Try Search Terms
                        if DataExpert.is_search_terms_file(f['name'], df_temp):
                            search_terms_data = DataExpert.extract_search_terms_data(df_temp, f['name'])
                            if search_terms_data.get("has_search_data"):
                                logger.info(f"[{self.role}] 🔍 SEARCH TERMS EXTRACTED: Vol {search_terms_data['total_search_volume']}")

                except Exception as ex:
                    logger.warning(f"[{self.role}] extraction error: {ex}")

                # Build lineage with guide context
                file_lineage[f['name']] = {
                    "id": f['id'],
                    "type": mime.split('/')[-1],
                    "size_kb": round(int(f.get('size', 0))/1024, 1),
                    "is_structured": structured_data is not None,
                    "is_xray": xray_pricing.get("has_real_data", False) if xray_pricing else False,
                    "is_search_terms": search_terms_data.get("has_search_data", False) if search_terms_data else False,
                    # POE Guide context
                    "poe_source": guide_instruction.get("source") if guide_instruction else None,
                    "poe_definition": guide_instruction.get("definition") if guide_instruction else None,
                    "poe_key_columns": guide_instruction.get("key_columns") if guide_instruction else None,
                    "poe_agent_instruction": guide_instruction.get("agent_instruction") if guide_instruction else None
                }
                
                data_packet = {
                    "id": generate_id(),
                    "file_id": f_id,
                    "file_name": f['name'],
                    "mime_type": mime,
                    "raw_content": extracted_content,
                    "structured_data": structured_data,
                    "ingested_at": timestamp_now(),
                    "validation_status": "pending",
                    "ingested_by": self.role,
                    "folder_id": folder_id,  # CRITICAL: Track source folder for isolation
                    # Include POE context for downstream agents
                    "poe_context": guide_instruction if guide_instruction else None,
                    # X-Ray pricing data (POE REAL DATA)
                    "xray_pricing": xray_pricing if xray_pricing and xray_pricing.get("has_real_data") else None,
                    # Search Terms data (POE REAL DATA)
                    "search_terms_data": search_terms_data if search_terms_data and search_terms_data.get("has_search_data") else None
                }
                doc_id = self._save_to_raw_inputs(data_packet)
                if doc_id:
                    ingested_ids.append(doc_id)
            
            # Aggregate X-Ray data from all files
            aggregated_xray = {"has_real_data": False, "products": [], "source_files": []}
            aggregated_search = {"has_real_data": False, "total_volume": 0, "avg_conversion": 0, "source_files": []}
            
            for f_name, lineage in file_lineage.items():
                if lineage.get("is_xray"):
                    aggregated_xray["has_real_data"] = True
                    aggregated_xray["source_files"].append(f_name)
                if lineage.get("is_search_terms"):
                    aggregated_search["has_real_data"] = True
                    aggregated_search["source_files"].append(f_name)
            
            return {
                "ids": ingested_ids,
                "filenames": filenames,
                "mode": "REAL_DRIVE",
                "message": f"Ingesta Experta de {len(files)} archivos completada.",
                "poe_guide": poe_guide_summary,
                "xray_data": aggregated_xray,
                "search_data": aggregated_search,
                "data_stats": {
                    "total_files": len(files),
                    "folder_name": folder_name,
                    "lineage": file_lineage,
                    "files_with_poe_context": sum(1 for v in file_lineage.values() if v.get("poe_source")),
                    "files_with_xray_pricing": sum(1 for v in file_lineage.values() if v.get("is_xray")),
                    "files_with_search_terms": sum(1 for v in file_lineage.values() if v.get("is_search_terms")),
                    "confidence_manifesto": {
                        "🟢 POE": "Datos reales de archivos Amazon (X-Ray/H10/Search Terms)",
                        "🟡 ESTIMADO": "Cálculo derivado o análisis de IA",
                        "🔴 PENDIENTE": "Sin fuente de datos verificada"
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"[{self.role}] Folder Ingestion Failed: {e}")
            return {"ids": [], "mode": "ERROR", "message": f"Fallo al acceder a Drive: {str(e)}"}

    def _save_to_raw_inputs(self, data: dict) -> str:
        if not self.db: return data["id"]
        try:
            self.db.collection("raw_inputs").document(data["id"]).set(data)
            return data["id"]
        except: return None

