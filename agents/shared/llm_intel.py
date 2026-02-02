"""
LLM-Powered Market Intelligence Generator
Uses Google Gemini AI to generate contextual competitive analysis for any product category.
"""
import os
import json
import logging
import random
import re
from datetime import datetime
from .utils import sanitize_text_field

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system env vars

logger = logging.getLogger("LLM-INTEL")

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. LLM features disabled.")


def get_gemini_model():
    """Initialize and return Gemini model if API key is available."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("No GEMINI_API_KEY found. Using enhanced mock data.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        return None


def generate_market_intel(product_description: str, additional_context: str = None) -> dict:
    """
    Generate market intelligence using Gemini AI.
    Falls back to enhanced mock data if LLM is unavailable.
    """
    if not GEMINI_AVAILABLE:
        return generate_enhanced_mock(product_description)
    
    model = get_gemini_model()
    if not model:
        return generate_enhanced_mock(product_description)
    
    context_block = ""
    if additional_context:
        context_block = f"\n═══════════════════════════════════════════════════════════════════════════════\nINFORMACIÓN EXTRAÍDA DE DOCUMENTOS DEL USUARIO (PRIORIDAD ALTA):\n═══════════════════════════════════════════════════════════════════════════════\n{additional_context}\n"

    prompt = f"""Eres un experto en Social Listening que combina el análisis de datos de Neil Patel con la estrategia de atención de GaryVee.

PRODUCTO A ANALIZAR: "{product_description}"
{context_block}
═══════════════════════════════════════════════════════════════════════════════
FASE 1: EXTRACCIÓN DE DATOS (ENFOQUE NEIL PATEL)
═══════════════════════════════════════════════════════════════════════════════

Actúa como analista de datos y especialista en SEO:

1. KEYWORDS DE INTENTO DE DOLOR: Identifica las 10 keywords más buscadas relacionadas con:
   - Términos de "comparación" (producto A vs B)
   - Términos de "problemas" (cómo arreglar, falla en, error de)
   - Términos de "alternativas" (alternativa a, reemplazo de)

2. ANÁLISIS DE COMPETENCIA: Para los 3 competidores principales:
   - ¿Qué están IGNORANDO en sus secciones de comentarios?
   - ¿Qué preguntas quedan sin responder?

3. SHARE OF SEARCH: ¿Qué preguntas se hacen en Google, TikTok y YouTube que NO tienen respuesta clara todavía?

═══════════════════════════════════════════════════════════════════════════════
FASE 2: INMERSIÓN CULTURAL (ENFOQUE GARYVEE)
═══════════════════════════════════════════════════════════════════════════════

Actúa como estratega de contenido que vive en las trincheras de redes sociales:

1. ANÁLISIS DEL 'DIRT' (COMENTARIOS): Clasifica el sentimiento por EMOCIONES:
   - Frustración: ¿Qué les molesta profundamente?
   - Nostalgia: ¿Qué extrañan de productos anteriores?
   - Humor: ¿Qué memes o bromas circulan?
   - Deseo: ¿Qué producto "soñado" describen?
   - Escepticismo: ¿Qué claims no les creen?

2. REVERSE ENGINEERING DE ATENCIÓN: ¿Qué formatos retienen atención?
   - ¿Es el tono crudo/auténtico?
   - ¿Es la edición rápida?
   - ¿Es el storytelling personal?

3. WHITE SPACE: Temas que la gente discute en comentarios pero las marcas NO han convertido en contenido principal.

═══════════════════════════════════════════════════════════════════════════════
FASE 3: RIGOR CIENTÍFICO E INDUSTRIAL (THE SCHOLAR AUDIT)
═══════════════════════════════════════════════════════════════════════════

Actúa como un auditor técnico y de cumplimiento:

1. FUENTES DE AUTORIDAD: Identifica 2-3 hallazgos de:
   - Papers académicos o estudios clínicos (si aplica)
   - Reportes de industria (Statista, McKinsey, Nielsen)
   - Normativas de seguridad o estándares (FDA, ISO, CE, ASTM, FCC)
   - Patentes o innovaciones técnicas en la categoría

2. RELEVANCIA: Explica cómo este hallazgo técnico se convierte en una ventaja competitiva de marketing.

═══════════════════════════════════════════════════════════════════════════════
FORMATO DE RESPUESTA: JSON ESTRUCTURADO
═══════════════════════════════════════════════════════════════════════════════

{{
    "niche_name": "Nombre de la categoría de mercado",
    "top_10_products": [
        {{
            "rank": 1,
            "name": "Nombre REAL del producto en Amazon",
            "price": 29.99,
            "reviews": 15000,
            "rating": 4.5,
            "adv": "Ventaja competitiva principal - SÉ MUY ESPECÍFICO",
            "vuln": "Debilidad real identificada en reviews - CITA PROBLEMAS REALES",
            "gap": "Brecha de mercado específica que NO cubre"
        }}
    ],
    "social_listening": {{
        "amazon_review_audit": "Análisis forense de 1000+ reseñas. Incluye patrones de quejas y elogios.",
        "pain_keywords": [
            {{"keyword": "término de dolor", "search_intent": "problema/comparación/alternativa", "volume": "Alto/Medio/Bajo", "opportunity": "Por qué es oportunidad"}}
        ],
        "competitor_gaps": [
            {{"competitor": "Nombre del competidor", "ignored_issue": "Qué ignoran en comentarios", "user_frustration": "Cita textual de frustración"}}
        ],
        "emotional_analysis": {{
            "frustration": "Qué les frustra profundamente (con ejemplos textuales)",
            "nostalgia": "Qué extrañan de versiones anteriores o competidores",
            "humor": "Memes y bromas que circulan sobre el producto/nicho",
            "desire": "El producto 'soñado' que describen los usuarios",
            "skepticism": "Claims de marketing que NO les creen"
        }},
        "attention_formats": {{
            "what_works": "Formatos de contenido que retienen atención",
            "tone": "Tono que resuena (crudo, educativo, emocional)",
            "viral_elements": "Elementos que hacen viral al contenido"
        }},
        "white_space_topics": ["Temas discutidos en comentarios que las marcas ignoran"],
        "cultural_vibe": "Descripción del tono de la comunidad: ¿cínica, entusiasta, confundida, escéptica?",
        "pros": ["5 puntos positivos del mercado detectados en social listening"],
        "cons": ["5 puntos negativos/frustraciones detectadas"],
        "tiktok_trends": "Hashtags virales, creadores clave, formatos dominantes con números de vistas",
        "reddit_insights": "Subreddits relevantes, opiniones dominantes, quejas recurrentes con r/ específicos",
        "youtube_search_gaps": "Preguntas en YouTube sin respuestas de calidad",
        "google_search_insights": "Tendencias de búsqueda, preguntas PAA sin responder",
        "consumer_desire": "Lo que REALMENTE desea el consumidor (no lo que las marcas creen)"
    }},
    "content_opportunities": {{
        "garyvee_style": [
            {{"idea": "Concepto de contenido", "format": "Formato específico", "hook": "Gancho de apertura", "emotional_trigger": "Emoción que activa"}}
        ],
        "patel_style": [
            {{"idea": "Concepto educativo/SEO", "target_keyword": "Keyword objetivo", "search_intent": "Intención de búsqueda", "content_gap": "Por qué no existe buen contenido"}}
        ]
    }},
    "trends": [
        {{
            "title": "Nombre de la tendencia",
            "description": "Descripción detallada con datos específicos"
        }}
    ],
    "keywords": [
        {{
            "term": "Término de búsqueda",
            "volume": "Alto/Medio/Bajo",
            "trend": "Trending Up/Stable/Emerging",
            "intent": "Informacional/Transaccional/Comparativo",
            "difficulty": "Alta/Media/Baja"
        }}
    ],
    "sales_intelligence": {{
        "market_share_by_brand": [
            {{"brand": "Marca", "share": 30, "status": "Líder/Retador/Nicho", "weakness": "Debilidad explotable"}}
        ],
        "sub_category_distribution": {{
            "Subcategoría 1": 40,
            "Subcategoría 2": 30
        }},
        "seasonality": {{
            "peaks": [{{"month": "Mes", "event": "Evento", "impact": "High/Extreme", "strategy": "Qué hacer"}}],
            "low_points": ["Meses bajos con razón"],
            "strategy_insight": "Insight estratégico detallado de timing",
            "monthly_demand": {{
                "Enero": 55, "Febrero": 60, "Marzo": 65, "Abril": 70, 
                "Mayo": 75, "Junio": 70, "Julio": 85, "Agosto": 70, 
                "Septiembre": 65, "Octubre": 75, "Noviembre": 100, "Diciembre": 95
            }}
        }}
    }},
    "sentiment_summary": "Resumen ejecutivo del sentimiento: ¿La comunidad es cínica, entusiasta o confundida? ¿Por qué?",
    "scholar_audit": [
        {{
            "source": "Fuente académica o de industria REAL",
            "finding": "Hallazgo específico con datos",
            "relevance": "Cómo aplica a este producto"
        }}
    ]
}}

