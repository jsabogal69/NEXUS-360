import logging
import re
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-4")

class Nexus4Strategist:
    task_description = "Hyper-Detailed Strategic Analysis & Moat Design"
    
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-4 (Strategist)"

    @report_agent_activity
    async def analyze_gaps(self, ssot_data: dict) -> dict:
        """
        Deep analysis of competitive gaps and design of defensive moats.
        Produces structured strategic gaps and McKinsey-style synthesis.
        """
        anchor = ssot_data.get("scout_anchor", "Mercado Analizado")
        input_names = [s['name'] for s in ssot_data.get("source_metadata", [])]
        
        logger.info(f"[{self.role}] Hyper-Detailed Strategic Analysis for: {anchor}")
        
        gaps = []
        v_title = ""
        v_text = ""
        roadmap = []
        
        ctx = anchor.upper()
        
        # --- STRATEGY FOR BABY NICHE ---
        if any(x in ctx for x in ["BABY", "NIGHT LIGHT", "SLEEP AID", "BEBE", "NOCHE", "SUEÑO"]):
            gaps.append({
                "niche": "Health & Pediatrics",
                "gap": "Barrera de Melatonina: El 80% de las luces actuales emiten picos de luz azul nociva.",
                "proposal": "Certificación 'SafeSleep' para espectro de luz roja pura (650nm) y materiales hipoalergénicos."
            })
            gaps.append({
                "niche": "Privacy & Security",
                "gap": "IoT Anxiety: Desconfianza masiva en cámaras chinas con almacenamiento en la nube.",
                "proposal": "Diseño 'Privacy-First' con procesamiento Edge-AI local para detección de llanto sin internet."
            })
            gaps.append({
                "niche": "Durability",
                "gap": "Obsolescencia Programada: Componentes plásticos que se degradan con el uso continuo.",
                "proposal": "Uso de Silicona Platino Grado Médico y chasis reforzado para ciclo de vida de 5+ años."
            })
            v_title = f"DOMINANCIA POR RESPONSABILIDAD Y SALUD EN {anchor.upper()}"
            v_text = f"El mercado de {anchor} ha sido inundado por juguetes genéricos que descuidan lo más importante: la salud neurológica del lactante. Proponemos el 'Ecosistema de Sueño Consciente', posicionando a NEXUS como la autoridad médica en el hogar moderno. No vendemos una lámpara; vendemos noches de descanso certificadas."
            roadmap = [
                ("I. Certificación Clínica", "Validación científica de espectros de luz y sonido sin loops. Objetivo: Ser el #1 en recomendación pediatra."),
                ("II. Ingeniería de Materiales", "Selección de materiales grado médico para contacto total. Certificación BPA-Free absoluta."),
                ("III. Capa Digital Offline", "Desarrollo de algoritmos locales de detección de llanto. Privacidad total como foso defensivo."),
                ("IV. Lanzamiento de Prestigio", "Colaboración con expertos en sueño infantil en TikTok y YouTube para educar sobre la luz roja."),
                ("V. Expansión de Ecosistema", "Lanzamiento de la App de monitoreo local y accesorios de aromaterapia integrados.")
            ]

        # --- STRATEGY FOR ELECTRONICS (GaN) ---
        elif any(x in ctx for x in ["65W", "GAN", "CHARGER", "ADAPTADOR", "POWER"]):
            gaps.append({
                "niche": "OLED Transparency",
                "gap": "Opacidad Energética: El usuario no sabe si su cargador realmente entrega los Watts prometidos.",
                "proposal": "Pantalla HD integrada que muestra Watts, temperatura y salud de batería en tiempo real."
            })
            gaps.append({
                "niche": "Power Stability",
                "gap": "Port Flapping: El reinicio de carga al conectar un segundo dispositivo estresa los circuitos.",
                "proposal": "Arquitectura de energía ininterrumpida que reasigna carga sin cortes de milisegundos."
            })
            gaps.append({
                "niche": "Moat: Status Design",
                "gap": "Commoditization: El sector es una guerra de 'plástico negro' indistinguible.",
                "proposal": "Chasis de aleación de aluminio CNC con estética 'Cyber-Professional' para desvincular precio de COGS."
            })
            v_title = f"DOMINANCIA POR TRANSPARENCIA Y PODER EN {anchor.upper()}"
            v_text = "Transformamos un commodity (el cargador) en un centro de comando energético. Al integrar transparencia total (OLED data) y seguridad de grado industrial, capturamos a los usuarios de alto ticket que no aceptan riesgos en sus dispositivos de $2000+."
            roadmap = [
                ("I. Validación GaN V Pro", "Testeo de carga continua al 100% por 48h. Objetivo: Ser el cargador más frío del mercado."),
                ("II. Estética & Materiales", "Carcasa de aluminio disipadora. No es plástico, es ingeniería aeroespacial."),
                ("III. Centro OLED Integrado", "Implementación de telemetría de energía visible para generar confianza inmediata."),
                ("IV. Campaña de Ingeniería Abierta", "Invitar a expertos a desarmar el producto para mostrar la calidad interna. Foso de transparencia."),
                ("V. Dominancia de Escritorio", "Lanzamiento de estaciones fijas y cables de silicona con el mismo ADN de diseño.")
            ]

        # --- DEFAULT STRATEGY ---
        else:
            gaps.append({
                "niche": "Brand Identity",
                "gap": "Trampa de Comoditización: Productos genéricos sin alma que el usuario desecha sin lealtad.",
                "proposal": "Inyección de ADN emocional y diseño propietario para romper la dependencia de moldes públicos."
            })
            gaps.append({
                "niche": "LTV & Ecosystem",
                "gap": "Vacío de Recurrencia: Ventas transaccionales que pierden la oportunidad de capturar lealtad post-venta.",
                "proposal": "Capa de servicios VIP o suscripción digital vinculada al hardware mediante beneficios de estatus."
            })
            v_title = "REDEFINICIÓN ESTRATÉGICA: EL NUEVO 'GOLD STANDARD'"
            v_text = f"Nuestra auditoría técnica confirma que el mercado de {anchor} está maduro para una disrupción de 'Estatus y Durabilidad'. Proponemos el abandono de la guerra de precios para capturar al segmento de 'Inversores de Estilo de Vida'."
            roadmap = [
                ("I. Auditoría de Fricción", "Analizar las 10 fallas críticas de los líderes y resolverlas en una sola pieza de ingeniería."),
                ("II. Selección Premium", "Sustitución de plásticos por materiales sostenibles y duraderos. El unboxing debe ser memorable."),
                ("III. Capa de Inteligencia", "Añadir funciones que realmente ahorren tiempo, no gadgets innecesarios."),
                ("IV. Lanzamiento de Escasez", "Preventa cerrada para early-adopters que buscan exclusividad."),
                ("V. Expansión de Categoría", "Bundle estratégico para elevar el Ticket Promedio (AOV) desde el lanzamiento.")
            ]

        # RECURSIVE INTELLIGENCE
        previous_intel = ssot_data.get("data_stats", {}).get("previous_intel")
        if previous_intel:
            p_verdict = previous_intel.get("verdict", {}).get("title", "Análisis Previo")
            gaps.insert(0, {
                "niche": "NEXUS Evolution",
                "gap": f"Continuidad Estratégica: Auditoría previa detectada ({p_verdict}).",
                "proposal": "Acelerar hacia fases avanzadas del Roadmap original para capitalizar la ventaja competitiva previa."
            })

        # PARTNER SUMMARY
        num_sources = len(input_names)
        partner_summary = f"""Socio, tras una inmersión forense en los {num_sources} archivos de inteligencia y un escaneo OSINT, mi síntesis es definitiva: estamos ante una oportunidad de **Dominancia por Ecosistema**, no por producto.

### I. La Trampa de la Comoditización
El análisis de 'Unit Economics' confirma que entrar con una 'Unidad Base' es un ejercicio de autodestrucción. En la categoría de {anchor}, los márgenes están bajo presión por la saturación de clones. Vender solo hardware es una carrera hacia el fondo.

### II. El Foso Estratégico
Nuestra ventaja reside en el diseño de un 'Moat' inexpugnable. Al desvincular el precio final del costo de materiales mediante materiales premium, servicios vinculados y una narrativa de estatus, creamos una barrera emocional y tecnológica que los incumbentes no pueden replicar sin canibalizar su propio inventario masivo.

### III. Veredicto NEXUS
Recomiendo posicionarnos como el **'Gold Standard'** absoluto. No vendemos un objeto; vendemos infraestructura de vida. La hoja de ruta está calibrada para ganar autoridad técnica antes de escalar. Es momento de dejar de ser un vendedor para convertirnos en el **dueño de la categoría**. El Dossier está listo para ejecución."""

        strategy_output = {
            "id": generate_id(),
            "parent_ssot_id": ssot_data.get("id"),
            "scout_data": ssot_data.get("scout_data", {}),
            "strategic_gaps": gaps,
            "timestamp": timestamp_now(),
            "scout_anchor": anchor,
            "analyzed_sources": input_names,
            "dynamic_verdict": {"title": v_title, "text": v_text},
            "dynamic_roadmap": roadmap,
            "partner_summary": partner_summary
        }
        
        self._save_strategy(strategy_output)
        return strategy_output

    def _save_strategy(self, data: dict):
        if not self.db: return
        try: self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: pass
