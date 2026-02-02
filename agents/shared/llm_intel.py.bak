"""
LLM-Powered Market Intelligence Generator
Uses Google Gemini AI to generate contextual competitive analysis for any product category.
"""
import os
import json
import logging
import random
from datetime import datetime

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


def generate_market_intel(product_description: str) -> dict:
    """
    Generate market intelligence using Gemini AI.
    Falls back to enhanced mock data if LLM is unavailable.
    """
    if not GEMINI_AVAILABLE:
        return generate_enhanced_mock(product_description)
    
    model = get_gemini_model()
    if not model:
        return generate_enhanced_mock(product_description)
    
    prompt = f"""Eres un experto en Social Listening que combina el análisis de datos de Neil Patel con la estrategia de atención de GaryVee.

PRODUCTO A ANALIZAR: "{product_description}"

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
            "strategy_insight": "Insight estratégico detallado de timing"
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
- SÉ EXTREMADAMENTE ESPECÍFICO - evita generalidades
- Usa citas textuales cuando describas frustraciones de usuarios
- Todos los textos en ESPAÑOL
- Responde SOLO con el JSON, sin texto adicional
"""

    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Clean response (remove markdown code blocks if present)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text.strip())
        logger.info(f"[LLM-INTEL] Successfully generated intelligence for: {product_description[:50]}...")
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"[LLM-INTEL] Failed to parse JSON response: {e}")
        return generate_enhanced_mock(product_description)
    except Exception as e:
        logger.error(f"[LLM-INTEL] Gemini API error: {e}")
        return generate_enhanced_mock(product_description)


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
        "seasonality": {
            "peaks": [
                {"month": "Noviembre", "event": "Black Friday", "impact": "Extreme"},
                {"month": "Diciembre", "event": "Holiday Season", "impact": "High"},
                {"month": "Julio", "event": "Prime Day", "impact": "High"}
            ],
            "low_points": ["Enero-Febrero (Post-Holiday)"],
            "strategy_insight": "Concentrar inventario para Q4. Oportunidad en Prime Day para penetración de mercado."
        }
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
