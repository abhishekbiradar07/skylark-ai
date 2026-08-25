"""Business metrics calculation."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict
from data.models import Deal, WorkOrder

logger = logging.getLogger(__name__)


class DealsMetrics:
    """Calculate deal/pipeline metrics."""
    
    @staticmethod
    def calculate_pipeline_summary(deals: List[Deal]) -> Dict[str, Any]:
        """Calculate overall pipeline summary.
        
        Args:
            deals: List of deals
            
        Returns:
            Pipeline summary metrics
        """
        total_deals = len(deals)
        
        # Filter for value
        deals_with_value = [d for d in deals if d.deal_value is not None]
        
        total_pipeline = sum(d.deal_value for d in deals_with_value)
        
        # Weighted pipeline
        deals_with_weighted = [d for d in deals if d.weighted_value is not None]
        weighted_pipeline = sum(d.weighted_value for d in deals_with_weighted)
        
        # Status breakdown
        open_deals = [d for d in deals if d.deal_status and "closed" not in d.deal_status and "won" not in d.deal_status and "lost" not in d.deal_status]
        closed_won = [d for d in deals if d.deal_status and ("won" in d.deal_status or "closed won" in d.deal_status)]
        closed_lost = [d for d in deals if d.deal_status and ("lost" in d.deal_status or "closed lost" in d.deal_status)]
        
        # Data quality
        missing_sector = sum(1 for d in deals if not d.sector)
        missing_value = sum(1 for d in deals if d.deal_value is None)
        missing_close_date = sum(1 for d in deals if d.close_date is None)
        
        return {
            "total_deals": total_deals,
            "deals_with_value": len(deals_with_value),
            "total_pipeline": total_pipeline,
            "weighted_pipeline": weighted_pipeline,
            "open_deals": len(open_deals),
            "closed_won": len(closed_won),
            "closed_lost": len(closed_lost),
            "data_quality": {
                "missing_sector": missing_sector,
                "missing_value": missing_value,
                "missing_close_date": missing_close_date
            }
        }
    
    @staticmethod
    def calculate_by_sector(deals: List[Deal]) -> List[Dict[str, Any]]:
        """Calculate pipeline by sector.
        
        Args:
            deals: List of deals
            
        Returns:
            List of sector metrics
        """
        sector_data = defaultdict(lambda: {
            "deal_count": 0,
            "pipeline": 0.0,
            "weighted_pipeline": 0.0
        })
        
        for deal in deals:
            sector = deal.sector or "Unknown"
            sector_data[sector]["deal_count"] += 1
            
            if deal.deal_value is not None:
                sector_data[sector]["pipeline"] += deal.deal_value
            
            if deal.weighted_value is not None:
                sector_data[sector]["weighted_pipeline"] += deal.weighted_value
        
        # Convert to list and sort by pipeline
        result = [
            {"sector": sector, **metrics}
            for sector, metrics in sector_data.items()
        ]
        result.sort(key=lambda x: x["pipeline"], reverse=True)
        
        return result
    
    @staticmethod
    def calculate_by_owner(deals: List[Deal]) -> List[Dict[str, Any]]:
        """Calculate pipeline by owner.
        
        Args:
            deals: List of deals
            
        Returns:
            List of owner metrics
        """
        owner_data = defaultdict(lambda: {
            "deal_count": 0,
            "pipeline": 0.0,
            "weighted_pipeline": 0.0
        })
        
        for deal in deals:
            owner = deal.owner or "Unknown"
            owner_data[owner]["deal_count"] += 1
            
            if deal.deal_value is not None:
                owner_data[owner]["pipeline"] += deal.deal_value
            
            if deal.weighted_value is not None:
                owner_data[owner]["weighted_pipeline"] += deal.weighted_value
        
        # Convert to list and sort by pipeline
        result = [
            {"owner": owner, **metrics}
            for owner, metrics in owner_data.items()
        ]
        result.sort(key=lambda x: x["pipeline"], reverse=True)
        
        return result
    
    @staticmethod
    def get_top_deals(deals: List[Deal], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top deals by value.
        
        Args:
            deals: List of deals
            limit: Number of top deals to return
            
        Returns:
            List of top deals
        """
        deals_with_value = [d for d in deals if d.deal_value is not None]
        deals_with_value.sort(key=lambda d: d.deal_value, reverse=True)
        
        return [
            {
                "deal_name": d.deal_name,
                "customer": d.customer,
                "sector": d.sector,
                "owner": d.owner,
                "deal_value": d.deal_value,
                "weighted_value": d.weighted_value,
                "probability": d.probability,
                "status": d.deal_status
            }
            for d in deals_with_value[:limit]
        ]


