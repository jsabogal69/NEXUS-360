from ..shared.utils import get_db, generate_id, timestamp_now, AgentRole, report_agent_activity
from ..shared.data_expert import DataExpert
import logging
import io

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-1")

class Nexus1Harvester:
    task_description = "Ingest files from a Google Drive folder (or mock data)"
    def __init__(self):
        self.db = get_db()
        self.role = AgentRole.HARVESTER.value

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

    @report_agent_activity
    async def ingest_from_folder(self, folder_id: str, access_token: str = None):
        """
        Connects to Google Drive, lists all files in a folder, and ingests them.
        Extracts specific data points (Lineage) per file.
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

            ingested_ids = []
            filenames = []
            file_lineage = {} # Track WHAT we access in each file
            
            for f in files:
                filenames.append(f['name'])
                f_id = f['id']
                mime = f['mimeType']
                
                logger.info(f"[{self.role}] Expertise Processing: {f['name']} ({mime})")
                
                # --- EXPERT DOWNLOAD & EXTRACTION ---
                extracted_content = ""
                structured_data = None
                
                try:
                    # Download content
                    request = service.files().get_media(fileId=f_id)
                    file_bytes = request.execute()
                    
                    if "csv" in mime:
                        df = DataExpert.process_csv(file_bytes)
                        extracted_content = df.head(50).to_string() # Summary for LLM
                        structured_data = df.to_dict(orient='records')
                    elif "spreadsheet" in mime or "excel" in mime:
                        # For Google Sheets, we must export to PDF or CSV first if using get_media on non-binary
                        # But for actual xlsx files uploaded to Drive, get_media works.
                        # If it's a native GDoc, we handle it separately
                        if "google-apps.spreadsheet" in mime:
                            export_request = service.files().export_media(fileId=f_id, mimeType='text/csv')
                            file_bytes = export_request.execute()
                            df = DataExpert.process_csv(file_bytes)
                            extracted_content = df.head(50).to_string()
                            structured_data = df.to_dict(orient='records')
                        else:
                            df = DataExpert.process_excel(file_bytes)
                            extracted_content = df.head(50).to_string()
                            structured_data = df.to_dict(orient='records')
                    elif "pdf" in mime:
                        extracted_content = DataExpert.process_pdf(file_bytes)
                    elif "word" in mime or "officedocument.wordprocessingml" in mime:
                        extracted_content = DataExpert.process_docx(file_bytes)
                    elif "image" in mime:
                        extracted_content = f"[IMAGE ASSET] {f['name']} - Ready for Vision Analysis"
                    else:
                        extracted_content = file_bytes.decode('utf-8', errors='ignore')[:5000]
                except Exception as ex:
                    logger.warning(f"Failed expert extraction for {f['name']}: {ex}")
                    extracted_content = f"Error in expert extraction. Raw metadata: {f['name']}"

                # PATTERN RECOGNITION (Simulated Visual Detection)
                name_up = f['name'].upper()
                visual_context = []
                if "XRAY" in name_up or "SALE" in name_up:
                    visual_context.append("Expert Alert: Financial/Sales Data Identified")
                
                # ... existing point logic ...
                if "XRAY" in name_up:
                    extracted_points = ["Volumen de búsquedas Helium10, Ingresos estimados por ASIN, Benchmark de precios y BSR."]
                elif "KEYWORD" in name_up or "SERP" in name_up:
                    extracted_points = ["Tendencias de búsqueda, Rankings orgánicos, Dificultad de Keyword (KD) y PPC Bids."]
                else:
                    extracted_points = ["Expertly Extracted Content & Normalized Structures."]

                final_points = extracted_points + visual_context

                file_lineage[f['name']] = {
                    "id": f['id'],
                    "type": mime.split('/')[-1],
                    "size_kb": round(int(f.get('size', 0))/1024, 1),
                    "accessed_data": final_points,
                    "is_structured": structured_data is not None
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
                    "ingested_by": self.role
                }
                doc_id = self._save_to_raw_inputs(data_packet)
                if doc_id:
                    ingested_ids.append(doc_id)
            
            return {
                "ids": ingested_ids,
                "filenames": filenames,
                "mode": "REAL_DRIVE",
                "message": f"Ingesta Experta de {len(files)} archivos completada.",
                "data_stats": {
                    "total_files": len(files),
                    "folder_name": folder_name,
                    "lineage": file_lineage
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
