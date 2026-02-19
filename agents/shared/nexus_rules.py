"""
NEXUS-360 BUSINESS RULES ENGINE
================================
Módulo centralizado con las 4 Reglas Estrictas de Negocio.
Todas las funciones de generación LLM DEBEN incluir estos bloques.

REGLAS:
  1. Sanitización Lingüística (Data Cleaning)
  2. Anclaje Financiero Dinámico (Cero Alucinaciones)
  3. Conciencia de Categoría (Moats Realistas)
  4. Análisis Competitivo Anti-Pereza
"""

import re
import logging

logger = logging.getLogger("NEXUS-RULES")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORÍAS LOW-TECH (REGLA 3)
# ═══════════════════════════════════════════════════════════════════════════
LOW_TECH_CATEGORIES = [
    # Hogar / Organización
    "escurridor", "dish rack", "zapatero", "shoe rack", "organizador", "organizer",
    "estantería", "shelf", "perchero", "coat rack", "cesta", "basket", "balde", "bucket",
    "mop", "trapeador", "escoba", "broom", "basurero", "trash can", "papelera",
    "colgador", "hanger", "tendedero", "drying rack", "porta", "holder",
    # Cocina low-tech
    "tabla de cortar", "cutting board", "colador", "strainer", "rallador", "grater",
    "embudo", "funnel", "espátula", "spatula", "pelador", "peeler",
    # Almacenamiento / Muebles simples
    "caja de almacenamiento", "storage box", "cajón", "drawer", "repisa", "ledge",
    "soporte", "stand", "base", "pedestal", "paleta", "pallet",
    # Jardín / Herramientas básicas
    "maceta", "flowerpot", "rastrillo", "rake", "pala", "shovel", "manguera", "hose",
]

DIGITAL_FORBIDDEN_TERMS = [
    "app", "aplicación", "software", "ecosistema digital", "plataforma digital",
    "suscripción digital", "cable usb", "cable de datos", "cable reforzado",
    "sistema inteligente", "smart", "iot", "bluetooth", "wifi", "nfc",
    "masterclass virtual", "acceso lifetime app", "dashboard", "api",
]


def is_low_tech_product(product_description: str) -> bool:
    """
    Detecta si el producto pertenece a la categoría Low-Tech / Hogar / Organización.
    Si es Low-Tech, la REGLA 3 aplica: moats 100% materiales.
    """
    desc_lower = product_description.lower()
    return any(term in desc_lower for term in LOW_TECH_CATEGORIES)


def sanitize_product_name(raw_anchor: str) -> str:
    """
    REGLA 1: Sanitización Lingüística.
    Extrae el nombre genérico, fluido y natural del producto.
    Elimina paréntesis con traducciones, códigos rotos, textos truncados.

    Ejemplos:
        "escurridores de platos (Dish Drying Rack) se desc" → "escurridores de platos"
        "ZAPATERO (Shoe Rack) - Amazon FBA" → "zapatero"
    """
    if not raw_anchor:
        return raw_anchor

    # 1. Eliminar contenido entre paréntesis (traducciones, códigos)
    cleaned = re.sub(r'\(.*?\)', '', raw_anchor)

    # 2. Eliminar contenido después de guión largo o doble guión (subtítulos)
    cleaned = re.sub(r'\s*[-–—]\s*.+', '', cleaned)

    # 3. Eliminar palabras técnicas/truncadas comunes al final
    noise_words = [
        r'\bse desc\b', r'\bse de\b', r'\bamazon\b', r'\bfba\b', r'\basin\b',
        r'\bnicho\b', r'\bmercado\b', r'\bprivate label\b', r'\bpl\b',
        r'\bkeyword\b', r'\bsearch\b', r'\bterm\b',
    ]
    for nw in noise_words:
        cleaned = re.sub(nw, '', cleaned, flags=re.IGNORECASE)

    # 4. Limpiar espacios múltiples y trimear
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip().rstrip('.,;:')

    # 5. Si quedó vacío, usar el original
    if not cleaned:
        return raw_anchor.strip()

    logger.debug(f"[REGLA-1] Sanitized: '{raw_anchor}' → '{cleaned}'")
    return cleaned


