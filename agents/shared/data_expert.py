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
        """Processes CSV with encoding and separator detection."""
        # Try common separators
        for sep in [',', ';', '\t', '|']:
            try:
                df = pd.read_csv(io.BytesIO(content_bytes), sep=sep, nrows=5)
                if len(df.columns) > 1:
                    # Found the separator
                    df = pd.read_csv(io.BytesIO(content_bytes), sep=sep)
                    return DataExpert.clean_dataframe(df)
            except:
                continue
        # Default
        return pd.read_csv(io.BytesIO(content_bytes))

    @staticmethod
    def process_excel(content_bytes):
        """Processes Excel files."""
        df = pd.read_excel(io.BytesIO(content_bytes))
        return DataExpert.clean_dataframe(df)

    @staticmethod
    def process_pdf(content_bytes):
        """Expertly extracts text from PDF."""
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(content_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

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
        Extracts pricing data from any competitive/pricing file.
        Supports: Helium10, Amazon exports, generic pricing CSVs.
        
        Returns:
            {
                "has_real_data": True/False,
                "products": [{asin, title, price, sales, revenue, bsr}, ...],
                "avg_price": float,
                "price_range": {"min": float, "max": float},
                "total_products": int,
                "source_file": str
            }
        """
        result = {
            "has_real_data": False,
            "products": [],
            "avg_price": 0,
            "price_range": {"min": 0, "max": 0},
            "total_products": 0,
            "source_file": filename
        }
        
        if df is None or df.empty:
            logger.warning(f"[DATA-EXPERT] Empty dataframe for {filename}")
            return result
        
        logger.info(f"[DATA-EXPERT] Processing {filename} with {len(df)} rows, columns: {list(df.columns)[:10]}")
        
        # Flexible column mapping - supports multiple names per field
        # INCLUDES: User's specific POE Guide column names (Helium10, Amazon Niche)
        column_aliases = {
            "price": [
                # Standard
                "price", "precio", "cost", "costo", "unit price", "precio unitario", "msrp", "buy box",
                # Amazon Niche specific
                "average selling price", "asp", "selling price", "avg price",
                # Helium10 specific
                "fba price", "fbm price"
            ],
            "sales": [
                # Standard
                "sales", "ventas", "units", "unidades", "units sold",
                # Helium10 specific
                "monthly sales", "sales (monthly)", "est. sales", "estimated sales",
                # Amazon Niche specific
                "niche click count", "click count"
            ],
            "revenue": [
                # Standard
                "revenue", "ingresos", "gross", "total sales",
                # Helium10 specific
                "monthly revenue", "est. revenue", "estimated revenue"
            ],
            "bsr": [
                # Standard
                "bsr", "rank", "ranking", "best seller", "posicion",
                # Helium10 specific
                "best sellers rank", "sales rank"
            ],
            "asin": [
                "asin", "product id", "sku", "id producto", "parent asin", "child asin"
            ],
            "title": [
                "title", "titulo", "product", "producto", "name", "nombre", "description", "product name"
            ],
            "reviews": [
                # Standard
                "reviews", "reseñas", "review count", "numero de reseñas",
                # Amazon Niche specific
                "total ratings", "ratings", "rating count"
            ],
            # Additional useful columns from POE Guide
            "click_share": [
                "click share", "cuota de clic", "market share"
            ],
            "launch_date": [
                "launch date", "fecha de lanzamiento", "date first available"
            ],
            "fba_fees": [
                "fba fees", "fba fee", "fulfillment fee", "tarifas fba"
            ],
            "dimensions": [
                "dimensions", "dimensiones", "package dimensions", "item dimensions"
            ],
            "active_sellers": [
                "active sellers", "sellers", "vendedores activos", "number of sellers"
            ]
        }
        
        col_map = {}
        for field, aliases in column_aliases.items():
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if any(alias in col_lower for alias in aliases):
                    col_map[field] = col
                    break
        
        logger.info(f"[DATA-EXPERT] Column mapping for {filename}: {col_map}")
        
        # We need at least price OR (sales + title) to be useful
        if "price" not in col_map and "sales" not in col_map:
            logger.warning(f"[DATA-EXPERT] No price or sales column found in {filename}")
            # Try to find ANY numeric column that could be price
            for col in df.columns:
                try:
                    sample = df[col].dropna().head(10)
                    if sample.apply(lambda x: isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.','').replace(',','').replace('$','').isdigit())).any():
                        numeric_vals = sample.apply(DataExpert.normalize_number)
                        if 1 < numeric_vals.mean() < 500:  # Reasonable price range
                            col_map["price"] = col
                            logger.info(f"[DATA-EXPERT] Auto-detected price column: {col}")
                            break
                except:
                    continue
        
        if "price" not in col_map:
            logger.warning(f"[DATA-EXPERT] Could not find price column in {filename}")
            return result
        
        # Extract products
        products = []
        prices = []
        
        for idx, row in df.iterrows():
            try:
                price_val = DataExpert.normalize_number(row.get(col_map.get("price", ""), 0))
                
                if price_val > 0:  # Only include products with valid prices
                    product = {
                        "asin": str(row.get(col_map.get("asin", ""), f"ASIN-{idx}"))[:12],
                        "title": str(row.get(col_map.get("title", ""), f"Product {idx}"))[:100],
                        "price": round(price_val, 2),
                        "sales": int(DataExpert.normalize_number(row.get(col_map.get("sales", ""), 0))),
                        "revenue": round(DataExpert.normalize_number(row.get(col_map.get("revenue", ""), 0)), 2),
                        "bsr": int(DataExpert.normalize_number(row.get(col_map.get("bsr", ""), 0))),
                        "reviews": int(DataExpert.normalize_number(row.get(col_map.get("reviews", ""), 0)))
                    }
                    products.append(product)
                    prices.append(price_val)
                    
            except Exception as e:
                logger.debug(f"[DATA-EXPERT] Row {idx} skip: {e}")
                continue
        
        if products:
            result["has_real_data"] = True
            result["products"] = products[:20]  # Top 20 products
            result["avg_price"] = round(sum(prices) / len(prices), 2)
            result["price_range"] = {"min": round(min(prices), 2), "max": round(max(prices), 2)}
            result["total_products"] = len(products)
            
            logger.info(f"[DATA-EXPERT] ✅ Extracted {len(products)} products from {filename}. AVG: ${result['avg_price']}")
        
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
            else:
                return {"has_real_data": False, "reason": "Not identified as X-Ray file"}
                
        except Exception as e:
            logger.error(f"[DATA-EXPERT] Error extracting pricing: {e}")
            return {"has_real_data": False, "error": str(e)}
