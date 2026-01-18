from ..shared.utils import get_db, ValidationStatus, timestamp_now, report_agent_activity, generate_id
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-8")

class Nexus8Guardian:
    task_description = "Validate input data schema and compliance"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-8 (The Guardian)"

    @report_agent_activity
    async def validate_input(self, input_id: str, content: dict) -> bool:
        """
        Validates raw input against safety, expert formatting, and schema rules.
        """
        logger.info(f"[{self.role}] Expertise Validation for: {input_id}")
        
        # Expert Fetch: If content is a placeholder, get real data from DB
        real_content = content
        if self.db and (not content or content.get("raw_content") == "batch_processing"):
            doc = self.db.collection("raw_inputs").document(input_id).get()
            if doc.exists:
                real_content = doc.to_dict()
        
        is_valid = True
        rejection_reason = None
        
        raw_text = real_content.get("raw_content", "")
        structured = real_content.get("structured_data")

        # 1. EMPTY CONTENT CHECK
        if not raw_text and not structured:
            is_valid = False
            rejection_reason = "NULL_DATA: No content or structured data found."

        # 2. EXPERT NUMBER CHECK (Anomaly Detection)
        if structured and isinstance(structured, list):
            # Check if numbers look sane or if there was a normalization failure
            # Heuristic: If a price column has values > 1,000,000 for a 65W charger, it's likely a separator error
            for row in structured[:20]:
                for k, v in row.items():
                    if "price" in k or "cost" in k:
                        if isinstance(v, (int, float)) and v > 500000:
                            is_valid = False
                            rejection_reason = f"FORMAT_ERROR: Suspiciously high value in {k} ({v}). Check thousands separator."
                            break

        # 3. CONTENT INTEGRITY (AI Hallucinated Text or Corrupted Data)
        if "Error in expert extraction" in raw_text:
            is_valid = False
            rejection_reason = "CORRUPTION: Harvester failed to read file bytes correctly."

        # 4. CROSS-FIELD VALIDATION
        if structured and len(structured) > 0:
            first_row_keys = set(structured[0].keys())
            if len(first_row_keys) < 2:
                is_valid = False
                rejection_reason = "STRUCTURE_WARNING: Low column density. Check if CSV separator was detected incorrectly."

        status = ValidationStatus.VALIDATED.value if is_valid else ValidationStatus.REJECTED.value
        
        self._update_status(input_id, status, rejection_reason)
        return is_valid

    @report_agent_activity
    async def perform_compliance_audit(self, strategy_data: dict) -> dict:
        """
        Auditoría exhaustiva de cumplimiento regulatorio internacional.
        Genera estándares específicos según la categoría del producto.
        """
        anchor = strategy_data.get("scout_anchor", "Mercado")
        norm_anchor = anchor.upper()
        
        # Enhanced category detection with more keywords
        is_electronics = any(x in norm_anchor for x in [
            "65W", "GAN", "CHARGER", "ADAPTADOR", "POWER", "USB", "BATTERY", "CABLE",
            "CARGADOR", "ENCHUFE", "OUTLET", "PLUG", "ELECTRIC", "VOLT", "WATT"
        ])
        is_lamp = any(x in norm_anchor for x in [
            "LAMP", "ILUMINACION", "LAMPARA", "LED", "LIGHTING", "LIGHT", "FOCO", 
            "BOMBILLA", "LUMINARIA", "SPOTLIGHT", "BULB"
        ])
        is_baby = any(x in norm_anchor for x in [
            "BABY", "BEBE", "BEBÉ", "INFANT", "NURSERY", "SLEEP", "CRIB", "CUNA",
            "RECIÉN NACIDO", "NOCHE", "DORMIR", "PROYECTOR", "ESTRELLAS", "RUIDO BLANCO",
            "WHITE NOISE", "NEWBORN", "TODDLER", "PEDIATRIC"
        ])
        is_beauty_personal_care = any(x in norm_anchor for x in [
            # Cabello / Hair
            "SHAMPOO", "CONDITIONER", "HAIR", "CABELLO", "PELO", "ANTICAIDA", "CAPILAR",
            "BIOTIN", "KERATIN", "ONION", "CEBOLLA", "MINOXIDIL", "TINTE", "DYE",
            # Piel / Skin
            "SKIN", "SKINCARE", "SERUM", "CREAM", "CREMA", "LOTION", "LOCIÓN",
            "MOISTURIZER", "HIDRATANTE", "PROTECTOR SOLAR", "SUNSCREEN", "SPF",
            "ANTI-AGING", "ANTIARRUGAS", "RETINOL", "VITAMINA C", "ÁCIDO HIALURÓNICO",
            # Cuidado Personal General
            "CUIDADO PERSONAL", "PERSONAL CARE", "BEAUTY", "COSMETIC", "BELLEZA",
            "HIGIENE", "HYGIENE", "CORPORAL", "BODY",
            # Dental
            "DENTAL", "TOOTHBRUSH", "CEPILLO DENTAL", "PASTA DENTAL", "TOOTHPASTE",
            "ENJUAGUE BUCAL", "MOUTHWASH", "BLANQUEADOR", "WHITENING", "FLOSS", "HILO DENTAL",
            # Afeitado / Razors
            "RAZOR", "RASURADORA", "AFEITADORA", "SHAVING", "ESPUMA DE AFEITAR",
            "BARBA", "BEARD", "TRIMMER", "RECORTADORA",
            # Desodorantes / Body Care
            "DEODORANT", "DESODORANTE", "ANTIPERSPIRANT", "ANTITRANSPIRANTE",
            "JABÓN", "SOAP", "GEL DE BAÑO", "BODY WASH", "EXFOLIANTE", "SCRUB",
            # Maquillaje
            "MAKEUP", "MAQUILLAJE", "LIPSTICK", "MASCARA", "FOUNDATION", "BASE",
            "EYESHADOW", "SOMBRA", "BLUSH", "RUBOR", "EYELINER", "DELINEADOR",
            # Aceites y tratamientos
            "ACEITE", "OIL", "MASCARILLA", "MASK", "TRATAMIENTO", "TREATMENT"
        ])
        is_food = any(x in norm_anchor for x in [
            "FOOD", "SUPPLEMENT", "VITAMIN", "ORGANIC", "EDIBLE", "DRINK", "SUPLEMENTO"
        ])
        is_toys = any(x in norm_anchor for x in [
            "TOY", "GAME", "PLAY", "KIDS", "CHILDREN", "JUGUETE", "NIÑO", "JUEGO"
        ])
        is_fitness = any(x in norm_anchor for x in [
            "YOGA", "FITNESS", "GYM", "EXERCISE", "SPORT", "WORKOUT", "EJERCICIO",
            "MAT", "COLCHONETA", "MANCUERNA", "PESA"
        ])
        is_pet = any(x in norm_anchor for x in [
            "PET", "DOG", "CAT", "ANIMAL", "MASCOTA", "PERRO", "GATO"
        ])
        is_home_appliance = any(x in norm_anchor for x in [
            "ASPIRADOR", "VACUUM", "ROBOT", "ROOMBA", "CLEANER", "LIMPIADOR",
            "HUMIDIFICADOR", "HUMIDIFIER", "PURIFICADOR", "PURIFIER", "AIR", "AIRE",
            "COCINA", "KITCHEN", "BLENDER", "LICUADORA", "FREIDORA", "FRYER"
        ])
        
        audit_results = []
        risk_level = "MEDIUM"
        compliance_score = 75
        
        # ═══════════════════════════════════════════════════════════════
        # ELECTRONICS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        if is_electronics:
            risk_level = "HIGH"
            compliance_score = 85
            audit_results = [
                {"std": "USB-IF / Power Delivery 3.1", "status": "MANDATORY", "desc": "Certificación obligatoria para negociación de voltaje dinámico. Garantiza compatibilidad universal y previene daños a dispositivos conectados. Requiere ensayos de interoperabilidad."},
                {"std": "IEC 62368-1 (Safety)", "status": "MANDATORY", "desc": "Estándar internacional de seguridad para equipos de audio/video y tecnología de la información. Reemplaza a IEC 60950-1. Obligatorio en UE, US, y Asia-Pacífico."},
                {"std": "DoE Level VI Efficiency", "status": "MANDATORY", "desc": "Regulación del Departamento de Energía de EE.UU. Exige eficiencia mínima del 87% en carga completa y <0.1W en modo standby. No-compliance = prohibición de venta."},
                {"std": "FCC Part 15 (EMC)", "status": "MANDATORY", "desc": "Límites de emisiones electromagnéticas para dispositivos electrónicos en EE.UU. Requiere testing en laboratorio acreditado y marcado FCC ID visible."},
                {"std": "CE Marking (EU)", "status": "MANDATORY", "desc": "Declaración de conformidad con directivas europeas LVD (2014/35/EU) y EMC (2014/30/EU). Obligatorio para venta en los 27 estados miembros."},
                {"std": "RoHS 3 Compliance", "status": "MANDATORY", "desc": "Restricción de sustancias peligrosas: Plomo, Mercurio, Cadmio, Cromo VI, PBB, PBDE y 4 ftalatos adicionales. Multas de hasta €50,000 por infracción."},
                {"std": "UL 62368-1 (NRTL)", "status": "RECOMMENDED", "desc": "Certificación de seguridad por laboratorio reconocido nacionalmente. Requerido por mayoría de retailers como Amazon, Best Buy y Target para listado."},
                {"std": "MFi Certification (Apple)", "status": "OPTIONAL", "desc": "Programa 'Made for iPhone/iPad' de Apple. Acceso a chips de autenticación y uso de logo oficial. Premium pricing justificado."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # BEAUTY / COSMETICS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_beauty_personal_care:
            risk_level = "HIGH"
            compliance_score = 80
            audit_results = [
                {"std": "FDA 21 CFR 700-740 (Cosmetics)", "status": "MANDATORY", "desc": "Regulación federal de EE.UU. para cosméticos. Exige etiquetado de ingredientes en orden descendente (INCI), advertencias de alérgenos, y prohibición de 11 sustancias."},
                {"std": "EU Cosmetics Regulation 1223/2009", "status": "MANDATORY", "desc": "Marco regulatorio europeo más estricto del mundo. Prohibe 1,300+ ingredientes, exige Persona Responsable en EU, y notificación en CPNP antes de venta."},
                {"std": "INCI Nomenclature (ISO 19749)", "status": "MANDATORY", "desc": "Nomenclatura Internacional de Ingredientes Cosméticos. Lista estandarizada obligatoria en etiquetado. Formato: Aqua, Sodium Laureth Sulfate, etc."},
                {"std": "Leaping Bunny (Cruelty-Free)", "status": "RECOMMENDED", "desc": "Certificación de Coalition for Consumer Information on Cosmetics. Garantiza cero testing en animales en toda la cadena de suministro. Alto valor para Gen-Z."},
                {"std": "USDA Organic (NOP)", "status": "OPTIONAL", "desc": "Certificación de Programa Nacional Orgánico. Permite uso de sello USDA si >95% de ingredientes son orgánicos certificados. Premium pricing +30%."},
                {"std": "EWG Verified", "status": "RECOMMENDED", "desc": "Verificación de Environmental Working Group. Rating de 1-10 en toxicidad de ingredientes. Productos con score 1-2 califican para sello EWG Verified."},
                {"std": "Prop 65 California", "status": "MANDATORY", "desc": "Proposición 65 de California. Requiere advertencias para productos con químicos conocidos por causar cáncer o toxicidad reproductiva. Multas de $2,500/día."},
                {"std": "Microplastic Ban (EU 2023/2055)", "status": "MANDATORY", "desc": "Prohibición de microplásticos añadidos intencionalmente. Afecta exfoliantes, glitter, y polímeros sintéticos <5mm. Entrada en vigor: Oct 2023."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # BABY PRODUCTS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_baby:
            risk_level = "CRITICAL"
            compliance_score = 90
            audit_results = [
                {"std": "CPSIA (Consumer Product Safety)", "status": "MANDATORY", "desc": "Ley de Mejora de Seguridad de Productos de Consumo. Límites estrictos de plomo (<100ppm) y ftalatos (<0.1%) en productos infantiles. Testing por terceros obligatorio."},
                {"std": "ASTM F963 (Toy Safety)", "status": "MANDATORY", "desc": "Estándar de seguridad de juguetes de EE.UU. Incluye pruebas de partes pequeñas (choke hazard), bordes afilados, inflamabilidad y toxicidad de pinturas."},
                {"std": "EN 71 (EU Toy Safety)", "status": "MANDATORY", "desc": "Directiva europea de seguridad de juguetes. Tres partes: propiedades mecánicas/físicas, inflamabilidad, y migración de elementos tóxicos. CE marking obligatorio."},
                {"std": "JPMA Certification", "status": "RECOMMENDED", "desc": "Certificación de Juvenile Products Manufacturers Association. Programa voluntario pero esperado por retailers premium. Incluye cunas, carriolas, sillas altas."},
                {"std": "FDA Food Contact (21 CFR 177)", "status": "MANDATORY", "desc": "Regulación para materiales en contacto con alimentos. Aplica a biberones, tetinas, mordedores. Silicona debe ser grado FDA o médico."},
                {"std": "Flammability (16 CFR 1610)", "status": "MANDATORY", "desc": "Estándar de inflamabilidad textil de CPSC. Prueba de tiempo de ignición y propagación de llama. Aplica a ropa de dormir y textiles de cuna."},
                {"std": "Safe Sleep Guidelines (AAP)", "status": "RECOMMENDED", "desc": "Guías de Academia Americana de Pediatría. Recomendaciones de superficie firme, sin objetos sueltos. Marketing debe alinearse con estas guías."},
                {"std": "BPA/Phthalate Free Claim", "status": "MANDATORY", "desc": "Declaración obligatoria de ausencia de Bisfenol A y ftalatos en productos de alimentación infantil. Verificación por laboratorio independiente requerida."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # LIGHTING / LAMPS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_lamp:
            risk_level = "MEDIUM"
            compliance_score = 82
            audit_results = [
                {"std": "UL 153 / UL 1598 (Luminaires)", "status": "MANDATORY", "desc": "Estándares de seguridad para lámparas portátiles y luminarias. Incluye pruebas de estabilidad, resistencia térmica, y aislamiento eléctrico."},
                {"std": "Energy Star Certification", "status": "RECOMMENDED", "desc": "Programa de EPA para eficiencia energética. LEDs deben mantener >70% de lúmenes iniciales a 25,000 horas. Marketing value significativo."},
                {"std": "IES LM-80 (LED Lumen Maintenance)", "status": "MANDATORY", "desc": "Metodología de prueba de mantenimiento lumínico. 6,000+ horas de testing requeridas para proyección de vida útil L70/L90."},
                {"std": "CRI Ra > 90 Claim", "status": "OPTIONAL", "desc": "Índice de Reproducción Cromática. Valores Ra >90 permiten claims de 'High CRI' o 'True Color'. Verificación por goniómetro requerida."},
                {"std": "IEEE 1789 (Flicker)", "status": "RECOMMENDED", "desc": "Prácticas recomendadas para reducir riesgos de parpadeo en iluminación LED. Modulation <8% a 100Hz para evitar efectos neurológicos."},
                {"std": "IEC 62471 (Photobiological Safety)", "status": "MANDATORY", "desc": "Clasificación de riesgo fotobiológico de lámparas. Evalúa daño UV, luz azul e infrarrojo. Grupo de riesgo debe estar en documentación técnica."},
                {"std": "California Title 20", "status": "MANDATORY", "desc": "Regulación de eficiencia energética de California. Requisitos mínimos de lúmenes/watt y límites de standby power para venta en CA."},
                {"std": "DLC (DesignLights Consortium)", "status": "OPTIONAL", "desc": "Programa de calificación para iluminación comercial LED. Acceso a rebates de utilities y preferencia en licitaciones gubernamentales."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # FITNESS / WELLNESS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_fitness:
            risk_level = "LOW"
            compliance_score = 78
            audit_results = [
                {"std": "ASTM F2006 (Fitness Equipment)", "status": "RECOMMENDED", "desc": "Estándar de seguridad para equipos de ejercicio de uso doméstico. Incluye pruebas de estabilidad, durabilidad y puntos de atrapamiento."},
                {"std": "EN 957 (EU Fitness Standards)", "status": "MANDATORY", "desc": "Serie de normas europeas para equipos de entrenamiento. Clasificación S, H, y A según intensidad de uso. CE marking requerido."},
                {"std": "REACH Compliance (EU)", "status": "MANDATORY", "desc": "Regulación de sustancias químicas en UE. Aplica a materiales como PVC, espumas EVA, y cauchos. Lista de 224+ sustancias restringidas."},
                {"std": "Prop 65 California", "status": "MANDATORY", "desc": "Advertencias para materiales de yoga mats y foam rollers que pueden contener ftalatos, plomo o formaldehído. Etiquetado preventivo común."},
                {"std": "OEKO-TEX Standard 100", "status": "RECOMMENDED", "desc": "Certificación de textiles libres de sustancias nocivas. Classes I-IV según contacto con piel. Alta demanda en productos premium."},
                {"std": "FSC Certification (Cork)", "status": "OPTIONAL", "desc": "Certificación Forest Stewardship Council para productos de corcho. Garantiza sostenibilidad forestal. Premium positioning para eco-conscious consumers."},
                {"std": "ISO 14001 (Environmental)", "status": "OPTIONAL", "desc": "Sistema de gestión ambiental. Demuestra compromiso con reducción de impacto ecológico en manufactura y supply chain."},
                {"std": "GRS (Global Recycled Standard)", "status": "OPTIONAL", "desc": "Certificación para productos con contenido reciclado. Permite claims de 'Made from Recycled Materials' con verificación de cadena de custodia."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # PET PRODUCTS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_pet:
            risk_level = "MEDIUM"
            compliance_score = 75
            audit_results = [
                {"std": "AAFCO Guidelines (Pet Food)", "status": "MANDATORY", "desc": "Guías de Association of American Feed Control Officials. Define requisitos nutricionales mínimos y etiquetado de ingredientes para alimentos de mascotas."},
                {"std": "FDA CVM Regulations", "status": "MANDATORY", "desc": "Center for Veterinary Medicine de FDA. Regula claims de salud, ingredientes prohibidos, y buenas prácticas de manufactura para pet food."},
                {"std": "FEDIAF (EU Pet Food)", "status": "MANDATORY", "desc": "Guías nutricionales de European Pet Food Industry Federation. Estándares de formulación para perros y gatos en mercado europeo."},
                {"std": "Non-Toxic Materials (ASTM F963)", "status": "MANDATORY", "desc": "Aplica estándares de juguetes infantiles a productos para mascotas. Límites de metales pesados y pequeñas partes desprendibles."},
                {"std": "NSF/ANSI 455 (Pet Supplements)", "status": "RECOMMENDED", "desc": "Estándar para suplementos dietéticos de mascotas. Verificación de potencia de ingredientes y ausencia de contaminantes."},
                {"std": "Organic Pet Food (USDA NOP)", "status": "OPTIONAL", "desc": "Certificación orgánica para ingredientes de pet food. Mismo estándar que alimentos humanos. Premium pricing +40%."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # FOOD / SUPPLEMENTS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_food:
            risk_level = "CRITICAL"
            compliance_score = 92
            audit_results = [
                {"std": "FDA FSMA (Food Safety)", "status": "MANDATORY", "desc": "Food Safety Modernization Act. Enfoque preventivo con planes HACCP, verificación de proveedores extranjeros, y trazabilidad completa."},
                {"std": "DSHEA (Supplements)", "status": "MANDATORY", "desc": "Dietary Supplement Health and Education Act. Define estructura de claims permitidos, etiquetado de Supplement Facts, y notificación de New Dietary Ingredients."},
                {"std": "NSF International Certification", "status": "RECOMMENDED", "desc": "Verificación de terceros para suplementos. Confirma contenido de etiqueta, ausencia de contaminantes, y GMP compliance. Confianza del consumidor."},
                {"std": "USP Verified", "status": "RECOMMENDED", "desc": "Marca de verificación de U.S. Pharmacopeia. Gold standard para potencia, pureza y calidad de suplementos. Diferenciador premium."},
                {"std": "Non-GMO Project Verified", "status": "OPTIONAL", "desc": "Certificación de ausencia de organismos genéticamente modificados. Sello reconocido por 88% de consumidores en encuestas."},
                {"std": "Allergen Labeling (FALCPA)", "status": "MANDATORY", "desc": "Food Allergen Labeling and Consumer Protection Act. Declaración obligatoria de los 9 alérgenos principales en etiquetado."},
                {"std": "California Prop 65", "status": "MANDATORY", "desc": "Advertencias para suplementos con ingredientes en lista de químicos conocidos. Acrylamide en café, lead en calcio, etc."},
                {"std": "cGMP 21 CFR 111", "status": "MANDATORY", "desc": "Current Good Manufacturing Practices para suplementos dietéticos. Incluye controles de identidad, pureza, fuerza y composición."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # TOYS / CHILDREN PRODUCTS COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_toys:
            risk_level = "CRITICAL"
            compliance_score = 88
            audit_results = [
                {"std": "CPSIA (Lead & Phthalates)", "status": "MANDATORY", "desc": "Límites de plomo <100ppm en sustratos y <90ppm en pinturas. Ftalatos prohibidos en productos de niños <12 años. Testing certificado obligatorio."},
                {"std": "ASTM F963-17 (Toy Safety)", "status": "MANDATORY", "desc": "Estándar comprensivo de seguridad de juguetes. 100+ pruebas incluyendo impacto, compresión, tensión, bordes y puntas afiladas."},
                {"std": "CPSC Registration", "status": "MANDATORY", "desc": "Registro de producto en Consumer Product Safety Commission. Incluye tarjeta de registro con información de contacto para recalls."},
                {"std": "EN 71 (CE Marking)", "status": "MANDATORY", "desc": "Directiva de seguridad de juguetes de UE. Partes 1-13 cubren propiedades mecánicas hasta químicas. Documentación técnica requerida."},
                {"std": "Age Grading Guidelines", "status": "MANDATORY", "desc": "Guías de CPSC para clasificación por edad. Determina advertencias de choke hazard y complejidad apropiada. Impacto legal significativo."},
                {"std": "ICTI Ethical Toy Program", "status": "RECOMMENDED", "desc": "Certificación de condiciones laborales éticas en fábricas de juguetes. Esperado por retailers como Walmart, Target, Amazon."},
                {"std": "Small Parts Regulation (16 CFR 1501)", "status": "MANDATORY", "desc": "Prohibición de partes pequeñas en juguetes para <3 años. Prueba con cilindro de partes pequeñas. Choke hazard = recall inmediato."},
                {"std": "Flammability (16 CFR 1500.44)", "status": "MANDATORY", "desc": "Prueba de inflamabilidad para juguetes. Tiempo de auto-extinción <2 segundos. Aplica a textiles, espumas y plásticos."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # HOME APPLIANCES COMPLIANCE
        # ═══════════════════════════════════════════════════════════════
        elif is_home_appliance:
            risk_level = "HIGH"
            compliance_score = 85
            audit_results = [
                {"std": "UL/ETL Listing (NRTL)", "status": "MANDATORY", "desc": "Certificación de seguridad eléctrica por laboratorio reconocido nacionalmente. Obligatorio para retailers como Amazon, Home Depot, Walmart."},
                {"std": "EPA Energy Star", "status": "RECOMMENDED", "desc": "Certificación de eficiencia energética. Reduce costos operativos y acceso a incentivos fiscales. Alto valor de marketing."},
                {"std": "FCC Part 15 (EMC)", "status": "MANDATORY", "desc": "Límites de emisiones electromagnéticas para dispositivos electrónicos. Obligatorio para venta en EE.UU. con marcado FCC ID."},
                {"std": "CE Marking (EU)", "status": "MANDATORY", "desc": "Conformidad con directivas europeas LVD, EMC y RoHS. Obligatorio para venta en los 27 estados miembros de la UE."},
                {"std": "RoHS 3 Compliance", "status": "MANDATORY", "desc": "Restricción de sustancias peligrosas en equipos eléctricos. 10 sustancias restringidas incluyendo plomo y mercurio."},
                {"std": "WEEE Directive (EU)", "status": "MANDATORY", "desc": "Directiva de residuos de equipos eléctricos y electrónicos. Requiere registro de productor y símbolo de reciclaje."},
                {"std": "Prop 65 California", "status": "MANDATORY", "desc": "Advertencias para productos que contienen químicos de la lista. Multas de $2,500/día por incumplimiento."},
                {"std": "IEC 60335-1 (Safety)", "status": "MANDATORY", "desc": "Estándar internacional de seguridad para electrodomésticos. Pruebas de aislamiento, resistencia térmica y protección eléctrica."}
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # GENERAL / OTHER CATEGORIES (Dynamic fallback)
        # ═══════════════════════════════════════════════════════════════
        else:
            risk_level = "LOW"
            compliance_score = 70
            # More generic but still useful standards
            audit_results = [
                {"std": "CE Marking (EU)", "status": "MANDATORY", "desc": f"Declaración de conformidad con directivas europeas aplicables para '{anchor}'. Obligatorio para venta en Espacio Económico Europeo."},
                {"std": "REACH Compliance (EU)", "status": "MANDATORY", "desc": "Regulación de químicos en productos vendidos en UE. Declaración de ausencia de sustancias de muy alta preocupación (SVHC)."},
                {"std": "California Prop 65", "status": "MANDATORY", "desc": f"Advertencias para productos de '{anchor}' que contienen químicos de la lista de California."},
                {"std": "Amazon Product Compliance", "status": "MANDATORY", "desc": f"Requisitos específicos de Amazon Seller Central para la categoría '{anchor}'. Documentación de seguridad requerida."},
                {"std": "Country of Origin Labeling", "status": "MANDATORY", "desc": "Marcado obligatorio de 'Made in [Country]' en todos los productos importados. Regulado por CBP."},
                {"std": "ISO 9001:2015 (Quality)", "status": "RECOMMENDED", "desc": "Sistema de gestión de calidad reconocido globalmente. Demuestra procesos consistentes de manufactura."},
                {"std": "Product Liability Insurance", "status": "RECOMMENDED", "desc": f"Seguro de responsabilidad del producto para '{anchor}'. Protección legal contra claims de consumidores."},
                {"std": "FBA Compliance (Amazon)", "status": "MANDATORY", "desc": "Requisitos de empaque, etiquetado y códigos de barras para Fulfillment by Amazon. Pasos de prep específicos por categoría."}
            ]

        return {
            "id": generate_id(),
            "niche_compliance": anchor,
            "risk_level": risk_level,
            "compliance_score": compliance_score,
            "audits": audit_results,
            "total_standards": len(audit_results),
            "mandatory_count": len([a for a in audit_results if a["status"] == "MANDATORY"]),
            "security_protocol": "EYES ONLY - E2E Encrypted Pipeline",
            "audit_note": f"Auditoría exhaustiva de {len(audit_results)} estándares internacionales para la categoría '{anchor}'. Se identificaron {len([a for a in audit_results if a['status'] == 'MANDATORY'])} requisitos obligatorios y {len([a for a in audit_results if a['status'] == 'RECOMMENDED'])} recomendados.",
            "timestamp": timestamp_now()
        }

    def _update_status(self, input_id: str, status: str, reason: str = None):
        if not self.db:
            logger.warning("DB not connected, skipping update.")
            return

        try:
            ref = self.db.collection("raw_inputs").document(input_id)
            update_data = {
                "validation_status": status,
                "validated_at": timestamp_now(),
                "validator": self.role
            }
            if reason:
                update_data["rejection_reason"] = reason
            
            ref.update(update_data)
            logger.info(f"[{self.role}] Updated {input_id} to {status}")
        except Exception as e:
            logger.error(f"Failed to update Firestore: {e}")

# Entry point for testing
if __name__ == "__main__":
    guardian = Nexus8Guardian()
    logger.info(f"{guardian.role} Online.")