def get_system_rules_block(product_description: str, avg_price: float = 0.0) -> str:
    """
    Genera el bloque de INSTRUCCIONES DEL SISTEMA con las 4 Reglas de Negocio.
    Este bloque debe inyectarse AL INICIO de cada prompt LLM relevante.

    Args:
        product_description: Nombre/descripción del producto (ya sanitizado con REGLA 1)
        avg_price: Precio promedio real del mercado para anclaje financiero (REGLA 2)
    
    Returns:
        String con el bloque completo de reglas para insertar en el prompt.
    """
    is_low_tech = is_low_tech_product(product_description)

    price_anchor = f"${avg_price:.2f}" if avg_price > 0 else "el precio promedio/mediana real del nicho"

    regla3_block = ""
    if is_low_tech:
        regla3_block = f"""
[REGLA 3: CONCIENCIA DE CATEGORÍA — LOW-TECH DETECTADO ⚠️]
- El producto "{product_description}" pertenece a la categoría: Hogar / Organización / Low-Tech.
- TIENES ABSOLUTAMENTE PROHIBIDO sugerir como diferenciadores o moats:
  ✗ Apps, software, plataformas digitales, ecosistemas digitales
  ✗ Cables (USB, de datos, reforzados, de cualquier tipo)
  ✗ Funciones "Smart" / IoT / Bluetooth / WiFi
  ✗ Suscripciones digitales, masterclasses virtuales, dashboards
- La propuesta de valor DEBE ser 100% material y física:
  ✓ Mayor grosor de acero inoxidable (ej. grado 304/316)
  ✓ Madera sólida certificada (bambú, roble, nogal)
  ✓ Diseño modular o expansible
  ✓ Empaque anti-roturas y tratamiento anticorrosión
  ✓ Garantías físicas extendidas (3-5 años)
  ✓ Acabados premium (sand-blasted, powder-coated, etc.)
"""
    else:
        regla3_block = """
[REGLA 3: CONCIENCIA DE CATEGORÍA]
- Analiza la naturaleza física del producto antes de proponer moats y diferenciadores.
- Si es Low-Tech (hogar, organización, utensilios), prohíbete sugerir Apps, Software o cables digitales.
- La propuesta de valor debe ser coherente con la categoría física del producto.
"""

    block = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║         INSTRUCCIONES DEL SISTEMA — NEXUS-360 REGLAS ESTRICTAS          ║
║    Incumplir estas reglas es un FALLO CRÍTICO del sistema. Sin excepciones.  ║
╚═══════════════════════════════════════════════════════════════════════════╝

[REGLA 1: SANITIZACIÓN LINGÜÍSTICA]
- El producto a analizar es: "{product_description}"
- TIENES PROHIBIDO inyectar el término crudo con paréntesis, traducciones o códigos rotos.
- Usa ÚNICAMENTE el nombre genérico, fluido y natural en español.
  ✗ Incorrecto: "escurridores de platos (Dish Drying Rack) se desc"
  ✓ Correcto: "escurridores de platos"

[REGLA 2: ANCLAJE FINANCIERO DINÁMICO — CERO ALUCINACIONES]
- El precio promedio/mediana REAL del mercado para este nicho es: {price_anchor}
- TODOS los cálculos de Unit Economics, escenarios proyectados y márgenes DEBEN
  basarse matemáticamente en ese precio real.
