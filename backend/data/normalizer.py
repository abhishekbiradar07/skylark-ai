"""Data normalization utilities."""
import re
import json
import logging
from typing import Any, Optional, Dict, List
from datetime import datetime
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

# Missing value representations
MISSING_VALUES = {
    None, "", "-", "N/A", "NA", "n/a", "na", "None", "none", 
    "Not Available", "not available", "NULL", "null", "#N/A"
}


class DataNormalizer:
    """Normalize Monday.com data."""
    
    @staticmethod
    def is_missing(value: Any) -> bool:
        """Check if value represents missing data.
        
        Args:
            value: Value to check
            
        Returns:
            True if value is missing
        """
        if value is None:
            return True
        
        if isinstance(value, str):
            stripped = value.strip()
            return stripped == "" or stripped in MISSING_VALUES
        
        return False
    
    @staticmethod
    def normalize_text(value: Any) -> Optional[str]:
        """Normalize text value.
        
        Args:
            value: Value to normalize
            
        Returns:
            Normalized text or None if missing
        """
        if DataNormalizer.is_missing(value):
            return None
        
        if isinstance(value, str):
            # Normalize whitespace
            normalized = " ".join(value.strip().split())
            return normalized if normalized else None
        
        return str(value)
    
    @staticmethod
    def normalize_number(value: Any) -> Optional[float]:
        """Normalize numeric value.
        
        Args:
            value: Value to normalize
            
        Returns:
            Normalized number or None if missing/invalid
        """
        if DataNormalizer.is_missing(value):
            return None
        
        try:
            # Handle string numbers
            if isinstance(value, str):
                # Remove currency symbols, commas, whitespace
                cleaned = re.sub(r'[₹$,\s]', '', value.strip())
                
                # Handle empty after cleaning
                if not cleaned or cleaned in MISSING_VALUES:
                    return None
                
                return float(cleaned)
            
            # Direct numeric types
            if isinstance(value, (int, float)):
                return float(value)
            
            return None
            
        except (ValueError, TypeError):
            logger.warning(f"Could not convert to number: {value}")
            return None
    
    @staticmethod
    def normalize_date(value: Any) -> Optional[datetime]:
        """Normalize date value.
        
        Args:
            value: Value to normalize
            
        Returns:
            Normalized datetime or None if missing/invalid
        """
        if DataNormalizer.is_missing(value):
            return None
        
        try:
            if isinstance(value, datetime):
                return value
            
            if isinstance(value, str):
                # Try parsing with dateutil
                return date_parser.parse(value, fuzzy=True)
            
            return None
            
        except (ValueError, TypeError, date_parser.ParserError):
            logger.warning(f"Could not parse date: {value}")
            return None
    
    @staticmethod
    def normalize_percentage(value: Any) -> Optional[float]:
        """Normalize percentage value to decimal (0-1).
        
        Args:
            value: Value to normalize (e.g., "70%" or 0.7)
            
        Returns:
            Normalized percentage as decimal or None
        """
        if DataNormalizer.is_missing(value):
            return None
        
        try:
            if isinstance(value, str):
                # Remove % symbol
                cleaned = value.strip().replace('%', '').strip()
                num = float(cleaned)
                
                # If > 1, assume it's in percentage form (70 means 70%)
                if num > 1:
                    return num / 100.0
                return num
            
            if isinstance(value, (int, float)):
                num = float(value)
                if num > 1:
                    return num / 100.0
                return num
            
            return None
            
        except (ValueError, TypeError):
            logger.warning(f"Could not convert to percentage: {value}")
            return None
    
    @staticmethod
    def normalize_status(value: Any) -> Optional[str]:
        """Normalize status value (case-insensitive, trimmed).
        
        Args:
            value: Status value
            
        Returns:
            Normalized status or None
        """
        normalized = DataNormalizer.normalize_text(value)
        if normalized:
            return normalized.lower()
        return None
    
    @staticmethod
    def parse_monday_json_value(value_str: str) -> Any:
        """Parse Monday.com JSON value string.
        
        Args:
            value_str: JSON string from Monday.com
            
        Returns:
            Parsed value or None
        """
        if DataNormalizer.is_missing(value_str):
            return None
        
        try:
            parsed = json.loads(value_str)
            return parsed
        except (json.JSONDecodeError, TypeError):
            return value_str
    
    @staticmethod
    def extract_column_value(column_data: Dict[str, Any]) -> Any:
        """Extract usable value from Monday.com column data.
        
        Args:
            column_data: Column data dict with 'text' and 'value'
            
        Returns:
            Extracted value
        """
        # Priority: text field (human-readable)
        text = column_data.get("text", "")
        if not DataNormalizer.is_missing(text):
            return text
        
        # Fallback: parse JSON value
        value_str = column_data.get("value", "")
        if not DataNormalizer.is_missing(value_str):
            return DataNormalizer.parse_monday_json_value(value_str)
        
        return None
    
    @staticmethod
    def normalize_customer_code(value: Any) -> Optional[str]:
        """Normalize customer/company code for matching.
        
        Args:
            value: Customer code value
            
        Returns:
            Normalized code or None
        """
        text = DataNormalizer.normalize_text(value)
        if not text:
            return None
        
        # Remove whitespace, convert to uppercase for matching
        normalized = re.sub(r'\s+', '', text).upper()
        return normalized if normalized else None
    
    @staticmethod
    def probability_category_to_value(category: str) -> Optional[float]:
        """Convert probability category to numeric value.
        
        Uses documented assumptions:
        - High: 0.70
        - Medium: 0.40
        - Low: 0.15
        
        Args:
            category: Probability category (High/Medium/Low)
            
        Returns:
            Numeric probability or None
        """
        if not category:
            return None
        
        category_lower = category.lower().strip()
        
        mapping = {
            "high": 0.70,
            "medium": 0.40,
            "med": 0.40,
            "low": 0.15
        }
        
        return mapping.get(category_lower)
