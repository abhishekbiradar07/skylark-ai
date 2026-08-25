"""Agent query routing and orchestration."""
import logging
from typing import Dict, Any, List
from data.models import Deal, WorkOrder
from data.quality import DataQualityAnalyzer
from analytics.metrics import DealsMetrics, WorkOrderMetrics
from analytics.cross_board import CrossBoardAnalytics
from agent.reasoning import AgentReasoning

logger = logging.getLogger(__name__)


class AgentRouter:
    """Routes queries and orchestrates analytics."""
    
    def __init__(self):
        """Initialize agent router."""
        self.reasoning = AgentReasoning()
    
    async def handle_query(
        self,
        question: str,
        deals: List[Deal],
        work_orders: List[WorkOrder]
    ) -> Dict[str, Any]:
        """Handle user query end-to-end.
        
        Args:
            question: User question
            deals: List of deals
            work_orders: List of work orders
            
        Returns:
            Response with answer, metrics, and metadata
        """
        logger.info(f"Handling query: {question}")
        
        # Step 1: Classify intent
        intent_data = await self.reasoning.classify_intent(question)
        intent = intent_data.get("intent", "PIPELINE_SUMMARY")
        
        logger.info(f"Classified intent: {intent}")
        
        # Step 2: Check if clarification needed
        if intent_data.get("requires_clarification"):
            clarification = intent_data.get("clarification_question", "Could you clarify your question?")
            return {
                "answer": clarification,
                "requires_clarification": True,
                "intent": intent,
                "data_sources": [],
                "metrics": {},
                "data_quality": []
            }
        
        # Step 3: Execute appropriate analytics
        metrics, data_sources, data_quality = await self._execute_analytics(
            intent,
            intent_data,
            deals,
            work_orders
        )
        
        # Step 4: Generate response
        if intent == "LEADERSHIP_UPDATE":
            answer = await self.reasoning.generate_leadership_update(metrics)
        else:
            answer = await self.reasoning.generate_response(
                question,
                intent,
                metrics,
                data_quality,
                data_sources
            )
        
        return {
            "answer": answer,
            "requires_clarification": False,
            "intent": intent,
            "data_sources": data_sources,
            "metrics": metrics,
            "data_quality": data_quality
        }
    
    async def _execute_analytics(
        self,
        intent: str,
        intent_data: Dict[str, Any],
        deals: List[Deal],
        work_orders: List[WorkOrder]
    ) -> tuple[Dict[str, Any], List[str], List[str]]:
        """Execute analytics based on intent.
        
        Args:
            intent: Query intent
            intent_data: Full intent classification data
            deals: List of deals
            work_orders: List of work orders
            
        Returns:
            Tuple of (metrics, data_sources, data_quality_issues)
        """
        sector_filter = intent_data.get("sector_filter")
        owner_filter = intent_data.get("owner_filter")
        
        metrics = {}
        data_sources = []
        data_quality = []
        
        # Filter data if needed
        filtered_deals = deals
        filtered_wos = work_orders
        
        if sector_filter:
            filtered_deals = [d for d in deals if d.sector and sector_filter.lower() in d.sector.lower()]
            filtered_wos = [w for w in work_orders if w.sector and sector_filter.lower() in w.sector.lower()]
        
        if owner_filter:
            filtered_deals = [d for d in filtered_deals if d.owner and owner_filter.lower() in d.owner.lower()]
            filtered_wos = [w for w in filtered_wos if w.owner and owner_filter.lower() in w.owner.lower()]
        
        # Execute analytics based on intent
        if intent == "PIPELINE_SUMMARY":
            data_sources.append("Monday.com — Skylark — Deals")
            metrics["pipeline_summary"] = DealsMetrics.calculate_pipeline_summary(filtered_deals)
            
            # Data quality
            quality_report = DataQualityAnalyzer.analyze_deals(filtered_deals)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["sector", "value", "owner"])
        
        elif intent == "PIPELINE_BY_SECTOR":
            data_sources.append("Monday.com — Skylark — Deals")
            metrics["by_sector"] = DealsMetrics.calculate_by_sector(filtered_deals)
            
            quality_report = DataQualityAnalyzer.analyze_deals(filtered_deals)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["sector", "value"])
        
        elif intent == "PIPELINE_BY_OWNER":
            data_sources.append("Monday.com — Skylark — Deals")
            metrics["by_owner"] = DealsMetrics.calculate_by_owner(filtered_deals)
            
            quality_report = DataQualityAnalyzer.analyze_deals(filtered_deals)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["owner", "value"])
        
        elif intent == "TOP_DEALS":
            data_sources.append("Monday.com — Skylark — Deals")
            metrics["top_deals"] = DealsMetrics.get_top_deals(filtered_deals, limit=10)
            
            quality_report = DataQualityAnalyzer.analyze_deals(filtered_deals)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["value"])
        
        elif intent == "OPERATIONS_SUMMARY":
            data_sources.append("Monday.com — Skylark — Work Orders")
            metrics["operations_summary"] = WorkOrderMetrics.calculate_operations_summary(filtered_wos)
            
            quality_report = DataQualityAnalyzer.analyze_work_orders(filtered_wos)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["execution", "billing"])
        
        elif intent == "OPERATIONS_BY_SECTOR":
            data_sources.append("Monday.com — Skylark — Work Orders")
            metrics["by_sector"] = WorkOrderMetrics.calculate_by_sector(filtered_wos)
            
            quality_report = DataQualityAnalyzer.analyze_work_orders(filtered_wos)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["sector"])
        
        elif intent == "OPERATIONS_BY_OWNER":
            data_sources.append("Monday.com — Skylark — Work Orders")
            metrics["by_owner"] = WorkOrderMetrics.calculate_by_owner(filtered_wos)
            
            quality_report = DataQualityAnalyzer.analyze_work_orders(filtered_wos)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["owner"])
        
        elif intent == "BILLING":
            data_sources.append("Monday.com — Skylark — Work Orders")
            ops_summary = WorkOrderMetrics.calculate_operations_summary(filtered_wos)
            metrics["billing"] = ops_summary["billing"]
            metrics["total_work_orders"] = ops_summary["total_work_orders"]
            
            quality_report = DataQualityAnalyzer.analyze_work_orders(filtered_wos)
            data_quality = DataQualityAnalyzer.get_relevant_issues(quality_report, ["billing"])
        
        elif intent == "CROSS_BOARD" or intent == "SECTOR_HEALTH":
            data_sources.extend(["Monday.com — Skylark — Deals", "Monday.com — Skylark — Work Orders"])
            metrics["sector_comparison"] = CrossBoardAnalytics.compare_by_sector(filtered_deals, filtered_wos)
            metrics["sector_health"] = CrossBoardAnalytics.sector_health_analysis(filtered_deals, filtered_wos)
            metrics["customer_matching"] = CrossBoardAnalytics.match_customers(filtered_deals, filtered_wos)
            
            deals_quality = DataQualityAnalyzer.analyze_deals(filtered_deals)
            wos_quality = DataQualityAnalyzer.analyze_work_orders(filtered_wos)
            data_quality.extend(DataQualityAnalyzer.get_relevant_issues(deals_quality, ["sector"]))
            data_quality.extend(DataQualityAnalyzer.get_relevant_issues(wos_quality, ["sector"]))
        
        elif intent == "LEADERSHIP_UPDATE":
            data_sources.extend(["Monday.com — Skylark — Deals", "Monday.com — Skylark — Work Orders"])
            
            # Comprehensive metrics
            metrics["pipeline"] = DealsMetrics.calculate_pipeline_summary(deals)
            metrics["pipeline_by_sector"] = DealsMetrics.calculate_by_sector(deals)
            metrics["top_deals"] = DealsMetrics.get_top_deals(deals, limit=5)
            
            metrics["operations"] = WorkOrderMetrics.calculate_operations_summary(work_orders)
            metrics["operations_by_sector"] = WorkOrderMetrics.calculate_by_sector(work_orders)
            
            metrics["cross_board"] = CrossBoardAnalytics.sector_health_analysis(deals, work_orders)
            metrics["customer_matching"] = CrossBoardAnalytics.match_customers(deals, work_orders)
            
            # Data quality summary
            deals_quality = DataQualityAnalyzer.analyze_deals(deals)
            wos_quality = DataQualityAnalyzer.analyze_work_orders(work_orders)
            data_quality.append(f"Deals completeness: {deals_quality.completeness_score:.1f}%")
            data_quality.append(f"Work Orders completeness: {wos_quality.completeness_score:.1f}%")
        
        else:
            # Default to pipeline summary
            data_sources.append("Monday.com — Skylark — Deals")
            metrics["pipeline_summary"] = DealsMetrics.calculate_pipeline_summary(filtered_deals)
        
        return metrics, data_sources, data_quality