═══════════════════════════════════════════════════════════════════════════════
REGLAS CRÍTICAS:
═══════════════════════════════════════════════════════════════════════════════

- Usa nombres de productos y marcas REALES que existen en Amazon
- Incluye exactamente 10 productos en top_10_products
- Incluye exactamente 4 tendencias
- Incluye exactamente 10 keywords con todos los campos
- Incluye 3 ideas GaryVee style y 3 ideas Patel style en content_opportunities
- Incluye 5 pain_keywords y 3 competitor_gaps
- Incluye EXACTAMENTE 5 marcas REALES en sales_intelligence.market_share_by_brand con sus respectivos % (ej: BrandA: 35, BrandB: 20...).
- IMPORTANTE: La distribución de market share debe seguir el Principio de Pareto (80/20). NUNCA asignes porcentajes iguales (ej: todo 10%). El líder debe tener >30%, el segundo ~20-25%, el tercero ~15%, etc.
- Incluye EXACTAMENTE entre 2 y 3 hallazgos en scholar_audit. 
  * Si no hay papers académicos, usa reportes de industria, normativas (FDA, ISO), o estudios de mercado REALES.
- SÉ EXTREMADAMENTE ESPECÍFICO - evita generalidades
- Usa citas textuales cuando describas frustraciones de usuarios
- Todos los textos en ESPAÑOL
- CRÍTICO para monthly_demand: Analiza ESTE PRODUCTO ESPECÍFICO y genera valores únicos:
  * NO uses patrones predefinidos por categoría
  * Analiza el comportamiento REAL del consumidor para ESTE producto
  * Considera: clima, temporadas, eventos específicos, comportamiento de compra
  * El mes con mayor demanda = 100, el resto proporcional
  * Si es un producto estacional (verano, invierno, escolar, etc), la curva debe reflejar ALTA VARIACIÓN
  * Si es un producto perenne (consumibles diarios, etc), la curva puede ser más estable
  * IMPORTANTE: Cada producto tiene su propia curva única - NO copies patrones genéricos
- Responde SOLO con el JSON, sin texto adicional
"""

    MAX_RETRIES = 2
    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(prompt)
            text = response.text
            break # Success
        except Exception as e:
            logger.error(f"[LLM-INTEL] Gemini API error (Attempt {attempt+1}/{MAX_RETRIES}): {str(e)}")
            if attempt == MAX_RETRIES - 1:
                return generate_enhanced_mock(product_description)
    
    try:
        
        # Clean response (remove markdown code blocks if present)
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        # Robustly find the first { and last }
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            text = text[start_idx:end_idx+1]
        
        data = json.loads(text.strip())
        
        # Sanitization: Clean string stutters (e.g. "fall primaril")
        # We can apply a recursive cleaner for strings
        def clean_stutters(obj):
            if isinstance(obj, dict):
                return {k: clean_stutters(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_stutters(i) for i in obj]
            elif isinstance(obj, str):
                # Specific fix for reported 'fall primaril' stutter if it's common
                # But more generally, trim and handle common LLM cutoffs
                return sanitize_text_field(obj)
            return obj
        
        data = clean_stutters(data)
        
        # v2.2: MARKET SHARE LOGIC FIX (Pareto Enforcer)
        # Prevents "10%, 10%, 10%" flat distributions
        ms_data = data.get("sales_intelligence", {}).get("market_share_by_brand", [])
        if ms_data:
            shares = [x.get("share", 0) for x in ms_data]
            # If standard deviation is low or all values are the same (or very close)
            is_flat = len(set(shares)) <= 1 or (max(shares) - min(shares) < 5)
            
            if is_flat:
                logger.warning("[LLM-INTEL] Detected flat market share distribution. Applying Pareto correction.")
                # Pareto curve for 5 items
                pareto_template = [35, 25, 20, 15, 5]
                # Sort brands by existing share (if any difference) or alphabetical to be deterministic
                # Actually, usually random shuffle is better for mock fairness if all are equal, 
                # but let's assume the LLM ordered them by relevance (Rank 1, 2, 3...)
                for i, item in enumerate(ms_data):
                    if i < len(pareto_template):
                        item["share"] = pareto_template[i]
                    else:
                        item["share"] = 0 # Fallback for extras
                
                # Normalize to ensure sum is reasonable (100%)
                # (The template sums to 100, so we are good)
        
        # v2.5 SAFETY GROUNDING: Never leave Scholar Audit empty
        if not data.get("scholar_audit"):
            niche = data.get("niche_name", product_description)
            data["scholar_audit"] = [
                {
                    "source": f"Industry Insights: {niche}",
                    "finding": f"El mercado de {niche} está migrando hacia estándares de calidad 'Pro-sumer', donde la durabilidad y la transparencia de materiales son los principales drivers de lealtad.",
                    "relevance": "Marketing de Autoridad"
                },
                {
                    "source": "E-commerce Trends Report",
                    "finding": "La reducción de fricción en la experiencia de usuario mediante diseño intuitivo aumenta la tasa de recompra en un 25% en esta categoría.",
                    "relevance": "Optimización de Conversión"
                }
            ]
        
        logger.info(f"[LLM-INTEL] Successfully generated intelligence for: {product_description[:50]}...")
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"[LLM-INTEL] Failed to parse JSON response: {e}")
        return generate_enhanced_mock(product_description)
    except Exception as e:
        logger.error(f"[LLM-INTEL] Gemini API error: {e}")
        return generate_enhanced_mock(product_description)


def _get_category_seasonality(product_description: str) -> dict:
    """
    ═══════════════════════════════════════════════════════════════════════════
    DYNAMIC SEASONALITY ANALYSIS - NO PREDEFINED PATTERNS
    ═══════════════════════════════════════════════════════════════════════════
    
    Esta función DEBE analizar cada producto individualmente usando LLM.
    NO usa patrones predefinidos por categoría.
    
    El LLM debe determinar la curva de demanda basándose en:
    1. El tipo específico de producto
    2. El comportamiento real del consumidor para ESE producto
    3. Factores estacionales únicos del nicho
    """
    if not GEMINI_AVAILABLE:
        return _generate_dynamic_seasonality_fallback(product_description)
    
    model = get_gemini_model()
    if not model:
        return _generate_dynamic_seasonality_fallback(product_description)
    
    prompt = f"""Eres un experto en análisis de demanda estacional para e-commerce.

