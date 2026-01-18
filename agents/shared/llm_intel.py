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
    
    prompt = f"""Eres un analista de inteligencia de mercado de Amazon experto. Analiza el siguiente producto y genera un análisis competitivo detallado:

PRODUCTO: "{product_description}"

Genera una respuesta JSON con la siguiente estructura EXACTA (todos los textos en español):

{{
    "niche_name": "Nombre de la categoría de mercado",
    "top_10_products": [
        {{
            "rank": 1,
            "name": "Nombre REAL del producto competidor en Amazon",
            "price": 29.99,
            "reviews": 15000,
            "rating": 4.5,
            "adv": "Ventaja competitiva principal del producto",
            "vuln": "Debilidad o punto vulnerable",
            "gap": "Brecha de mercado que no cubre"
        }}
    ],
    "social_listening": {{
        "amazon_review_audit": "Resumen de análisis de reseñas de Amazon",
        "pros": ["Lista de 5 puntos positivos del mercado"],
        "cons": ["Lista de 5 puntos negativos del mercado"],
        "tiktok_trends": "Tendencias relevantes en TikTok",
        "reddit_insights": "Insights de comunidades de Reddit",
        "google_search_insights": "Tendencias de búsqueda en Google",
        "consumer_desire": "Lo que realmente desea el consumidor"
    }},
    "trends": [
        {{
            "title": "Nombre de la tendencia",
            "description": "Descripción detallada de la tendencia"
        }}
    ],
    "keywords": [
        {{
            "term": "Término de búsqueda",
            "volume": "Alto/Medio/Bajo",
            "trend": "Trending Up/Stable/Emerging"
        }}
    ],
    "sales_intelligence": {{
        "market_share_by_brand": [
            {{"brand": "Marca líder", "share": 30, "status": "Líder"}}
        ],
        "sub_category_distribution": {{
            "Subcategoría 1": 40,
            "Subcategoría 2": 30
        }},
        "seasonality": {{
            "peaks": [{{"month": "Diciembre", "event": "Holiday", "impact": "High"}}],
            "low_points": ["Febrero"],
            "strategy_insight": "Insight estratégico de estacionalidad"
        }}
    }},
    "sentiment_summary": "Resumen del sentimiento del mercado",
    "scholar_audit": [
        {{
            "source": "Fuente académica o industrial",
            "finding": "Hallazgo relevante",
            "relevance": "Relevancia para el producto"
        }}
    ]
}}

IMPORTANTE:
- Usa nombres de productos y marcas REALES que existen en Amazon
- Incluye exactamente 10 productos en top_10_products
- Incluye exactamente 4 tendencias
- Incluye exactamente 10 keywords
- Todos los precios en USD
- Sé específico y detallado, no uses placeholders genéricos
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