class WorkOrderMetrics:
    """Calculate work order/operations metrics."""
    
    @staticmethod
    def calculate_operations_summary(work_orders: List[WorkOrder]) -> Dict[str, Any]:
        """Calculate overall operations summary.
        
        Args:
            work_orders: List of work orders
            
        Returns:
            Operations summary metrics
        """
        total_wos = len(work_orders)
        
        # Execution status breakdown
        completed = [w for w in work_orders if w.execution_status and "completed" in w.execution_status]
        ongoing = [w for w in work_orders if w.execution_status and ("ongoing" in w.execution_status or "in progress" in w.execution_status)]
        not_started = [w for w in work_orders if w.execution_status and "not started" in w.execution_status]
        
        # Billing metrics
        wos_with_billed = [w for w in work_orders if w.billed_value is not None]
        total_billed = sum(w.billed_value for w in wos_with_billed)
        
        wos_with_collected = [w for w in work_orders if w.collected_amount is not None]
        total_collected = sum(w.collected_amount for w in wos_with_collected)
        
        wos_with_to_bill = [w for w in work_orders if w.amount_to_bill is not None]
        total_to_bill = sum(w.amount_to_bill for w in wos_with_to_bill)
        
        outstanding = total_billed - total_collected if wos_with_billed and wos_with_collected else 0
        
        # Data quality
        missing_sector = sum(1 for w in work_orders if not w.sector)
        missing_exec_status = sum(1 for w in work_orders if not w.execution_status)
        
        return {
            "total_work_orders": total_wos,
            "completed": len(completed),
            "ongoing": len(ongoing),
            "not_started": len(not_started),
            "billing": {
                "total_billed": total_billed,
                "total_collected": total_collected,
                "total_to_bill": total_to_bill,
                "outstanding": outstanding
            },
            "data_quality": {
                "missing_sector": missing_sector,
                "missing_exec_status": missing_exec_status
            }
        }
    
    @staticmethod
    def calculate_by_sector(work_orders: List[WorkOrder]) -> List[Dict[str, Any]]:
        """Calculate work orders by sector.
        
        Args:
            work_orders: List of work orders
            
        Returns:
            List of sector metrics
        """
        sector_data = defaultdict(lambda: {
            "wo_count": 0,
            "billed_value": 0.0,
            "collected": 0.0,
            "to_bill": 0.0
        })
        
        for wo in work_orders:
            sector = wo.sector or "Unknown"
            sector_data[sector]["wo_count"] += 1
            
            if wo.billed_value is not None:
                sector_data[sector]["billed_value"] += wo.billed_value
            
            if wo.collected_amount is not None:
                sector_data[sector]["collected"] += wo.collected_amount
            
            if wo.amount_to_bill is not None:
                sector_data[sector]["to_bill"] += wo.amount_to_bill
        
        # Convert to list and sort by billed value
        result = [
            {"sector": sector, **metrics}
            for sector, metrics in sector_data.items()
        ]
        result.sort(key=lambda x: x["billed_value"], reverse=True)
        
        return result
    
    @staticmethod
    def calculate_by_owner(work_orders: List[WorkOrder]) -> List[Dict[str, Any]]:
        """Calculate work orders by owner.
        
        Args:
            work_orders: List of work orders
            
        Returns:
            List of owner metrics
        """
        owner_data = defaultdict(lambda: {
            "wo_count": 0,
            "billed_value": 0.0,
            "collected": 0.0,
            "to_bill": 0.0
        })
        
        for wo in work_orders:
            owner = wo.owner or "Unknown"
            owner_data[owner]["wo_count"] += 1
            
            if wo.billed_value is not None:
                owner_data[owner]["billed_value"] += wo.billed_value
            
            if wo.collected_amount is not None:
                owner_data[owner]["collected"] += wo.collected_amount
            
            if wo.amount_to_bill is not None:
                owner_data[owner]["to_bill"] += wo.amount_to_bill
        
        # Convert to list and sort by billed value
        result = [
            {"owner": owner, **metrics}
            for owner, metrics in owner_data.items()
        ]
        result.sort(key=lambda x: x["billed_value"], reverse=True)
        
        return result
