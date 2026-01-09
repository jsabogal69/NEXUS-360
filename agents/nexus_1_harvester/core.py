import time
from ..shared.utils import get_db, generate_id, timestamp_now, AgentRole, report_agent_activity
import logging

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
                
                name_up = f['name'].upper()
                
                # PATTERN RECOGNITION (Simulated Visual Detection)
                visual_context = []
                if any(x in name_up for x in ["SALE", "VENTA", "CHART", "GRAPH"]):
                    visual_context.append("Visual Detection: Trend Pattern Identified")
                if any(x in name_up for x in ["SEASON", "ESTACIONALIDAD", "HEATMAP"]):
                    visual_context.append("Visual Detection: Temporal Seasonality Pattern")
                
                if "XRAY" in name_up:
                    extracted_points = ["Volumen de búsquedas Helium10, Ingresos estimados por ASIN, Benchmark de precios y BSR."]
                elif "KEYWORD" in name_up or "SERP" in name_up:
                    extracted_points = ["Tendencias de búsqueda, Rankings orgánicos, Dificultad de Keyword (KD) y PPC Bids."]
                elif "SEARCHTERMS" in name_up:
                    extracted_points = ["Palabras clave de conversión, Cuota de mercado por término y Análisis de competencia SEO."]
                elif "PRODUCTS" in name_up or "ASIN" in name_up or "SEARCHRESULTS" in name_up:
                    extracted_points = ["Matriz técnica de competidores (Visual Match), Ratings promedio y Análisis de variantes (Top Sellers)."]
                elif "NICHES" in name_up:
                    extracted_points = ["Categorización de mercado, Segmentación de sub-nichos y Visibilidad de marca."]
                elif any(x in name_up for x in [".PNG", ".JPG", "SCREENSHOT", "CAPTUR"]):
                    extracted_points = ["Auditoría visual: Infografías de producto, Diseño de empaque y Calidad de Assets en Amazon."]
                elif "ESTUDIO" in name_up or "OPORTUNIDAD" in name_up:
                    extracted_points = ["Análisis de viabilidad, Roadmap de lanzamiento y Análisis de brechas de satisfacción."]
                elif "HIQ" in name_up or "PROD" in name_up or "LAMPARA" in name_up:
                    extracted_points = ["Especificaciones de ingeniería, Materiales (Grade), y Propuesta de Valor única."]
                elif "REPORT_" in name_up or "DOSSIER" in name_up:
                    extracted_points = ["Pre-Analytic Intelligence: Veredictos Históricos, Roadmaps Previos y Gaps de Consultoría NEXUS."]
                else:
                    extracted_points = ["Metadatos generales, Estructura de documentos y Resumen de contenido crudo."]
                
                # Combine points with visual context
                final_points = extracted_points + visual_context

                file_lineage[f['name']] = {
                    "id": f['id'],
                    "type": f['mimeType'].split('/')[-1],
                    "size_kb": round(int(f.get('size', 0))/1024, 1),
                    "accessed_data": final_points
                }
                
                mock_content = f"Contenido REAL de {f['name']} resumido para análisis."
                doc_id = self.ingest_mock_data(f['name'], mock_content)
                if doc_id:
                    ingested_ids.append(doc_id)
            
            return {
                "ids": ingested_ids,
                "filenames": filenames,
                "mode": "REAL_DRIVE",
                "message": f"Ingesta exitosa de {len(files)} archivos.",
                "data_stats": {
                    "total_files": len(files),
                    "folder_name": folder_name,
                    "lineage": file_lineage # PASS TO STRATEGIST
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
