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
