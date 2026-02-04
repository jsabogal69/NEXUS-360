# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS-360: GOOGLE TRENDS INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════
# 
# Fetches real 12-month search interest data from Google Trends
# Uses pytrends library for API access
#
# ═══════════════════════════════════════════════════════════════════════════════

import logging
from datetime import datetime, timedelta

logger = logging.getLogger("TRENDS")

def get_google_trends_data(keywords: list, geo: str = "") -> dict:
    """
    Fetches 12-month Google Trends data for given keywords.
    
    Args:
        keywords: List of search terms (max 5)
        geo: Geographic location (e.g., 'US', 'ES', 'MX'). Empty for worldwide.
    
    Returns:
        dict with:
            - months: List of month labels
            - data: Dict with keyword -> list of values (0-100)
            - status: 'live' or 'simulated'
    """
    try:
        from pytrends.request import TrendReq
        
        # Initialize pytrends
        pytrends = TrendReq(hl='es', tz=360, timeout=(10, 25))
        
        # Limit to 5 keywords (Google Trends API limit)
        keywords = keywords[:5]
        
        # Build payload for last 12 months
        pytrends.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe='today 12-m',
            geo=geo,
            gprop=''
        )
        
        # Get interest over time
        interest_df = pytrends.interest_over_time()
        
        if interest_df.empty:
            logger.warning("[TRENDS] No data returned from Google Trends API")
            return _generate_simulated_data(keywords)
        
        # Process data - aggregate by month
        interest_df = interest_df.drop(columns=['isPartial'], errors='ignore')
        
        # Resample to monthly and get mean
        monthly_df = interest_df.resample('M').mean()
        
        # Get last 12 months
        monthly_df = monthly_df.tail(12)
        
        # Format month labels in Spanish
        month_names = {
            1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
        }
        
        months = [f"{month_names[d.month]} {str(d.year)[2:]}" for d in monthly_df.index]
        
        # Build data dict
        data = {}
        for keyword in keywords:
            if keyword in monthly_df.columns:
                values = monthly_df[keyword].fillna(0).round().astype(int).tolist()
                data[keyword] = values
        
        logger.info(f"[TRENDS] ✅ Fetched live Google Trends data for {len(keywords)} keywords")
        
        return {
            "months": months,
            "data": data,
            "status": "live",
            "source": "Google Trends API",
            "period": "12 meses"
        }
        
    except ImportError:
        logger.warning("[TRENDS] pytrends not installed, using simulated data")
        return _generate_simulated_data(keywords)
    except Exception as e:
        logger.error(f"[TRENDS] Error fetching Google Trends: {e}")
        return _generate_simulated_data(keywords)


def _generate_simulated_data(keywords: list) -> dict:
    """
    Generates simulated trend data when API is unavailable.
    Uses realistic seasonal patterns.
    """
    import random
    
    # Spanish month abbreviations
    month_names = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", 
                   "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    
    # Get current month and generate last 12 months
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    months = []
    for i in range(11, -1, -1):
        month_idx = (current_month - i - 1) % 12
        year = current_year if (current_month - i) > 0 else current_year - 1
        months.append(f"{month_names[month_idx]} {str(year)[2:]}")
    
    # Base seasonal pattern (Q4 spike typical for e-commerce)
    base_pattern = [45, 42, 50, 55, 60, 58, 70, 65, 75, 85, 100, 90]
    
    # Generate data with variation per keyword
    data = {}
    for i, keyword in enumerate(keywords[:5]):
        # Add slight variation per keyword
        variation = random.uniform(0.8, 1.2)
        noise = [random.randint(-5, 10) for _ in range(12)]
        values = [max(0, min(100, int(base_pattern[j] * variation + noise[j]))) for j in range(12)]
        data[keyword] = values
    
    logger.info(f"[TRENDS] 📊 Generated simulated trends for {len(keywords)} keywords")
    
    return {
        "months": months,
        "data": data,
        "status": "simulated",
        "source": "Simulación basada en patrones estacionales",
        "period": "12 meses"
    }


def extract_trend_keywords(product_name: str, category_hints: list = None) -> list:
    """
    Extracts relevant search keywords from product name for trends analysis.
    Ensures a minimum of 3 robust search terms.
    """
    import re
    
    # 1. CLEANING
    clean_name = re.sub(r'[^\w\s]', ' ', product_name.lower())
    words = clean_name.split()
    
    # Common stopwords to filter (Spanish & English)
    stopwords = {
        'de', 'para', 'y', 'en', 'con', 'the', 'for', 'and', 'with', 
        'a', 'el', 'la', 'los', 'las', 'un', 'una', 'of', 'to', 'in',
        'is', 'at', 'on', 'by', 'about', 'del', 'los', 'las'
    }
    
    # 2. FILTERING
    keywords = [w for w in words if len(w) >= 3 and w not in stopwords]
    
    search_terms = []
    
    # 3. BUILD LAYERED SEARCH TERMS
    # a. Full context phrase (Max 4 words)
    if keywords:
        search_terms.append(' '.join(keywords[:4]))
    
    # b. Core keyword pairs
    for i in range(min(2, len(keywords))):
        if i + 1 < len(keywords):
            search_terms.append(f"{keywords[i]} {keywords[i+1]}")
    
    # c. Single impact words
    for word in keywords[:2]:
        if len(word) >= 4:
            search_terms.append(word)
    
    # d. Category Hints
    if category_hints:
        search_terms.extend(category_hints[:2])
        
    # e. BROAD FALLBACKS (If extraction is too thin)
    if len(search_terms) < 3:
        fallbacks = ["amazon best sellers", "tendencias de mercado", "ecommerce trends"]
        search_terms.extend(fallbacks)
    
    # 4. DEDUPLICATE & LIMIT
    seen = set()
    unique_terms = []
    for term in search_terms:
        # Type safety: ensure term is a string
        if isinstance(term, dict):
            term = term.get("term", term.get("keyword", str(term)))
        term = str(term) if term else ""
        term_lower = term.lower().strip()
        if term_lower and term_lower not in seen:
            seen.add(term_lower)
            unique_terms.append(term_lower.title() if len(term_lower) > 3 else term_lower.upper())
    
    # Ensure at least 3 terms
    if len(unique_terms) < 3:
        unique_terms = (unique_terms + ["Amazon", "Ecommerce", "Trends"])[:3]
        
    return unique_terms[:5]


# Entry point for testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with sample product
    test_product = "Calcetines de compresión para running"
    keywords = extract_trend_keywords(test_product, ["calcetines compresión", "medias compresión"])
    print(f"Keywords: {keywords}")
    
    trends = get_google_trends_data(keywords, geo="ES")
    print(f"Months: {trends['months']}")
    print(f"Data: {trends['data']}")
    print(f"Status: {trends['status']}")
