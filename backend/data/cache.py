"""Data cache management."""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from data.models import Deal, WorkOrder
from config import config

logger = logging.getLogger(__name__)


class DataCache:
    """In-memory cache for Monday.com data."""
    
    def __init__(self):
        """Initialize cache."""
        self._deals: Optional[List[Deal]] = None
        self._work_orders: Optional[List[WorkOrder]] = None
        self._deals_raw: Optional[Dict[str, Any]] = None
        self._work_orders_raw: Optional[Dict[str, Any]] = None
        self._last_refresh: Optional[datetime] = None
        self._cache_duration = timedelta(minutes=config.CACHE_DURATION_MINUTES)
    
    def is_expired(self) -> bool:
        """Check if cache is expired.
        
        Returns:
            True if cache needs refresh
        """
        if self._last_refresh is None:
            return True
        
        return datetime.now() - self._last_refresh > self._cache_duration
    
    def get_deals(self) -> Optional[List[Deal]]:
        """Get cached deals.
        
        Returns:
            List of deals or None if not cached/expired
        """
        if self.is_expired():
            return None
        return self._deals
    
    def get_work_orders(self) -> Optional[List[WorkOrder]]:
        """Get cached work orders.
        
        Returns:
            List of work orders or None if not cached/expired
        """
        if self.is_expired():
            return None
        return self._work_orders
    
    def set_deals(self, deals: List[Deal], raw_data: Dict[str, Any]):
        """Cache deals data.
        
        Args:
            deals: List of Deal entities
            raw_data: Raw board data
        """
        self._deals = deals
        self._deals_raw = raw_data
        self._last_refresh = datetime.now()
        logger.info(f"Cached {len(deals)} deals")
    
    def set_work_orders(self, work_orders: List[WorkOrder], raw_data: Dict[str, Any]):
        """Cache work orders data.
        
        Args:
            work_orders: List of WorkOrder entities
            raw_data: Raw board data
        """
        self._work_orders = work_orders
        self._work_orders_raw = raw_data
        self._last_refresh = datetime.now()
        logger.info(f"Cached {len(work_orders)} work orders")
    
    def clear(self):
        """Clear all cached data."""
        self._deals = None
        self._work_orders = None
        self._deals_raw = None
        self._work_orders_raw = None
        self._last_refresh = None
        logger.info("Cache cleared")
    
    def get_last_refresh_time(self) -> Optional[datetime]:
        """Get last refresh timestamp.
        
        Returns:
            Last refresh datetime or None
        """
        return self._last_refresh
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information.
        
        Returns:
            Cache status information
        """
        return {
            "last_refresh": self._last_refresh.isoformat() if self._last_refresh else None,
            "is_expired": self.is_expired(),
            "deals_count": len(self._deals) if self._deals else 0,
            "work_orders_count": len(self._work_orders) if self._work_orders else 0,
            "cache_duration_minutes": config.CACHE_DURATION_MINUTES
        }


# Global cache instance
data_cache = DataCache()