- NUNCA inventes precios de plantilla ($50, $92, $125) si los datos muestran otra cosa.
- NUNCA uses márgenes de "0%" como relleno.
- Si faltan datos logísticos, escribe EXACTAMENTE:
  "Datos logísticos insuficientes para un cálculo de margen exacto"
{regla3_block}
[REGLA 4: ANÁLISIS COMPETITIVO ANTI-PEREZA]
- Para cada ASIN/competidor, redacta una [Vulnerabilidad] o [Insight] ÚNICO.
- TIENES PROHIBIDO copiar y pegar la misma frase genérica en múltiples filas.
  ✗ Incorrecto: "FAST MOVER: Seller nuevo con pocas reviews" para TODOS los ASINs
  ✓ Correcto: Analiza métricas individuales (BSR, rating, reviews, precio) de CADA producto
- Analiza a cada jugador de forma individual.
- Si no hay datos suficientes, escribe EXACTAMENTE:
  "Datos cualitativos insuficientes para perfilado individual"

═══════════════════════════════════════════════════════════════════════════
FIN DE INSTRUCCIONES DEL SISTEMA — COMIENZA EL ANÁLISIS
═══════════════════════════════════════════════════════════════════════════
"""
    return block


def get_financial_anchor_warning(avg_price: float) -> str:
    """
    Genera una advertencia específica para los modelos financieros (REGLA 2).
    Úsала al inicio de cualquier prompt que calcule Unit Economics o ROI.
    """
    if avg_price > 0:
        return f"""
⚠️ ANCLAJE FINANCIERO OBLIGATORIO (REGLA 2):
El precio de referencia para TODOS los cálculos es ${avg_price:.2f} (dato real del nicho).
No uses $50, $92 ni $125 por defecto. Usa ${avg_price:.2f} como base.
"""
    return """
⚠️ DATOS FINANCIEROS PENDIENTES (REGLA 2):
No se detectaron datos de precio reales. Escribe "Datos logísticos insuficientes
para un cálculo de margen exacto" en lugar de inventar valores.
"""


def validate_moat_for_low_tech(moat_text: str, product_description: str) -> str:
    """
    REGLA 3 post-processing: Si el producto es Low-Tech, elimina referencias
    a términos digitales/electrónicos de los moats generados por el LLM.
    Retorna el texto corregido con una nota si se realizaron cambios.
    """
    if not is_low_tech_product(product_description):
        return moat_text

    original = moat_text
    corrected = moat_text
    changes = []

    for forbidden in DIGITAL_FORBIDDEN_TERMS:
        pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
        if pattern.search(corrected):
            corrected = pattern.sub("[DIFERENCIADOR FÍSICO REQUERIDO]", corrected)
            changes.append(forbidden)

    if changes:
        logger.warning(
            f"[REGLA-3] Low-Tech violation detected in moat text. "
            f"Replaced: {changes}. Product: {product_description[:50]}"
        )

    return corrected


def validate_competitive_analysis(top_10_products: list) -> list:
    """
    REGLA 4 post-processing: Detecta y marca vulnerabilidades genéricas copy-pasted.
    Si más del 60% de los productos tienen el mismo texto de vulnerabilidad,
    marca todos como 'Datos cualitativos insuficientes para perfilado individual'.
    """
    if not top_10_products:
        return top_10_products

    vulns = [p.get("vuln", "").strip().lower() for p in top_10_products if p.get("vuln")]
    if not vulns:
        return top_10_products

    from collections import Counter
    vuln_counts = Counter(vulns)
    most_common_vuln, most_common_count = vuln_counts.most_common(1)[0]

    # If the same vulnerability appears in >60% of products, flag it
    if most_common_count / len(vulns) > 0.60:
        logger.warning(
            f"[REGLA-4] Generic copy-paste detected: '{most_common_vuln[:60]}...' "
            f"appears in {most_common_count}/{len(vulns)} products. Flagging."
        )
        for p in top_10_products:
            if p.get("vuln", "").strip().lower() == most_common_vuln:
                p["vuln"] = "Datos cualitativos insuficientes para perfilado individual"
                p["_regla4_flag"] = True

    return top_10_products
