import pandas as pd
import re
from datetime import datetime
import io
import logging

logger = logging.getLogger("DATA-EXPERT")

class DataExpert:
    """
    Expert system for data cleaning, normalization, and validation.
    Handles complex number formats, date parsing, and structured data extraction.
    """
    
    @staticmethod
    def normalize_number(value):
        """
        Expertly converts strings with various separators to floats.
        Handles:
        - 1.234,56 -> 1234.56
        - 1,234.56 -> 1234.56
        - 1 234,56 -> 1234.56
        """
        if pd.isna(value) or value is None:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        
        s = str(value).strip()
        # Remove currency symbols and other common non-numeric chars except separators
        s = re.sub(r'[^\d,.\s-]', '', s)
        
        if not s:
            return 0.0
            
        # Determine decimal separator
        # Logic: If both , and . exist, the last one is likely the decimal
        # If only one exists, check frequency or position
        last_dot = s.rfind('.')
        last_comma = s.rfind(',')
        
        if last_dot > last_comma:
            # . is decimal, , is thousands
            s = s.replace(',', '').replace(' ', '')
        elif last_comma > last_dot:
            # , is decimal, . is thousands
            s = s.replace('.', '').replace(' ', '').replace(',', '.')
        else:
            # Only one or none. If it's at index -3 or -2, it's likely a decimal
            # e.g. 1.23 or 1,23. Otherwise if it's 1.234 it's likely thousands
            # We assume . as decimal if not sure, but let's be smarter
            clean_s = s.replace(',', '.').replace(' ', '')
            try:
                return float(clean_s)
            except:
                return 0.0
                
        try:
            return float(s)
        except:
            return 0.0

    @staticmethod
    def normalize_date(value):
        """
        Expertly parses dates from various formats.
        """
        if pd.isna(value) or value is None:
            return None
        if isinstance(value, datetime):
            return value
        
        s = str(value).strip()
        formats = [
            "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", 
            "%d-%m-%Y", "%Y/%m/%d", "%b %d, %Y"
        ]
        for fmt in formats:
            try:
                return datetime.strptime(s, fmt)
            except:
                continue
        return s # Fallback to string

    @staticmethod
    def clean_dataframe(df):
        """
        Expertly cleans a whole dataframe:
        - Normalizes column names (snake_case).
        - Detects numeric columns and cleans them.
        - Detects date columns.
        """
        # 1. Clean Column Names
        df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', c.strip().lower()) for c in df.columns]
        
        # 2. Expert Cleaning per Column
        for col in df.columns:
            # Try to see if it's numeric
            sample = df[col].dropna().head(10).astype(str)
            
            # Check if looks like numbers
            is_numeric_like = sample.str.match(r'^-?[\d\s,.]+$').all()
            if is_numeric_like and not df[col].empty:
                df[col] = df[col].apply(DataExpert.normalize_number)
            
            # Check if looks like dates
            # Simple heuristic: contains / or - and has enough digits
            is_date_like = sample.str.contains(r'[/|-]').all() and sample.str.count(r'\d').mean() > 4
            if is_date_like:
                df[col] = df[col].apply(DataExpert.normalize_date)
                
        return df

    @staticmethod
    def process_csv(content_bytes):
        """
        Robust CSV processing using a 'Sniffer' approach.
        Detects separator and header row by scanning line-by-line.
        """
        try:
            content_str = content_bytes.decode('utf-8', errors='ignore')
            lines = content_str.splitlines()
            
            if not lines:
                return pd.DataFrame()

            # Keywords to identify the header row
            header_keywords = ["asin", "product", "price", "precio", "sales", "ventas", "rank", "bsr", "revenue", "ingresos", "title", "titulo"]
            
            best_sep = ','
            header_row_idx = 0
            max_score = 0
            
            # Scan first 30 lines to find the header
            for i, line in enumerate(lines[:30]):
                line_lower = line.lower()
                
                # Check possible separators
                for sep in [',', '\t', ';', '|']:
                    # Count columns with this separator
                    parts = line_lower.split(sep)
                    if len(parts) < 2: continue
                    
                    # Score based on keyword matches in this row
                    # We check if the split parts contain our keywords
                    matches = sum(1 for part in parts if any(kw in part.strip() for kw in header_keywords))
                    
                    # If we find strong matches, this is likely our winner
                    if matches > max_score:
                        max_score = matches
                        best_sep = sep
                        header_row_idx = i
            
            if max_score >= 1:
                logger.info(f"[DATA-EXPERT] 🕵️ Sniffer found header at row {header_row_idx} with sep='{best_sep}' (Score: {max_score})")
                
                # Use engine='python' for robustness against bad lines elsewhere
                # skip_blank_lines=True is default but explicit is good
                try:
                    df = pd.read_csv(
                        io.StringIO(content_str), 
                        sep=best_sep, 
                        skiprows=header_row_idx, 
                        engine='python',
                        on_bad_lines='warn' # Warn but don't crash on subsequent bad lines
                    )
                    return DataExpert.clean_dataframe(df)
                except Exception as e:
                    logger.warning(f"[DATA-EXPERT] Sniffer read failed: {e}. Falling back to default.")
            
            # Fallback for standard clean CSVs
            return pd.read_csv(io.StringIO(content_str))

        except Exception as e:
            logger.error(f"[DATA-EXPERT] CSV Sniffer Failed: {e}")
            return pd.DataFrame()

    @staticmethod
    def _find_header_row(df_raw, search_keywords):
        # Kept for Excel support - same logic as before or simplified
        for i in range(min(20, len(df_raw))):
            row_vals = df_raw.iloc[i].astype(str).str.lower().tolist()
            matches = sum(1 for kw in search_keywords if any(kw in val for val in row_vals))
            if matches >= 2:
                new_columns = df_raw.iloc[i].tolist()
                new_df = df_raw.iloc[i+1:].copy()
                new_df.columns = new_columns
                return new_df
        return df_raw

    @staticmethod
    def process_excel(content_bytes):
        """Processes Excel files with smart header detection."""
        try:
            header_keywords = ["asin", "product", "price", "precio", "sales", "ventas", "rank", "bsr"]
            
            # Read first without header
            df = pd.read_excel(io.BytesIO(content_bytes), header=None)
            
            # Apply Header Hunter
            df = DataExpert._find_header_row(df, header_keywords)
            
            return DataExpert.clean_dataframe(df)
        except Exception as e:
             logger.error(f"[DATA-EXPERT] Excel Processing Failed: {e}")
             return pd.DataFrame()

    @staticmethod
    def process_pdf(content_bytes):
        """Expertly extracts text from PDF."""
        import PyPDF2
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(content_bytes))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"PDF Error: {e}")
            return ""

    @staticmethod
    def process_docx(content_bytes):
        """Expertly extracts text from DOCX."""
        import docx
        doc = docx.Document(io.BytesIO(content_bytes))
        return "\n".join([p.text for p in doc.paragraphs])

    # ═══════════════════════════════════════════════════════════════════════
    # POE DATA EXTRACTION (X-Ray, Amazon, Helium10, Any pricing file)
    # ═══════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def is_pricing_data_file(filename: str, df: pd.DataFrame = None) -> bool:
        """
        Detects if a file contains pricing/competitive data.
        Matches: Helium10, Amazon exports, any file with price columns.
        """
        # Keywords in filename that indicate pricing data
        filename_keywords = [
            "xray", "x-ray", "helium", "h10", "cerebro", "magnet",  # Helium10
            "amazon", "seller", "product", "listing", "competitor",  # Amazon
            "price", "precio", "pricing", "sales", "ventas",  # Generic
            "market", "analysis", "export", "data"  # Generic exports
        ]
        
        # Check filename
        fname_lower = filename.lower()
        if any(kw in fname_lower for kw in filename_keywords):
            logger.info(f"[DATA-EXPERT] File '{filename}' matched by filename keyword")
            return True
        
        # Check columns if DataFrame provided
        if df is not None and not df.empty:
            # Columns that indicate pricing data (English and Spanish)
            pricing_columns = [
                # English
                "price", "sales", "revenue", "bsr", "asin", "title", "reviews",
                "units", "cost", "margin", "rank", "rating", "seller",
                # Spanish
                "precio", "ventas", "ingresos", "titulo", "costo", "margen",
                "calificacion", "vendedor", "unidades"
            ]
            
            col_names_lower = [str(c).lower().strip() for c in df.columns]
            
            # Count matches
            matches = 0
            matched_cols = []
            for pricing_col in pricing_columns:
                for actual_col in col_names_lower:
                    if pricing_col in actual_col:
                        matches += 1
                        matched_cols.append(actual_col)
                        break
            
            # If we have at least 2 pricing-related columns, it's a pricing file
            if matches >= 2:
                logger.info(f"[DATA-EXPERT] File '{filename}' matched {matches} columns: {matched_cols}")
                return True
        
        return False
    
    # Keep old function name for backwards compatibility
    @staticmethod
    def is_xray_file(filename: str, df: pd.DataFrame = None) -> bool:
        """Alias for is_pricing_data_file for backwards compatibility."""
        return DataExpert.is_pricing_data_file(filename, df)

    @staticmethod
    def extract_xray_pricing(df: pd.DataFrame, filename: str = "") -> dict:
        """
        Extracts Product Intelligence: Pricing, Sales, Revenue, BSR + 
        New fields: Fees, Dimensions, Launch Date, Click Share.
        """
        # Dictionary to store results
        result = {
            "has_real_data": False,
            "products": [],
            "avg_price": 0.0,
            "price_range": "N/A",
            "total_products": 0,
            "source_file": filename
        }
        
        if df is None or df.empty:
            return result
            
        logger.info(f"[DATA-EXPERT] Extracting Product Data from {filename}")
        
        # 1. Map columns (Expanded)
        col_map = {}
        column_aliases = {
            "price": ["price", "precio", "average selling price", "asp", "average_selling_price", "price_usd", "valor"],
            "sales": ["sales", "ventas", "units", "unidades", "monthly sales", "monthly_sales", "est_sales", "est. sales", "unit sales", "sales (30 days)"],
            "revenue": ["revenue", "ingresos", "facturación", "est_revenue", "est. revenue", "revenue (30 days)"],
            "bsr": ["bsr", "rank", "ranking", "best sellers rank", "best_sellers_rank", "sales rank"],
            "asin": ["asin", "product id", "product_id", "id"],
            "title": ["title", "título", "product name", "nombre", "product_name", "product_details", "description", "item name", "name", "listing name", "listing_name", "item", "product title", "product_title"],
            "reviews": ["reviews", "reseñas", "total ratings", "review count", "review_count", "rating count", "rating_count", "number of ratings", "total_ratings", "reviews count", "customer reviews"],
            "rating_score": ["star rating", "star_rating", "avg_rating", "average_rating", "avg rating", "average rating", "rating", "score", "stars", "puntuación", "estrellas"],
            "fees": ["fees", "fba fees", "tarifas", "amazon fees", "fba_fees", "fulfillment fee"],
            "active_sellers": ["active sellers", "sellers", "vendedores", "num sellers", "active_sellers", "seller count"],
            "dimensions": ["dimensions", "dimensiones", "size", "talla", "product dimensions"],
            "launch_date": ["launch date", "fecha lanzamiento", "creation date", "date first available", "creation_date", "published date"],
            "click_share": ["click share", "cuota de clic", "share", "click share %", "click_share", "click share percentage"],
            "click_count": ["niche click count", "click count", "recuento de clics", "click_count", "clicks"],
            # ── NEW Helium 10 Extended Fields ──
            "brand": ["brand", "marca", "brand name", "brand_name"],
            "seller_country": ["seller country", "seller country/region", "país del vendedor", "seller_country", "country", "region"],
            "fulfillment": ["fulfillment", "fulfillment type", "tipo fulfillment", "fba/fbm", "fulfilled by"],
            "weight": ["weight", "peso", "item weight", "product weight", "shipping weight"],
            "review_velocity": ["review velocity", "velocidad de reseñas", "review_velocity", "review vel", "reviews/month"],
            "images_count": ["images", "imágenes", "image count", "images_count", "num images", "photo count"],
            "seller_age_months": ["seller age", "edad del vendedor", "seller age (mo)", "seller_age", "months selling"],
            "size_tier": ["size tier", "tier de tamaño", "size_tier", "fba size tier", "product size tier"],
            "sponsored": ["sponsored", "patrocinado", "is_sponsored", "ad type", "ppc"],
            "seller_name": ["seller", "vendedor", "seller name", "seller_name", "sold by"],
            "buy_box": ["buy box", "buy_box", "buy box owner", "buybox"],
            "title_length": ["title char", "title characters", "title char. count", "title_length", "char count", "character count"],
            "recent_purchases": ["recent purchases", "compras recientes", "recent_purchases", "bought in past month"],
            "category": ["category", "categoría", "department", "product category", "main category"],
            "parent_sales": ["parent level sales", "parent sales", "parent_sales", "parent_level_sales"],
            "parent_revenue": ["parent level revenue", "parent revenue", "parent_revenue", "parent_level_revenue"],
            "best_seller": ["best seller", "best_seller", "bestseller", "amazon's choice"],
            "display_order": ["display order", "display_order", "order", "position", "rank position"]
        }
        
        # Normalize aliases the same way clean_dataframe normalizes columns:
        # spaces and special chars → underscores, lowercase
        def _normalize(s):
            return re.sub(r'[^a-zA-Z0-9_]', '_', s.strip().lower())
        
        # Two-pass matching: exact first, then substring
        # Pass 1: Exact matches (prevents 'name' from matching 'brand_name')
        for field, aliases in column_aliases.items():
            if field in col_map:
                continue
            for col in df.columns:
                col_norm = _normalize(str(col))
                if any(col_norm == _normalize(alias) for alias in aliases):
                    col_map[field] = col
                    break
        
        # Pass 2: Substring matches (for remaining unmapped fields)
        mapped_cols = set(col_map.values())
        for field, aliases in column_aliases.items():
            if field in col_map:
                continue
            for col in df.columns:
                if col in mapped_cols:
                    continue  # Skip columns already assigned
                col_norm = _normalize(str(col))
                if any(_normalize(alias) in col_norm for alias in aliases):
                    col_map[field] = col
                    break
        
        logger.info(f"[DATA-EXPERT] Column mapping for {filename}: {col_map}")
        logger.info(f"[DATA-EXPERT] Available columns: {list(df.columns)}")
        
        # Validation: Needs at least Price or Sales or Click Count to be useful
        if "price" not in col_map and "sales" not in col_map and "click_count" not in col_map:
            logger.warning(f"[DATA-EXPERT] Missing essential columns in {filename}")
            return result
            
        products = []
        prices = []
        
        for idx, row in df.iterrows():
            try:
                # Basic Fields
                price_val = DataExpert.normalize_number(row.get(col_map.get("price", ""), 0))
                sales_val = int(DataExpert.normalize_number(row.get(col_map.get("sales", ""), 0)))
                
                # Demand Proxy: If no sales, check for Click Count
                if sales_val == 0 and "click_count" in col_map:
                     sales_val = int(DataExpert.normalize_number(row.get(col_map.get("click_count", ""), 0)))
                
                asin = str(row.get(col_map.get("asin", ""), f"ASIN-{idx}"))
                if len(asin) > 20: asin = asin[:12]
                
                product = {
                    "asin": asin,
                    "title": str(row.get(col_map.get("title", ""), f"Product {idx}"))[:150],
                    "name": str(row.get(col_map.get("title", ""), f"Product {idx}"))[:150], # Alias for Architect compatibility (uses 'name')
                    "price": round(price_val, 2),
                    "sales": sales_val,
                    "revenue": round(DataExpert.normalize_number(row.get(col_map.get("revenue", ""), 0)), 2),
                    "bsr": int(DataExpert.normalize_number(row.get(col_map.get("bsr", ""), 0))),
                    "reviews": int(DataExpert.normalize_number(row.get(col_map.get("reviews", ""), 0))),
                    "rating": round(DataExpert.normalize_number(row.get(col_map.get("rating_score", ""), 0)), 1),
                    # Extended Intelligence
                    "fees": round(DataExpert.normalize_number(row.get(col_map.get("fees", ""), 0)), 2),
                    "active_sellers": int(DataExpert.normalize_number(row.get(col_map.get("active_sellers", ""), 1))),
                    "dimensions": str(row.get(col_map.get("dimensions", ""), "N/A")),
                    "launch_date": str(row.get(col_map.get("launch_date", ""), "N/A")),
                    "click_share": DataExpert.normalize_number(row.get(col_map.get("click_share", ""), 0)),
                    "rank": int(DataExpert.normalize_number(row.get(col_map.get("bsr", ""), 0))),
                    # ── NEW Helium 10 Extended Fields ──
                    "brand": str(row.get(col_map.get("brand", ""), "N/A")).strip() or "N/A",
                    "seller_country": str(row.get(col_map.get("seller_country", ""), "N/A")).strip() or "N/A",
                    "fulfillment": str(row.get(col_map.get("fulfillment", ""), "N/A")).strip() or "N/A",
                    "weight": str(row.get(col_map.get("weight", ""), "N/A")).strip() or "N/A",
                    "weight_lbs": DataExpert.normalize_number(row.get(col_map.get("weight", ""), 0)),
                    "review_velocity": int(DataExpert.normalize_number(row.get(col_map.get("review_velocity", ""), 0))),
                    "images_count": int(DataExpert.normalize_number(row.get(col_map.get("images_count", ""), 0))),
                    "seller_age_months": int(DataExpert.normalize_number(row.get(col_map.get("seller_age_months", ""), 0))),
                    "size_tier": str(row.get(col_map.get("size_tier", ""), "N/A")).strip() or "N/A",
                    "sponsored": str(row.get(col_map.get("sponsored", ""), "No")).strip() or "No",
                    "seller_name": str(row.get(col_map.get("seller_name", ""), "N/A")).strip() or "N/A",
                    "buy_box": str(row.get(col_map.get("buy_box", ""), "N/A")).strip() or "N/A",
                    "title_length": int(DataExpert.normalize_number(row.get(col_map.get("title_length", ""), 0))),
                    "recent_purchases": int(DataExpert.normalize_number(row.get(col_map.get("recent_purchases", ""), 0))),
                    "category": str(row.get(col_map.get("category", ""), "N/A")).strip() or "N/A",
                    "parent_sales": int(DataExpert.normalize_number(row.get(col_map.get("parent_sales", ""), 0))),
                    "parent_revenue": round(DataExpert.normalize_number(row.get(col_map.get("parent_revenue", ""), 0)), 2),
                    "best_seller": str(row.get(col_map.get("best_seller", ""), "No")).strip() or "No",
                    "display_order": int(DataExpert.normalize_number(row.get(col_map.get("display_order", ""), idx + 1)))
                }
                
                if product["price"] > 0 or product["sales"] > 0 or product["click_share"] > 0:
                    products.append(product)
                    if product["price"] > 0:
                        prices.append(product["price"])
                        
            except Exception as e:
                continue
                
        if products:
            result["has_real_data"] = True
            result["products"] = products[:50] # Increase limit to 50
            result["total_products"] = len(products)
            if prices:
                result["avg_price"] = round(sum(prices) / len(prices), 2)
                result["price_range"] = f"${min(prices)} - ${max(prices)}"
            
            # ── AUTO: Tag demographics & compute niche analytics ──
            try:
                DataExpert.analyze_product_demographics(products)
                result["niche_analytics"] = DataExpert.compute_niche_analytics(products)
                logger.info(f"[DATA-EXPERT] 🎯 Niche analytics computed: {result['niche_analytics'].get('demographics', {}).get('dominant_segment', 'N/A')} dominant")
            except Exception as e:
                logger.warning(f"[DATA-EXPERT] Niche analytics failed (non-critical): {e}")
            
            logger.info(f"[DATA-EXPERT] 💰 Extracted {len(products)} products from {filename}. Avg Price: ${result['avg_price']}")
            
        return result

    # ═══════════════════════════════════════════════════════════════════════
    # PRODUCT DEMOGRAPHICS & TARGET AGE ANALYSIS
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def analyze_product_demographics(products: list) -> dict:
        """
        Analyzes product titles to extract target customer demographics.
        Uses regex patterns to identify age ranges, grade levels, and 
        age-related keywords. Modifies products in-place by adding:
          - target_age_min, target_age_max, age_segment
        
        Returns:
            Summary dict with segment counts and dominant segment.
        """
        # Grade-to-age mapping
        GRADE_TO_AGE = {
            "pre-k": 4, "prek": 4, "preschool": 4,
            "kindergarten": 5, "k": 5,
            "1st": 6, "first": 6, "1": 6,
            "2nd": 7, "second": 7, "2": 7,
            "3rd": 8, "third": 8, "3": 8,
            "4th": 9, "fourth": 9, "4": 9,
            "5th": 10, "fifth": 10, "5": 10,
            "6th": 11, "sixth": 11, "6": 11,
            "7th": 12, "seventh": 12,
            "8th": 13, "eighth": 13,
        }
        
        def _classify_segment(age_min, age_max):
            """Classify age range into market segment."""
            mid = (age_min + age_max) / 2
            if mid <= 1:
                return "Infant"
            elif mid <= 3:
                return "Toddler"
            elif mid <= 5:
                return "Preschool"
            elif mid <= 10:
                return "Elementary"
            elif mid <= 12:
                return "Tween"
            elif mid <= 17:
                return "Teen"
            elif mid >= 18:
                return "Adult"
            return "Unspecified"
        
        def _extract_age_from_title(title: str) -> tuple:
            """Extract (age_min, age_max) from product title using regex patterns."""
            t = title.lower()
            
            # Pattern 1: "Ages X-Y" / "Age X-Y" / "ages X to Y"
            m = re.search(r'ages?\s*(\d{1,2})\s*[-–—to&]\s*(\d{1,2})', t)
            if m:
                return int(m.group(1)), int(m.group(2))
            
            # Pattern 2: "Ages X+" / "Age X & Up" / "Age X and Up"  
            m = re.search(r'ages?\s*(\d{1,2})\s*(?:\+|&\s*up|and\s*up|up)', t)
            if m:
                a = int(m.group(1))
                return a, min(a + 6, 99)
            
            # Pattern 3: "X-Y years" / "X-Y year old"
            m = re.search(r'(\d{1,2})\s*[-–—to]\s*(\d{1,2})\s*(?:years?|yr|año)', t)
            if m:
                return int(m.group(1)), int(m.group(2))
            
            # Pattern 4: "for X year olds"
            m = re.search(r'for\s*(\d{1,2})\s*year\s*old', t)
            if m:
                a = int(m.group(1))
                return a, a + 2
            
            # Pattern 5: Grade ranges "Grade K-3" / "1st-3rd Grade" / "Grades 1-5"
            m = re.search(r'grades?\s*(pre-?k|k|kindergarten|\d+(?:st|nd|rd|th)?)\s*[-–—to&]\s*(pre-?k|k|kindergarten|\d+(?:st|nd|rd|th)?)', t)
            if m:
                g1 = re.sub(r'(st|nd|rd|th)$', '', m.group(1).lower())
                g2 = re.sub(r'(st|nd|rd|th)$', '', m.group(2).lower())
                a1 = GRADE_TO_AGE.get(g1, int(g1) + 5 if g1.isdigit() else 5)
                a2 = GRADE_TO_AGE.get(g2, int(g2) + 5 if g2.isdigit() else 10)
                return a1, a2
            
            # Pattern 6: Single grade mention "Kindergarten" / "3rd Grade"
            m = re.search(r'(pre-?k|kindergarten|\d+(?:st|nd|rd|th))\s*grade', t)
            if m:
                g = re.sub(r'(st|nd|rd|th)$', '', m.group(1).lower())
                a = GRADE_TO_AGE.get(g, int(g) + 5 if g.isdigit() else 5)
                return a, a + 1
            
            # Pattern 7: Keyword-based age inference
            keyword_ages = [
                (r'\b(?:infant|newborn|baby)\b', 0, 1),
                (r'\b(?:toddler|toddlers)\b', 1, 3),
                (r'\b(?:preschool|pre-school|pre school|prek|pre-k)\b', 3, 5),
                (r'\bfor\s+kids\b', 4, 12),
                (r'\bchildren\b', 4, 12),
                (r'\b(?:tween|tweens)\b', 10, 12),
                (r'\b(?:teen|teens|teenager|adolescent)\b', 13, 17),
                (r'\b(?:adult|adults|grown-?up)\b', 18, 65),
                (r'\b(?:family|families|all\s+ages)\b', 4, 99),
                (r'\b(?:senior|elderly)\b', 60, 99),
            ]
            for pattern, a_min, a_max in keyword_ages:
                if re.search(pattern, t):
                    return a_min, a_max
            
            # Pattern 8: Multiple standalone ages "4-5-6-7-8" / "4, 5, 6, 7, 8"
            m = re.findall(r'\b(\d{1,2})\b', t)
            ages = [int(x) for x in m if 1 <= int(x) <= 17]
            if len(ages) >= 3:
                return min(ages), max(ages)
            
            return None, None
        
        segments = {}
        for p in products:
            title = p.get("title", p.get("name", ""))
            age_min, age_max = _extract_age_from_title(title)
            
            if age_min is not None:
                p["target_age_min"] = age_min
                p["target_age_max"] = age_max
                seg = _classify_segment(age_min, age_max)
                p["age_segment"] = seg
            else:
                p["target_age_min"] = None
                p["target_age_max"] = None
                p["age_segment"] = "Unspecified"
                seg = "Unspecified"
            
            segments[seg] = segments.get(seg, 0) + 1
        
        # Find dominant segment (excluding Unspecified)
        specified = {k: v for k, v in segments.items() if k != "Unspecified"}
        dominant = max(specified, key=specified.get) if specified else "Unspecified"
        
        return {
            "segments": segments,
            "dominant_segment": dominant,
            "total_classified": sum(v for k, v in segments.items() if k != "Unspecified"),
            "total_unclassified": segments.get("Unspecified", 0),
            "classification_rate": round(sum(v for k, v in segments.items() if k != "Unspecified") / max(len(products), 1) * 100, 1)
        }

    # ═══════════════════════════════════════════════════════════════════════
    # ADVANCED NICHE ANALYTICS (Pandas-Powered)
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def compute_niche_analytics(products: list) -> dict:
        """
        Computes advanced niche analytics using Pandas:
          - Price statistics (mean, median, std, quartiles)
          - Revenue Pareto analysis (top 20% = X% revenue)
          - Brand concentration (HHI index)
          - Rating distribution
          - Seller origin & fulfillment breakdown
          - Review velocity percentiles
          - Age segment distribution
        """
        if not products:
            return {}
        
        df = pd.DataFrame(products)
        analytics = {}
        
        # ── 1. PRICE ANALYTICS ──
        prices = df["price"][df["price"] > 0].dropna()
        if len(prices) > 0:
            analytics["price"] = {
                "mean": round(float(prices.mean()), 2),
                "median": round(float(prices.median()), 2),
                "std": round(float(prices.std()), 2) if len(prices) > 1 else 0,
                "q25": round(float(prices.quantile(0.25)), 2),
                "q75": round(float(prices.quantile(0.75)), 2),
                "min": round(float(prices.min()), 2),
                "max": round(float(prices.max()), 2),
                "sweet_spot": f"${round(float(prices.quantile(0.25)),2)} - ${round(float(prices.quantile(0.75)),2)}"
            }
        
        # ── 2. REVENUE PARETO ANALYSIS ──
        revenues = df["revenue"][df["revenue"] > 0].sort_values(ascending=False).dropna()
        if len(revenues) > 0:
            total_rev = revenues.sum()
            top_20_count = max(1, int(len(revenues) * 0.2))
            top_20_rev = revenues.iloc[:top_20_count].sum()
            pareto_ratio = round((top_20_rev / total_rev) * 100, 1) if total_rev > 0 else 0
            analytics["revenue_pareto"] = {
                "total_revenue": round(float(total_rev), 2),
                "top_20pct_share": pareto_ratio,
                "top_20pct_count": top_20_count,
                "concentration": "Alta" if pareto_ratio > 70 else ("Media" if pareto_ratio > 50 else "Baja"),
                "interpretation": f"Top {top_20_count} productos generan {pareto_ratio}% del revenue total"
            }
        
        # ── 3. BRAND CONCENTRATION (HHI) ──
        if "brand" in df.columns:
            brands = df["brand"][df["brand"] != "N/A"].dropna()
            if len(brands) > 0:
                brand_counts = brands.value_counts()
                total_brands = len(brands)
                # HHI = sum of squared market shares (0-10000 scale)
                market_shares = (brand_counts / total_brands * 100)
                hhi = round(float((market_shares ** 2).sum()))
                
                if hhi >= 2500:
                    hhi_label = "Muy Concentrado"
                    hhi_color = "#ef4444"
                elif hhi >= 1500:
                    hhi_label = "Moderadamente Concentrado"
                    hhi_color = "#d97706"
                else:
                    hhi_label = "Competitivo"
                    hhi_color = "#059669"
                
                analytics["brand_concentration"] = {
                    "hhi_index": hhi,
                    "hhi_label": hhi_label,
                    "hhi_color": hhi_color,
                    "unique_brands": int(len(brand_counts)),
                    "top_brand": str(brand_counts.index[0]),
                    "top_brand_share": round(float(brand_counts.iloc[0] / total_brands * 100), 1),
                    "top_3": [{"brand": str(b), "share": round(float(c / total_brands * 100), 1)} for b, c in brand_counts.head(3).items()]
                }
        
        # ── 4. RATING DISTRIBUTION ──
        ratings = df["rating"][df["rating"] > 0].dropna()
        if len(ratings) > 0:
            bins = {"below_3.5": 0, "3.5_to_4.0": 0, "4.0_to_4.5": 0, "above_4.5": 0}
            for r in ratings:
                if r < 3.5:
                    bins["below_3.5"] += 1
                elif r < 4.0:
                    bins["3.5_to_4.0"] += 1
                elif r < 4.5:
                    bins["4.0_to_4.5"] += 1
                else:
                    bins["above_4.5"] += 1
            analytics["rating_distribution"] = {
                "bins": bins,
                "mean": round(float(ratings.mean()), 2),
                "median": round(float(ratings.median()), 2),
                "quality_bar": round(float((ratings >= 4.0).sum() / len(ratings) * 100), 1)
            }
        
        # ── 5. SELLER ORIGIN BREAKDOWN ──
        if "seller_country" in df.columns:
            origins = df["seller_country"].str.upper().value_counts()
            total_o = len(df)
            origin_dist = {}
            for country, count in origins.head(5).items():
                origin_dist[str(country)] = round(float(count / total_o * 100), 1)
            analytics["seller_origins"] = origin_dist
        
        # ── 6. FULFILLMENT MIX ──
        if "fulfillment" in df.columns:
            ful = df["fulfillment"].str.upper().value_counts()
            total_f = len(df)
            ful_dist = {}
            for ftype, count in ful.items():
                ful_dist[str(ftype)] = round(float(count / total_f * 100), 1)
            analytics["fulfillment_mix"] = ful_dist
        
        # ── 7. REVIEW VELOCITY PERCENTILES ──
        if "review_velocity" in df.columns:
            rv = df["review_velocity"][df["review_velocity"] > 0].dropna()
            if len(rv) > 0:
                analytics["review_velocity"] = {
                    "p25": int(rv.quantile(0.25)),
                    "p50": int(rv.quantile(0.50)),
                    "p75": int(rv.quantile(0.75)),
                    "p90": int(rv.quantile(0.90)) if len(rv) >= 5 else int(rv.max()),
                    "mean": round(float(rv.mean()), 1)
                }
        
        # ── 8. DEMOGRAPHICS (from previously tagged products) ──
        if "age_segment" in df.columns:
            seg_counts = df["age_segment"].value_counts()
            total_seg = len(df)
            demographics = {}
            for seg, count in seg_counts.items():
                demographics[str(seg)] = {
                    "count": int(count),
                    "pct": round(float(count / total_seg * 100), 1)
                }
            
            # Dominant specified segment
            specified = {k: v for k, v in demographics.items() if k != "Unspecified"}
            dominant = max(specified, key=lambda x: specified[x]["count"]) if specified else "Unspecified"
            
            analytics["demographics"] = {
                "segments": demographics,
                "dominant_segment": dominant,
                "classification_rate": round(float(df["age_segment"].ne("Unspecified").sum() / total_seg * 100), 1)
            }
            
            # Price by segment analysis
            price_by_seg = {}
            for seg in df["age_segment"].unique():
                seg_prices = df[df["age_segment"] == seg]["price"]
                seg_prices = seg_prices[seg_prices > 0].dropna()
                if len(seg_prices) > 0:
                    price_by_seg[str(seg)] = {
                        "avg_price": round(float(seg_prices.mean()), 2),
                        "count": int(len(seg_prices))
                    }
            analytics["price_by_segment"] = price_by_seg
        
        return analytics

    @staticmethod
    def extract_pricing_from_bytes(content_bytes: bytes, filename: str) -> dict:
        """
        Convenience method: Detects file type, processes, and extracts X-Ray pricing.
        """
        try:
            if filename.lower().endswith(('.csv', '.txt')):
                df = DataExpert.process_csv(content_bytes)
            elif filename.lower().endswith(('.xlsx', '.xls')):
                df = DataExpert.process_excel(content_bytes)
            else:
                return {"has_real_data": False, "error": "Unsupported file type"}
            
            if DataExpert.is_xray_file(filename, df):
                return DataExpert.extract_xray_pricing(df, filename)
            elif DataExpert.is_search_terms_file(filename, df):
                return DataExpert.extract_search_terms_data(df, filename)
            else:
                return {"has_real_data": False, "reason": "Not identified as X-Ray or Search Terms file"}
                
        except Exception as e:
            logger.error(f"[DATA-EXPERT] Error extracting pricing: {e}")
            return {"has_real_data": False, "error": str(e)}

    # ═══════════════════════════════════════════════════════════════════════
    # SEARCH TERMS DATA EXTRACTION (Amazon Search Terms / Niche Details)
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def is_search_terms_file(filename: str, df: pd.DataFrame = None) -> bool:
        """
        Detects if a file contains Search Terms data (Volume, Conversion, Click Share).
        Matches: Amazon Brand Analytics, Niche Details - Search Terms Tab.
        """
        filename_keywords = [
            "search terms", "search_terms", "searchterms", "terminos de busqueda",
            "keyword", "palabra clave", "niche details", "search volume"
        ]
        
        fname_lower = filename.lower()
        if any(kw in fname_lower for kw in filename_keywords):
            logger.info(f"[DATA-EXPERT] File '{filename}' matched as Search Terms by filename")
            return True
            
        if df is not None and not df.empty:
            st_columns = [
                "search term", "search volume", "click share", "conversion rate",
                "volumen de busqueda", "tasa de conversion"
            ]
            col_names_lower = [str(c).lower().strip() for c in df.columns]
            
            matches = 0
            for st_col in st_columns:
                for actual_col in col_names_lower:
                    if st_col in actual_col:
                        matches += 1
                        break
            
            if matches >= 2:
                logger.info(f"[DATA-EXPERT] File '{filename}' matched {matches} Search Terms columns")
                return True
                
        return False

    @staticmethod
    def extract_search_terms_data(df: pd.DataFrame, filename: str = "") -> dict:
        """
        Extracts Search Terms intelligence: Volume, Growth, Conversion.
        
        Returns:
            {
                "has_search_data": True,
                "terms": [{term, volume, growth_90d, click_share, conversion_rate}, ...],
                "total_search_volume": int,
                "avg_conversion_rate": float, # Weighted by volume
                "top_keywords": [str],
                "source_file": str
            }
        """
        result = {
            "has_search_data": False,
            "terms": [],
            "total_search_volume": 0,
            "avg_conversion_rate": 0.0,
            "top_keywords": [],
            "source_file": filename
        }
        
        if df is None or df.empty:
            return result
            
        logger.info(f"[DATA-EXPERT] Extracting Search Terms from {filename}")
        
        # Column mapping
        col_map = {}
        column_aliases = {
            "term": ["search term", "término de búsqueda", "keyword", "palabra clave"],
            "volume": ["search volume", "volumen de búsqueda", "count", "recuento"],
            "growth_90d": ["growth (past 90 days)", "crecimiento (90 días)", "change"],
            "click_share": ["click share", "cuota de clic", "participación de clic"],
            "conversion_rate": ["search conversion rate", "conversion rate", "tasa de conversión", "conv. rate"]
        }
        
        for field, aliases in column_aliases.items():
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(alias in col_lower for alias in aliases):
                    col_map[field] = col
                    break
        
        if "term" not in col_map or "volume" not in col_map:
            logger.warning(f"[DATA-EXPERT] Missing essential search term columns in {filename}")
            return result
            
        terms = []
        total_vol = 0
        weighted_conv_sum = 0
        total_vol_for_conv = 0
        
        for idx, row in df.iterrows():
            try:
                term = str(row.get(col_map.get("term"), "")).strip()
                if not term or term.lower() == "nan": continue
                
                vol = int(DataExpert.normalize_number(row.get(col_map.get("volume"), 0)))
                # Growth can be negative, normalize_number handles it? 
                # Need to be careful with percentages if they are purely string like "12%"
                # normalize_number handles basic cleaning
                growth = DataExpert.normalize_number(row.get(col_map.get("growth_90d"), 0)) 
                click_share = DataExpert.normalize_number(row.get(col_map.get("click_share"), 0))
                conv_rate = DataExpert.normalize_number(row.get(col_map.get("conversion_rate"), 0))
                
                # Conversion rate might be percentage (e.g. 5.4 or 0.054)
                # Heuristic: if mean > 1 it's likely percentage (5.4%), if < 1 it's decimal (0.054)
                # We'll normalize later if needed, but usually POE data is numeric
                
                terms.append({
                    "term": term,
                    "volume": vol,
                    "growth_90d": growth,
                    "click_share": click_share,
                    "conversion_rate": conv_rate
                })
                
                total_vol += vol
                if conv_rate > 0:
                    weighted_conv_sum += (vol * conv_rate)
                    total_vol_for_conv += vol
                    
            except Exception as e:
                continue
                
        if terms:
            result["has_search_data"] = True
            result["terms"] = sorted(terms, key=lambda x: x["volume"], reverse=True)[:50] # Top 50
            result["total_search_volume"] = total_vol
            result["top_keywords"] = [t["term"] for t in result["terms"][:5]]
            
            if total_vol_for_conv > 0:
                result["avg_conversion_rate"] = round(weighted_conv_sum / total_vol_for_conv, 2)
            
            logger.info(f"[DATA-EXPERT] ✅ Extracted {len(terms)} search terms. Total Vol: {total_vol}, Avg Conv: {result['avg_conversion_rate']}%")
            
        return result
