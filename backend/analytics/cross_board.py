"""Cross-board analytics."""
import logging
from typing import List, Dict, Any
from collections import defaultdict
from data.models import Deal, WorkOrder

logger = logging.getLogger(__name__)


class CrossBoardAnalytics:
    """Analytics across Deals and Work Orders boards."""
    
    @staticmethod
    def compare_by_sector(deals: List[Deal], work_orders: List[WorkOrder]) -> List[Dict[str, Any]]:
        """Compare deals and work orders by sector.
        
        Args:
            deals: List of deals
            work_orders: List of work orders
            
        Returns:
            Sector comparison data
        """
        # Collect all sectors
        all_sectors = set()
        all_sectors.update(d.sector for d in deals if d.sector)
        all_sectors.update(w.sector for w in work_orders if w.sector)
        
        # Build sector data
        sector_data = {}
        
        for sector in all_sectors:
            sector_deals = [d for d in deals if d.sector == sector]
            sector_wos = [w for w in work_orders if w.sector == sector]
            
            pipeline = sum(d.deal_value for d in sector_deals if d.deal_value is not None)
            weighted_pipeline = sum(d.weighted_value for d in sector_deals if d.weighted_value is not None)
            billed = sum(w.billed_value for w in sector_wos if w.billed_value is not None)
            collected = sum(w.collected_amount for w in sector_wos if w.collected_amount is not None)
            
            sector_data[sector] = {
                "sector": sector,
                "deals": {
                    "count": len(sector_deals),
                    "pipeline": pipeline,
                    "weighted_pipeline": weighted_pipeline
                },
                "work_orders": {
                    "count": len(sector_wos),
                    "billed": billed,
                    "collected": collected
                }
            }
        
        # Convert to list and sort by total activity
        result = list(sector_data.values())
        result.sort(key=lambda x: x["deals"]["pipeline"] + x["work_orders"]["billed"], reverse=True)
        
        return result
    
    @staticmethod
    def match_customers(deals: List[Deal], work_orders: List[WorkOrder]) -> Dict[str, Any]:
        """Match customers across boards.
        
        Uses customer_code for matching. Reports matching statistics.
        
        Args:
            deals: List of deals
            work_orders: List of work orders
            
        Returns:
            Customer matching analysis
        """
        # Get customer codes from each board
        deal_customers = set()
        wo_customers = set()
        
        for deal in deals:
            if deal.customer_code:
                deal_customers.add(deal.customer_code)
        
        for wo in work_orders:
            if wo.customer_code:
                wo_customers.add(wo.customer_code)
        
        # Find overlap
        common_customers = deal_customers.intersection(wo_customers)
        only_deals = deal_customers - wo_customers
        only_wos = wo_customers - deal_customers
        
        # Detailed analysis for common customers
        common_customer_data = []
        
        for customer_code in common_customers:
            customer_deals = [d for d in deals if d.customer_code == customer_code]
            customer_wos = [w for w in work_orders if w.customer_code == customer_code]
            
            pipeline = sum(d.deal_value for d in customer_deals if d.deal_value is not None)
            billed = sum(w.billed_value for w in customer_wos if w.billed_value is not None)
            
            # Get customer display name (prefer from deals)
            customer_name = customer_deals[0].customer if customer_deals else customer_wos[0].customer if customer_wos else customer_code
            
            common_customer_data.append({
                "customer_code": customer_code,
                "customer_name": customer_name,
                "deal_count": len(customer_deals),
                "wo_count": len(customer_wos),
                "pipeline": pipeline,
                "billed": billed
            })
        
        common_customer_data.sort(key=lambda x: x["pipeline"] + x["billed"], reverse=True)
        
        return {
            "total_deal_customers": len(deal_customers),
            "total_wo_customers": len(wo_customers),
            "common_customers": len(common_customers),
            "only_in_deals": len(only_deals),
            "only_in_wos": len(only_wos),
            "matching_rate": len(common_customers) / max(len(deal_customers), 1),
            "common_customer_details": common_customer_data[:20]  # Top 20
        }
    
    @staticmethod
    def sector_health_analysis(deals: List[Deal], work_orders: List[WorkOrder]) -> List[Dict[str, Any]]:
        """Analyze sector health: pipeline vs execution.
        
        Identifies sectors with:
        - Strong pipeline, strong execution (healthy)
        - Strong pipeline, weak execution (growth opportunity)
        - Weak pipeline, strong execution (at risk)
        - Weak pipeline, weak execution (struggling)
        
        Args:
            deals: List of deals
            work_orders: List of work orders
            
        Returns:
            Sector health analysis
        """
        sector_comparison = CrossBoardAnalytics.compare_by_sector(deals, work_orders)
        
        if not sector_comparison:
            return []
        
        # Calculate medians for classification
        pipelines = [s["deals"]["pipeline"] for s in sector_comparison if s["deals"]["pipeline"] > 0]
        billeds = [s["work_orders"]["billed"] for s in sector_comparison if s["work_orders"]["billed"] > 0]
        
        median_pipeline = sorted(pipelines)[len(pipelines) // 2] if pipelines else 0
        median_billed = sorted(billeds)[len(billeds) // 2] if billeds else 0
        
        # Classify sectors
        for sector in sector_comparison:
            pipeline = sector["deals"]["pipeline"]
            billed = sector["work_orders"]["billed"]
            
            if pipeline >= median_pipeline and billed >= median_billed:
                health = "Healthy"
                insight = "Strong pipeline and execution"
            elif pipeline >= median_pipeline and billed < median_billed:
                health = "Growth Opportunity"
                insight = "Strong pipeline but weaker execution"
            elif pipeline < median_pipeline and billed >= median_billed:
                health = "At Risk"
                insight = "Strong execution but weaker pipeline"
            else:
                health = "Needs Attention"
                insight = "Lower pipeline and execution"
            
            sector["health"] = health
            sector["insight"] = insight
        
        return sector_comparison