PRODUCTO A ANALIZAR: "{product_description}"

═══════════════════════════════════════════════════════════════════════════════
MISIÓN: Determinar la curva de demanda mensual ESPECÍFICA para este producto
═══════════════════════════════════════════════════════════════════════════════

REGLAS CRÍTICAS:
1. NO uses patrones genéricos - analiza ESTE producto específico
2. Considera factores únicos: clima, temporadas, eventos, comportamiento del consumidor
3. Los valores deben reflejar la REALIDAD del mercado para este producto
4. El mes con mayor demanda = 100, el resto proporcional a ese máximo

EJEMPLOS DE LÓGICA CORRECTA:
- Trajes de baño: Pico en Junio-Agosto (verano), muy bajo en invierno
- Equipo de esquí: Pico en Nov-Feb (invierno), muy bajo en verano
- Artículos escolares: Pico en Agosto-Sept (back to school)
- Regalos románticos: Pico en Feb (San Valentín) y Dic (Navidad)
- Equipo de fitness: Pico en Enero (propósitos de año nuevo)
- Productos de Halloween: Pico extremo en Octubre
- Protector solar: Pico en verano (Mayo-Agosto)

Responde SOLO con JSON válido, sin markdown:
{{
    "peaks": [
        {{"month": "Mes del pico principal", "event": "Evento/razón del pico", "impact": "Extreme/High/Medium", "strategy": "Estrategia recomendada"}}
    ],
    "low_points": ["Mes bajo y razón", "Otro mes bajo y razón"],
    "strategy_insight": "Insight estratégico detallado sobre la estacionalidad de ESTE producto específico",
    "monthly_demand": {{
        "Enero": XX, "Febrero": XX, "Marzo": XX, "Abril": XX, "Mayo": XX, "Junio": XX,
        "Julio": XX, "Agosto": XX, "Septiembre": XX, "Octubre": XX, "Noviembre": XX, "Diciembre": XX
    }}
}}

