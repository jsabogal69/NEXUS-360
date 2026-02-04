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
            "title": ["title", "título", "product name", "nombre", "product_name", "product_details", "description", "item name"],
            "reviews": ["reviews", "reseñas", "total ratings", "review count", "review_count", "rating count"],
            "rating_score": ["rating", "score", "stars", "puntuación", "estrellas", "average rating", "avg rating"],
            "fees": ["fees", "fba fees", "tarifas", "amazon fees", "fba_fees", "fulfillment fee"],
            "active_sellers": ["active sellers", "sellers", "vendedores", "num sellers", "active_sellers", "seller count"],
            "dimensions": ["dimensions", "dimensiones", "size", "talla", "product dimensions"],
            "launch_date": ["launch date", "fecha lanzamiento", "creation date", "date first available", "creation_date", "published date"],
            "click_share": ["click share", "cuota de clic", "share", "click share %", "click_share", "click share percentage"],
            "click_count": ["niche click count", "click count", "recuento de clics", "click_count", "clicks"]
        }
        
        for field, aliases in column_aliases.items():
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(alias in col_lower for alias in aliases):
                    col_map[field] = col
                    break
        
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
                    "rank": int(DataExpert.normalize_number(row.get(col_map.get("bsr", ""), 0))) # Alias for Architect compatibility
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
            
            logger.info(f"[DATA-EXPERT] 💰 Extracted {len(products)} products from {filename}. Avg Price: ${result['avg_price']}")
            
        return result

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