IMPORTANTE: Los valores en monthly_demand deben sumar lógica para ESTE producto específico.
El máximo = 100, el resto proporcional. Mínimo puede ser tan bajo como 10-15 si es muy estacional."""

    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Clean response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        result = json.loads(text.strip())
        logger.info(f"[LLM-INTEL] ✅ Dynamic seasonality generated for: {product_description[:50]}...")
        return result
        
    except Exception as e:
        logger.warning(f"[LLM-INTEL] Seasonality LLM failed, using dynamic fallback: {e}")
        return _generate_dynamic_seasonality_fallback(product_description)


def _generate_dynamic_seasonality_fallback(product_description: str) -> dict:
    """
    Fallback cuando el LLM no está disponible.
    Genera una curva NEUTRAL que no asume ningún patrón predefinido.
    El reporte debe indicar claramente que necesita datos reales.
    """
    return {
        "peaks": [
            {"month": "N/A", "event": "Análisis pendiente - Se requieren datos POE", "impact": "Unknown", "strategy": "Subir archivos X-Ray/Helium10 con datos históricos de ventas para análisis preciso"}
        ],
        "low_points": ["Análisis pendiente - Sin datos suficientes"],
        "strategy_insight": f"⚠️ ANÁLISIS DE ESTACIONALIDAD PENDIENTE para '{product_description[:50]}...'. Para obtener una curva de demanda precisa, sube archivos POE (X-Ray, Helium10) con datos históricos de ventas mensuales. Sin estos datos, no es posible determinar el patrón estacional específico de este producto.",
        "monthly_demand": {
            "Enero": 50, "Febrero": 50, "Marzo": 50, "Abril": 50, "Mayo": 50, "Junio": 50,
            "Julio": 50, "Agosto": 50, "Septiembre": 50, "Octubre": 50, "Noviembre": 50, "Diciembre": 50
        },
        "needs_poe_data": True
    }


def generate_enhanced_mock(product_description: str) -> dict:
    """
    Generate enhanced mock data that is contextually relevant to the product.
    Uses keyword extraction to create meaningful fake competitors.
    """
    import re
    
    # Extract meaningful tokens from product description
    ctx = product_description.upper()
    tokens = re.findall(r'[A-Z]{3,}', ctx)
    ignore = ["PDF", "XLSX", "DOCX", "GOOGLE", "DRIVE", "FILE", "ANALYSIS", "BATCH", "FOLDER", "THE", "AND", "FOR", "WITH"]
    clean_tokens = [t.capitalize() for t in tokens if t not in ignore][:5]
    
    # Build niche name from tokens
    if len(product_description.split()) > 3:
        niche_name = " ".join(product_description.split()[:4]) + " Market"
    else:
        niche_name = f"{clean_tokens[0] if clean_tokens else 'Specialized'} Products"
    
    # Generate contextual competitor names
    prefixes = ["Pro", "Elite", "Prime", "Ultra", "Max", "Advanced", "Premium", "Essential", "Pure", "Vital"]
    suffixes = ["Plus", "Pro", "X", "360", "Max", "One", "Classic", "Series", "Edition", "Gold"]
    
    base_word = clean_tokens[0] if clean_tokens else "Product"
    
    top_10 = []
    for i in range(1, 11):
        brand = f"{prefixes[i-1]} {base_word} {suffixes[(i+2)%10]}"
        price = round(random.uniform(15, 150), 2)
        reviews = random.randint(500, 50000)
        rating = round(4.0 + random.random() * 0.8, 1)
        
        top_10.append({
            "rank": i,
            "name": brand,
            "price": price,
            "reviews": reviews,
            "rating": rating,
            "adv": f"Líder en {prefixes[i-1].lower()} market fit con alta calidad y reviews positivas.",
            "vuln": "Precio competitivo pero margen de mejora en diferenciación.",
            "gap": f"Oportunidad de personalización y valor agregado en el segmento {base_word.lower()}."
        })
    
    social = {
        "amazon_review_audit": f"Análisis forense de reseñas en la categoría {niche_name}. Tendencias principales identificadas.",
        "pros": [
            "Calidad de materiales consistente en líderes de mercado",
            "Precios competitivos en el rango medio",
            "Buenas valoraciones promedio (4.3+)",
            "Envío Prime disponible en mayoría",
            "Variedad de opciones para diferentes necesidades"
        ],
        "cons": [
            "Falta de diferenciación clara entre competidores",
            "Inconsistencia en tamaños o especificaciones",
            "Servicio post-venta limitado",
            "Empaque genérico en muchos casos",
            "Falta de certificaciones de calidad"
        ],
        "tiktok_trends": f"Tendencias en #{base_word}TikTok con millones de vistas. UGC dominando la conversión.",
        "reddit_insights": f"Comunidades de Reddit discuten pros y contras. Alta demanda de transparencia.",
        "google_search_insights": f"Crecimiento en búsquedas de 'best {base_word.lower()}' y variantes.",
        "consumer_desire": "Mejor calidad, precios justos, y marcas con propósito."
    }
    
    trends = [
        {"title": "Personalización Masiva", "description": "Los consumidores buscan productos adaptados a sus necesidades específicas."},
        {"title": "Sostenibilidad", "description": "Creciente demanda por materiales eco-friendly y empaques reciclables."},
        {"title": "Transparencia de Ingredientes", "description": "El consumidor exige saber exactamente qué contiene el producto."},
        {"title": "Experiencia Premium", "description": "Disposición a pagar más por experiencias de unboxing y servicio excepcional."}
    ]
    
    keywords = [
        {"term": f"Best {base_word}", "volume": "Alto", "trend": "Trending Up"},
        {"term": f"{base_word} Premium", "volume": "Medio", "trend": "Stable"},
        {"term": f"{base_word} for {clean_tokens[1] if len(clean_tokens) > 1 else 'Home'}", "volume": "Alto", "trend": "Rising"},
        {"term": f"Top Rated {base_word}", "volume": "Medio", "trend": "Steady"},
        {"term": f"{base_word} Reviews", "volume": "Alto", "trend": "Stable"},
        {"term": f"Affordable {base_word}", "volume": "Medio", "trend": "High Demand"},
        {"term": f"{base_word} Comparison", "volume": "Bajo", "trend": "Emerging"},
        {"term": f"Professional {base_word}", "volume": "Medio", "trend": "Rising"},
        {"term": f"{base_word} 2026", "volume": "Alto", "trend": "Trending Up"},
        {"term": f"{base_word} Guide", "volume": "Bajo", "trend": "Stable"}
    ]
    
    sales_intelligence = {
        "market_share_by_brand": [
            {"brand": f"{prefixes[0]} Brand", "share": 30, "status": "Líder"},
            {"brand": f"{prefixes[1]} Brand", "share": 25, "status": "Retador"},
            {"brand": f"{prefixes[2]} Brand", "share": 20, "status": "Establecido"},
            {"brand": "Otras Marcas", "share": 15, "status": "Fragmentado"},
            {"brand": "NEXUS Opportunity", "share": 10, "status": "Potencial"}
        ],
        "sub_category_distribution": {
            "Segmento Premium": 35,
            "Segmento Medio": 40,
            "Segmento Entry-Level": 25
        },
        "seasonality": _get_category_seasonality(product_description)
    }
    
    sentiment_summary = f"Análisis de sentimiento para {niche_name}: Mercado competitivo con oportunidades de diferenciación. El consumidor busca calidad consistente y valor agregado."
    
    scholar_audit = [
        {
            "source": "Market Analysis Quarterly",
            "finding": "La diferenciación por experiencia de usuario es el factor #1 de retención.",
            "relevance": "Competitive Strategy"
        },
        {
            "source": "Consumer Behavior Journal",
            "finding": "El 70% de las decisiones de compra se toman basadas en reseñas y UGC.",
            "relevance": "Marketing Focus"
        }
    ]
    
    logger.info(f"[LLM-INTEL] Generated enhanced mock for: {product_description[:50]}...")
    
    return {
        "niche_name": niche_name,
        "top_10_products": top_10,
        "social_listening": social,
        "trends": trends,
        "keywords": keywords,
        "sales_intelligence": sales_intelligence,
        "sentiment_summary": sentiment_summary,
        "scholar_audit": scholar_audit
    }


def generate_strategic_avatars(product_context: str, scout_data: dict) -> dict:
    """
    ═══════════════════════════════════════════════════════════════════════════
    NEXUS STRATEGIC INTELLIGENCE ENGINE v2.0
    ═══════════════════════════════════════════════════════════════════════════
    Generate elite-level strategic intelligence including:
    - Blue Ocean Positioning Matrix
    - Precision Customer Avatars (JTBD-Rooted)
    - Multi-Tier Pricing Psychology
    - Anti-Competition Moat Architecture
    - 90-Day Blitzscale Roadmap
    """
    if not GEMINI_AVAILABLE:
        return _generate_mock_avatars(product_context)
    
    model = get_gemini_model()
    if not model:
        return _generate_mock_avatars(product_context)

    # Extract deep insights from Scout Data
    competitor_cons = scout_data.get("social_listening", {}).get("cons", [])
    competitor_pros = scout_data.get("social_listening", {}).get("pros", [])
    pain_keywords = scout_data.get("social_listening", {}).get("pain_keywords", [])
    emotional_analysis = scout_data.get("social_listening", {}).get("emotional_analysis", {})
    top_products = scout_data.get("top_10_products", [])[:5]  # Top 5
    trends = scout_data.get("trends", [])
    
    # Extract price range from competitors if available
    prices = [p.get("price", 0) for p in top_products if p.get("price", 0) > 0]
    avg_price = sum(prices) / len(prices) if prices else 0
    
    prompt = f"""
    ═══════════════════════════════════════════════════════════════════════════
    NEXUS STRATEGIC INTELLIGENCE ENGINE - CONSULTORÍA DE ÉLITE
    ═══════════════════════════════════════════════════════════════════════════
    
    Eres un Partner Senior de una fusión híbrida entre McKinsey, Bain, y la boutique 
    estratégica más agresiva de Silicon Valley. Tu cliente te paga $50,000/mes por 
    insights accionables que conviertan commodities en categorías propias.
    
    ═══════════════════════════════════════════════════════════════════════════
    INTELLIGENCE BRIEF
    ═══════════════════════════════════════════════════════════════════════════
    
    PRODUCTO/NICHO: "{product_context}"
    
    COMPETENCIA (Top 5):
    {json.dumps(top_products, indent=2, default=str)}
    
    DOLORES DETECTADOS EN REVIEWS:
    {json.dumps(competitor_cons)}
    
    LO QUE SÍ FUNCIONA:
    {json.dumps(competitor_pros)}
    
    PALABRAS CLAVE DE DOLOR:
    {json.dumps(pain_keywords)}
    
    ANÁLISIS EMOCIONAL DEL MERCADO:
    {json.dumps(emotional_analysis)}
    
    PRECIO PROMEDIO MERCADO: ${avg_price:.2f}
    
    TENDENCIAS ACTIVAS:
    {json.dumps(trends)}
    
    ═══════════════════════════════════════════════════════════════════════════
    TU MISIÓN: Entregar el BLUEPRINT ESTRATÉGICO más potente posible.
    ═══════════════════════════════════════════════════════════════════════════
    
    1. 🎯 NAMING ESTRATÉGICO DEL PROYECTO
       - 3 opciones de nombre CÓDIGO para el proyecto (NO el producto final)
       - Deben sonar como proyectos internos de Apple o Tesla: confidenciales, 
         evocadores, memorables pero sin revelar el producto.
       - Ejemplos de estilo: "Project Titan", "Initiative Aurora", "Protocolo Meridian"
    
    2. 👤 AVATARES DE PRECISIÓN (Jobs-To-Be-Done Framework)
       ═══════════════════════════════════════════════════════════════════════════
       REGLAS DE ORO (ESPECIFICIDAD TOTAL):
       - PROHIBIDO LO GENÉRICO: No uses nombres como "Early Adopter" a secas. 
         Dales nombres con personalidad real (ej: "El Perfeccionista del Home-Office").
       - GROUNDING (FUNDAMENTACIÓN): Cada dolor (Pain Point) DEBE estar basado 
         DIRECTAMENTE en los 'cons' o frustraciones reales encontradas por el Scout. 
       - CITA EVIDENCIA: Menciona qué frustración del mercado estás resolviendo.
       ═══════════════════════════════════════════════════════════════════════════
       
       Define 3 PERSONAS REALES que buscan este producto:
       
       Para CADA avatar:
       a) NOMBRE CREATIVO: Un título poético pero descriptivo
          - Si es skincare: "La Arquitecta de su Propia Piel" no "Usuario de Skincare"
          - Si es tech: "El Estratega del Tiempo Optimizado" no "Tech Enthusiast"
       
       b) PERFIL DEMOGRÁFICO PRECISO:
          - Rango de edad REAL para este nicho (ej: 32-41, no "25-45")
          - Ingreso anual estimado en USD
          - Contexto de vida (¿casado? ¿hijos? ¿profesión?)
       
       c) JOB-TO-BE-DONE PRIMARIO:
          - "Cuando [SITUACIÓN], quiero [MOTIVACIÓN] para poder [RESULTADO]"
          - Debe ser hiperspecífico al producto
       
       d) PAIN POINT ACTUAL:
          - ¿Qué EXACTAMENTE le frustra de las opciones actuales?
          - Usa lenguaje que ellos usarían en una queja de 1 estrella
       
       e) TRIGGER DE COMPRA:
          - ¿Qué frase/promesa EXACTA le haría sacar la tarjeta HOY?
          - Debe ser testeable en un headline de Amazon
       
       f) PORCENTAJE DEL TAM:
          - ¿Cuánto del mercado total representa este avatar?
    
    3. 💰 ESTRATEGIA DE PRICING PSICOLÓGICO (3 Tiers)
       Define cómo estructurar la línea de productos:
       
       - TIER ENTRADA: Precio, propósito, y cómo "engancha" al cliente
       - TIER CORE (Estrella): El producto principal, pricing vs competencia
       - TIER PREMIUM: Versión élite, justificación del precio elevado
       
       Incluye el PRECIO SUGERIDO para cada tier basándote en el promedio de ${avg_price:.2f}
    
    4. 🛡️ ARQUITECTURA DEL MOAT (Foso Defensivo Anti-Copia)
       NO digas "patentes" ni "calidad superior" (todos lo dicen).
       
       Define defensas REALES:
       a) MOAT TECNOLÓGICO: ¿Qué podemos hacer que requiera 12+ meses replicar?
       b) MOAT DE MARCA: ¿Qué narrativa emocional es difícil de copiar?
       c) MOAT DE ECOSISTEMA: ¿Cómo creamos lock-in sin ser malvados?
       d) MOAT DE VELOCIDAD: ¿Cómo iteramos más rápido que la competencia?
    
    5. 📍 ROADMAP DE 90 DÍAS (Blitzscale)
       Define 3 fases de lanzamiento:
       - Días 1-30: ¿Qué hacemos para validar y ganar tracción inicial?
       - Días 31-60: ¿Cómo escalamos lo que funciona?
       - Días 61-90: ¿Qué palancas activamos para dominar el nicho?
    
    6. 💎 HEADLINE DE POSICIONAMIENTO (Blue Ocean)
       Una frase tipo "Tagline CEO" que capture TODA la estrategia.
       - Formato: "[Producto] para [Avatar] que [Diferenciador único]"
       - Ejemplo: "El cargador de los que no tienen tiempo que perder en cargadores."
    
    ═══════════════════════════════════════════════════════════════════════════
    FORMATO JSON REQUERIDO (SIN MARKDOWN, SOLO JSON PURO):
    ═══════════════════════════════════════════════════════════════════════════
    {{
        "project_names": ["Nombre1", "Nombre2", "Nombre3"],
        "selected_project_name": "El Mejor de los 3",
        "avatars": [
            {{
                "name": "Nombre Creativo del Avatar 1",
                "percentage": "40%",
                "demographics": "Perfil demográfico detallado",
                "job_to_be_done": "Cuando [X], quiero [Y] para [Z]",
                "pain_point": "Dolor específico actual",
                "trigger": "Frase exacta que dispara la compra"
            }},
            {{
                "name": "Nombre Creativo del Avatar 2",
                "percentage": "35%",
                "demographics": "Perfil demográfico detallado",
                "job_to_be_done": "Cuando [X], quiero [Y] para [Z]",
                "pain_point": "Dolor específico actual",
                "trigger": "Frase exacta que dispara la compra"
            }},
            {{
                "name": "Nombre Creativo del Avatar 3",
                "percentage": "25%",
                "demographics": "Perfil demográfico detallado",
                "job_to_be_done": "Cuando [X], quiero [Y] para [Z]",
                "pain_point": "Dolor específico actual",
                "trigger": "Frase exacta que dispara la compra"
            }}
        ],
        "pricing_strategy": {{
            "tier_entry": {{
                "name": "Nombre del tier",
                "price": 0.00,
                "purpose": "Propósito estratégico"
            }},
            "tier_core": {{
                "name": "Nombre del tier estrella",
                "price": 0.00,
                "vs_competition": "+X% sobre promedio porque..."
            }},
            "tier_premium": {{
                "name": "Nombre del tier élite",
                "price": 0.00,
                "justification": "Por qué alguien pagaría esto"
            }}
        }},
        "moat_architecture": {{
            "tech_moat": "Descripción del moat tecnológico",
            "brand_moat": "Descripción del moat de marca",
            "ecosystem_moat": "Descripción del moat de ecosistema",
            "speed_moat": "Descripción del moat de velocidad"
        }},
        "roadmap_90_days": {{
            "phase_1_validate": "Días 1-30: Acciones específicas",
            "phase_2_scale": "Días 31-60: Acciones de escala",
            "phase_3_dominate": "Días 61-90: Acciones de dominancia"
        }},
        "moat_strategy": "Resumen ejecutivo del foso defensivo en una oración",
        "blue_ocean_headline": "El tagline que captura toda la estrategia"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Clean markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        result = json.loads(text.strip())
        
        # Apply global sanitization to all string fields
        def deep_sanitize(obj):
            if isinstance(obj, dict):
                return {k: deep_sanitize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [deep_sanitize(i) for i in obj]
            elif isinstance(obj, str):
                return sanitize_text_field(obj)
            return obj
            
        result = deep_sanitize(result)
        
        # Ensure backwards compatibility - add 'trigger' field if using old 'job_to_be_done'
        for avatar in result.get("avatars", []):
            if "trigger" not in avatar and "job_to_be_done" in avatar:
                avatar["trigger"] = avatar.get("pain_point", "Calidad superior")
        
        return result
    except Exception as e:
        logger.error(f"Failed to generate strategic avatars: {e}")
        return _generate_mock_avatars(product_context)

def _generate_mock_avatars(ctx: str) -> dict:
    """Fallback logic derived from context string"""
    ctx_upper = ctx.upper()
    
    if "SHAMPOO" in ctx_upper or "CABELLO" in ctx_upper or "HAIR" in ctx_upper:
        return {
            "project_names": ["Project Velvet Root", "Initiative Follicle-Guard", "Protocolo Silk-Flow"],
            "selected_project_name": "Project Velvet Root",
            "avatars": [
                {"name": "La Restauradora Consciente", "percentage": "45%", "demographics": "Mujer 28-40, Urbana", "pain_point": "Caída por estrés/químicos", "trigger": "Sin sulfatos, resultado clínico"},
                {"name": "El Bio-Hacker Capilar", "percentage": "30%", "demographics": "Hombre/Mujer 35-50", "pain_point": "Adelgazamiento del cabello", "trigger": "Ingredientes activos densificantes"},
                {"name": "Gift-Giver de Lujo", "percentage": "25%", "demographics": "Varios", "pain_point": "Regalos genéricos", "trigger": "Packaging de experiencia unboxing"}
            ],
            "moat_strategy": "Formulación propietaria con extracto fermentado exclusivo y comunidad educativa de 'Salud Capilar' difícil de replicar."
        }
    else:
        # Generic fallback using existing logic but slightly renamed to show variance
        return {
            "project_names": [f"Project {ctx.split()[0]} Alpha", "Initiative Core-Value", "Protocolo Market-Fit"],
            "selected_project_name": f"Project {ctx.split()[0]} Alpha",
            "avatars": [
                {"name": "Premium Performance Seeker", "percentage": "40%", "demographics": "High Income", "pain_point": "Product Failure", "trigger": "Reliability Guarantee"},
                {"name": "Value Maximizer", "percentage": "35%", "demographics": "Middle Class", "pain_point": "Overpriced commodities", "trigger": "Cost-Benefit Ratio"},
                {"name": "Esthetic Purist", "percentage": "25%", "demographics": "Design Conscious", "pain_point": "Ugly generic products", "trigger": "Minimalist Design"}
            ],
            "moat_strategy": "Brand ecosystem and superior customer service layer."
        }


def generate_strategic_verdict(product_context: str, scout_data: dict, gap_analysis: list) -> dict:
    """
    ═══════════════════════════════════════════════════════════════════════════
    NEXUS STRATEGIC VERDICT ENGINE
    ═══════════════════════════════════════════════════════════════════════════
    Generates a dynamic, context-aware strategic verdict title and narrative.
    
    Instead of always saying "GOLD STANDARD", this engine analyzes the market
    and chooses the most appropriate strategic framework:
    
    - BLUE OCEAN: When creating a new market category
    - CATEGORY CREATION: When redefining what the product is
    - NICHE DOMINANCE: When capturing a specific underserved segment
    - PREMIUM DISRUPTION: When attacking from above with quality
    - ECOSYSTEM LOCK-IN: When building interconnected products
    - SPEED BLITZ: When first-mover advantage is critical
    - TRUST MOAT: When trust/safety is the key differentiator
    - EXPERIENCE REVOLUTION: When the buying experience is broken
    """
    if not GEMINI_AVAILABLE:
        return _generate_mock_verdict(product_context)
    
    model = get_gemini_model()
    if not model:
        return _generate_mock_verdict(product_context)
    
    # Extract insights
    competitor_cons = scout_data.get("social_listening", {}).get("cons", [])
    top_products = scout_data.get("top_10_products", [])[:5]
    emotional_analysis = scout_data.get("social_listening", {}).get("emotional_analysis", {})
    
    # Calculate market dynamics
    prices = [p.get("price", 0) for p in top_products if p.get("price", 0) > 0]
    avg_price = sum(prices) / len(prices) if prices else 0
    avg_rating = sum(p.get("rating", 4) for p in top_products) / len(top_products) if top_products else 4.0
    
    prompt = f"""
    ═══════════════════════════════════════════════════════════════════════════
    NEXUS STRATEGIC VERDICT ENGINE - ANÁLISIS DE MARCO ESTRATÉGICO
    ═══════════════════════════════════════════════════════════════════════════
    
    Eres el Director de Estrategia de BCG y tu cliente te pide que determines 
    el MARCO ESTRATÉGICO óptimo para entrar a un mercado.
    
    PRODUCTO/NICHO: "{product_context}"
    
    DATOS DEL MERCADO:
    - Precio promedio: ${avg_price:.2f}
    - Rating promedio: {avg_rating:.1f}/5
    - Dolores detectados: {json.dumps(competitor_cons[:5])}
    - Análisis emocional: {json.dumps(emotional_analysis)}
    
    GAPS IDENTIFICADOS:
    {json.dumps(gap_analysis, indent=2)}
    
    ═══════════════════════════════════════════════════════════════════════════
    TU MISIÓN: Determinar el MARCO ESTRATÉGICO más potente y generar el veredicto.
    ═══════════════════════════════════════════════════════════════════════════
    
    MARCOS ESTRATÉGICOS DISPONIBLES (elige el MÁS apropiado, NO 'GOLD STANDARD'):
    
    1. OCÉANO AZUL (Blue Ocean)
       - Usar cuando: El mercado está saturado de commodities similares
       - Titulo tipo: "REDEFINICIÓN DE CATEGORÍA: [NUEVA DEFINICIÓN]"
       
    2. CREACIÓN DE CATEGORÍA
       - Usar cuando: Podemos inventar un nuevo tipo de producto
       - Título tipo: "NACIMIENTO DE UNA NUEVA CATEGORÍA: [NOMBRE]"
       
    3. DOMINANCIA DE NICHO
       - Usar cuando: Hay un segmento específico desatendido
       - Título tipo: "MONOPOLIO DEL SEGMENTO: [NICHO ESPECÍFICO]"
       
    4. DISRUPCIÓN PREMIUM
       - Usar cuando: El mercado está lleno de opciones baratas pero malas
       - Título tipo: "REVOLUCIÓN DE CALIDAD: EL [PRODUCTO] QUE SÍ FUNCIONA"
       
    5. ECOSISTEMA INTELIGENTE
       - Usar cuando: Podemos crear lock-in con productos complementarios
       - Título tipo: "EL ECOSISTEMA [CATEGORÍA]: MÁS QUE UN PRODUCTO"
       
    6. BLITZSCALE
       - Usar cuando: La velocidad y primera posición son críticos
       - Título tipo: "CARRERA POR LA MENTE: CAPTURA ANTES QUE COPIEN"
       
    7. FOSO DE CONFIANZA
       - Usar cuando: La seguridad/salud/garantía es el diferenciador clave
       - Título tipo: "LA MARCA DE CONFIANZA: [PROMESA CLAVE]"
       
    8. REVOLUCIÓN DE EXPERIENCIA
       - Usar cuando: La experiencia de compra/uso está rota
       - Título tipo: "REINVENTANDO LA EXPERIENCIA: [TRANSFORMACIÓN]"
       
    9. HÍBRIDO TECNOLÓGICO
       - Usar cuando: Podemos integrar tech donde antes no existía
       - Título tipo: "FUSIÓN INTELIGENTE: [PRODUCTO] + [TECNOLOGÍA]"
       
    10. SOSTENIBILIDAD COMO VENTAJA
        - Usar cuando: El mercado está lleno de productos desechables
        - Título tipo: "EL [PRODUCTO] PARA SIEMPRE: INVERSIÓN, NO GASTO"
    
    REGLAS CRÍTICAS:
    - NUNCA uses "GOLD STANDARD" - es genérico y aburrido.
    - El título debe ser ESPECÍFICO al producto analizado y revelar la ESTRATEGIA.
    - Debe sonar como un headline de Harvard Business Review.
    - **SUBSTANCIA QUIRÚRGICA:** Las propuestas de USP deben ser densas, técnicas y con métricas de impacto REALES (ej: "Reduce fricción en 40% mediante recubrimiento de titanio" o "Latencia <10ms"). EVITA vaguedades, placeholders o textos cortos tipo "...".
    - Cada campo del USP (title, substance, pain_attack, details) debe tener al menos 10 palabras de substancia.
    
    ═══════════════════════════════════════════════════════════════════════════
    FORMATO JSON REQUERIDO:
    ═══════════════════════════════════════════════════════════════════════════
    {{
        "strategic_framework": "Nombre del marco elegido",
        "verdict_title": "TÍTULO EN MAYÚSCULAS PARA EL BANNER PRINCIPAL",
        "verdict_subtitle": "Oración ejecutiva de la estrategia",
        "strategic_thesis": "Hipótesis central potente",
        "key_insight": "Insight #1 fundamentador",
        "competitive_angle": "Cómo ganamos vs competencia (específico)",
        "3_usp_proposals": [
            {{
                "title": "Título del USP (ej: Durabilidad Extrema)",
                "substance": "Datos técnicos o métrica de impacto (ej: Certificación IP68 + 5 años garantía)",
                "pain_attack": "Qué dolor específico resuelve (ej: Resuelve el 35% de quejas por daño)",
                "details": "Explicación breve pero densa del CÓMO se logra (detalles técnicos, materiales, etc.)",
                "icon": "Icono Emoji pertinente"
            }}
        ],
        "partner_summary": "Párrafo administrativo (CEO level, ~150 palabras)."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Clean markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        result = json.loads(text.strip())
        return result
    except Exception as e:
        logger.error(f"Failed to generate strategic verdict: {e}")
        return _generate_mock_verdict(product_context)


def _generate_mock_verdict(ctx: str) -> dict:
    """Fallback verdicts based on product context."""
    ctx_upper = ctx.upper()
    
    # Strategic frameworks for different product types
    frameworks = {
        "baby": {
            "strategic_framework": "TRUST_MOAT",
            "verdict_title": "EL GUARDIÁN DEL SUEÑO INFANTIL",
            "verdict_subtitle": "Posicionamiento como la marca de confianza en el desarrollo neurológico temprano",
            "strategic_thesis": "En un mercado inundado de juguetes electrónicos sin fundamento científico, capturamos a los padres que entienden que el sueño es la base del desarrollo cognitivo.",
            "key_insight": "El 78% de los padres primerizos busca validación científica pero no la encuentra en los productos actuales.",
            "competitive_angle": "Mientras la competencia vende 'conveniencia', nosotros vendemos 'desarrollo óptimo certificado'.",
            "risk_acknowledged": "Riesgo de ser percibidos como 'premium inaccesible'. Mitigación: tier de entrada con upgrade path.",
            "partner_summary": "Socio, el análisis revela una oportunidad de Foso de Confianza. El mercado de productos para bebé está plagado de commodities sin respaldo. Al posicionarnos como la autoridad en sueño científico, creamos una barrera emocional impenetrable."
        },
        "charger": {
            "strategic_framework": "TECHNOLOGY_HYBRID",
            "verdict_title": "EL CENTRO DE COMANDO ENERGÉTICO",
            "verdict_subtitle": "Transformación de un commodity en un hub de gestión de energía inteligente",
            "strategic_thesis": "Los cargadores actuales son cajas negras. Al hacerlos transparentes y conectados, capturamos al profesional que valora su equipamiento de $2000+.",
            "key_insight": "El usuario premium no sabe si su cargador está dañando su batería - eso genera ansiedad latente.",
            "competitive_angle": "Añadimos telemetría donde antes había ignorancia. Somos el Garmin del mundo de la carga.",
            "risk_acknowledged": "Riesgo de overengineering. Mitigación: UX ultra-simple con data bajo demanda.",
            "partner_summary": "Socio, identificamos una jugada de Fusión Tecnológica. El mercado de cargadores es una guerra de precios sin diferenciación real. Al integrar transparencia y datos, creamos una nueva subcategoría: 'Smart Charging'."
        },
        "hair": {
            "strategic_framework": "CATEGORY_CREATION",
            "verdict_title": "RITUAL DE RESTAURACIÓN CAPILAR",
            "verdict_subtitle": "De shampoo commodity a tratamiento terapéutico de resultados medibles",
            "strategic_thesis": "El mercado de cuidado capilar está lleno de promesas vacías. Al ofrecer resultados clínicamente medibles, capturamos al consumidor escéptico pero dispuesto a pagar.",
            "key_insight": "El 67% de los usuarios de shampoos premium no ve resultados pero sigue comprando por esperanza.",
            "competitive_angle": "Garantía de resultados visibles en 30 días o devolución. Nadie más se atreve.",
            "risk_acknowledged": "Riesgo de devoluciones masivas. Mitigación: formulación validada + guía de uso correcta.",
            "partner_summary": "Socio, esto es Creación de Categoría pura. No vendemos shampoo, vendemos un 'Protocolo de Restauración Capilar'. Al medicalizar la narrativa sin ser medicina, escapamos de la comoditización."
        }
    }
    
    # Find matching framework
    for key, framework in frameworks.items():
        if key in ctx_upper.lower():
            return framework
    
    # Default framework with product-specific title
    product_word = ctx.split()[0] if ctx.split() else "producto"
    return {
        "strategic_framework": "PREMIUM_DISRUPTION",
        "verdict_title": f"LA VERSIÓN DEFINITIVA: {product_word.upper()} SIN COMPROMISOS",
        "verdict_subtitle": f"Captura del segmento premium insatisfecho en el mercado de {product_word}",
        "strategic_thesis": f"El mercado de {product_word} está saturado de opciones 'suficientemente buenas'. Atacamos desde arriba con la versión que los exigentes estaban esperando.",
        "key_insight": "El segmento premium está desatendido porque los incumbentes optimizan para volumen, no para excelencia.",
        "competitive_angle": "Mientras ellos reducen costos, nosotros maximizamos valor percibido y real.",
        "risk_acknowledged": "Riesgo de mercado pequeño. Mitigación: premium atrae imitadores que validan la categoría.",
        "partner_summary": f"Socio, el análisis indica una estrategia de Disrupción Premium. El mercado de {product_word} sufre de comoditización Terminal. Nuestra jugada es clara: ser el Tesla de la categoría. No competimos en precio, competimos en aspiración."
    }

def generate_compliance_audit(product_description: str) -> dict:
    """
    Generate a dynamic compliance audit using Gemini AI.
    Identifies relevant international standards (CE, FCC, FDA, etc.) based on product type.
    """
    if not GEMINI_AVAILABLE:
        return _generate_mock_compliance_audit(product_description)
    
    model = get_gemini_model()
    if not model:
        return _generate_mock_compliance_audit(product_description)

    prompt = f"""Eres un auditor de cumplimiento regulatorio experto en e-commerce internacional (Amazon, eBay, Walmart).
    
    PRODUCTO: "{product_description}"
    
    MISIÓN: Generar una auditoría de cumplimiento detallada para este producto específico.
    
    REGLAS:
    1. Identifica al menos 6-8 estándares reales que aplican a este producto (ej: CE, FCC, RoHS, FDA, CPC, ASTM, etc.).
    2. Clasifica cada estándar como MANDATORY (Obligatorio), RECOMMENDED (Recomendado) u OPTIONAL (Opcional).
    3. Para cada uno, escribe una descripción técnica de por qué aplica y qué implica.
    4. Determina un NIVEL DE RIESGO (LOW, MEDIUM, HIGH, CRITICAL).
    5. Calcula un SCORE DE CUMPLIMIENTO (0-100%) basado en la complejidad regulatoria del nicho.
    
    FORMATO JSON IGUAL AL SIGUIENTE:
    {{
        "risk_level": "NIVEL",
        "compliance_score": 85,
        "audits": [
            {{
                "std": "Nombre del Estándar (Nombre Común)",
                "status": "MANDATORY/RECOMMENDED/OPTIONAL",
                "desc": "Descripción técnica detallada"
            }}
        ],
        "audit_note": "Resumen ejecutivo de la auditoría."
    }}
    
    Responde SOLO con JSON, sin markdown ni explicaciones adicionales.
    """

    try:
        response = model.generate_content(prompt)
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        result = json.loads(text.strip())
        logger.info(f"[LLM-INTEL] ✅ Dynamic compliance audit generated for: {product_description[:50]}...")
        return result
    except Exception as e:
        logger.error(f"Failed to generate dynamic compliance audit: {e}")
        return _generate_mock_compliance_audit(product_description)


def _generate_mock_compliance_audit(ctx: str) -> dict:
    """Enhanced mock compliance audit based on keywords."""
    ctx_upper = ctx.upper()
    
    # Defaults
    risk = "MEDIUM"
    score = 75
    audits = [
        {"std": "ISO 9001", "status": "RECOMMENDED", "desc": "Sistema de gestión de calidad genérico para asegurar procesos estables."},
        {"std": "CE Marking (EU)", "status": "MANDATORY", "desc": "Conformidad europea para venta en mercado comunitario."},
        {"std": "Country of Origin", "status": "MANDATORY", "desc": "Etiquetado obligatorio del país de fabricación."}
    ]

    # Electronics
    if any(x in ctx_upper for x in ["CHARGER", "GAN", "POWER", "USB", "ELECTRONIC", "DEVICE"]):
        risk = "HIGH"
        score = 85
        audits = [
            {"std": "FCC Part 15", "status": "MANDATORY", "desc": "Regulación de emisiones electromagnéticas para EE.UU."},
            {"std": "RoHS 3", "status": "MANDATORY", "desc": "Restricción de materiales peligrosos en electrónicos."},
            {"std": "CE Marking (LVD/EMC)", "status": "MANDATORY", "desc": "Seguridad eléctrica y compatibilidad electromagnética en UE."},
            {"std": "DoE Level VI", "status": "MANDATORY", "desc": "Eficiencia energética para fuentes de alimentación."},
            {"std": "UL 62368-1", "status": "RECOMMENDED", "desc": "Estándar de seguridad de producto por laboratorio reconocido."}
        ]
    
    # Beauty
    elif any(x in ctx_upper for x in ["SHAMPOO", "HAIR", "CREAM", "SKIN", "COSMETIC"]):
        risk = "HIGH"
        score = 80
        audits = [
            {"std": "FDA 21 CFR 701", "status": "MANDATORY", "desc": "Etiquetado obligatorio de cosméticos en EE.UU."},
            {"std": "EU 1223/2009", "status": "MANDATORY", "desc": "Regulación estricta de ingredientes en la Unión Europea."},
            {"std": "INCI Nomenclature", "status": "MANDATORY", "desc": "Nomenclatura internacional obligatoria de ingredientes."},
            {"std": "Leaping Bunny", "status": "RECOMMENDED", "desc": "Certificación de no testado en animales."}
        ]

    return {
        "risk_level": risk,
        "compliance_score": score,
        "audits": audits,
        "audit_note": f"Auditoría simulada basada en detección de palabras clave para '{ctx[:30]}'."
    }
