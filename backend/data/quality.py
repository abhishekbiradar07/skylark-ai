"""Data quality assessment."""
import logging
from typing import List, Dict, Any
from data.models import Deal, WorkOrder, DataQualityIssue, BoardDataQuality

logger = logging.getLogger(__name__)


class DataQualityAnalyzer:
    """Analyze data quality issues."""
    
    @staticmethod
    def analyze_deals(deals: List[Deal]) -> BoardDataQuality:
        """Analyze deal data quality.
        
        Args:
            deals: List of deals
            
        Returns:
            Data quality report
        """
        total = len(deals)
        if total == 0:
            return BoardDataQuality(
                board_name="Deals",
                total_items=0,
                issues=[],
                completeness_score=0.0
            )
        
        issues = []
        
        # Missing sector
        missing_sector = sum(1 for d in deals if not d.sector)
        if missing_sector > 0:
            issues.append(DataQualityIssue(
                field="sector",
                issue_type="missing",
                count=missing_sector,
                percentage=missing_sector / total * 100,
                description=f"{missing_sector} deals have missing sector values"
            ))
        
        # Missing value
        missing_value = sum(1 for d in deals if d.deal_value is None)
        if missing_value > 0:
            issues.append(DataQualityIssue(
                field="deal_value",
                issue_type="missing",
                count=missing_value,
                percentage=missing_value / total * 100,
                description=f"{missing_value} deals have missing deal value"
            ))
        
        # Missing close date
        missing_close_date = sum(1 for d in deals if d.close_date is None)
        if missing_close_date > 0:
            issues.append(DataQualityIssue(
                field="close_date",
                issue_type="missing",
                count=missing_close_date,
                percentage=missing_close_date / total * 100,
                description=f"{missing_close_date} deals have missing close date"
            ))
        
        # Missing owner
        missing_owner = sum(1 for d in deals if not d.owner)
        if missing_owner > 0:
            issues.append(DataQualityIssue(
                field="owner",
                issue_type="missing",
                count=missing_owner,
                percentage=missing_owner / total * 100,
                description=f"{missing_owner} deals have missing owner"
            ))
        
        # Missing customer
        missing_customer = sum(1 for d in deals if not d.customer)
        if missing_customer > 0:
            issues.append(DataQualityIssue(
                field="customer",
                issue_type="missing",
                count=missing_customer,
                percentage=missing_customer / total * 100,
                description=f"{missing_customer} deals have missing customer"
            ))
        
        # Missing probability
        missing_probability = sum(1 for d in deals if d.probability is None)
        if missing_probability > 0:
            issues.append(DataQualityIssue(
                field="probability",
                issue_type="missing",
                count=missing_probability,
                percentage=missing_probability / total * 100,
                description=f"{missing_probability} deals have missing probability"
            ))
        
        # Calculate completeness score
        key_fields = ["sector", "deal_value", "close_date", "owner", "customer"]
        total_fields = total * len(key_fields)
        missing_total = missing_sector + missing_value + missing_close_date + missing_owner + missing_customer
        completeness_score = (1 - missing_total / total_fields) * 100 if total_fields > 0 else 0
        
        return BoardDataQuality(
            board_name="Deals",
            total_items=total,
            issues=issues,
            completeness_score=completeness_score
        )
    
    @staticmethod
    def analyze_work_orders(work_orders: List[WorkOrder]) -> BoardDataQuality:
        """Analyze work order data quality.
        
        Args:
            work_orders: List of work orders
            
        Returns:
            Data quality report
        """
        total = len(work_orders)
        if total == 0:
            return BoardDataQuality(
                board_name="Work Orders",
                total_items=0,
                issues=[],
                completeness_score=0.0
            )
        
        issues = []
        
        # Missing sector
        missing_sector = sum(1 for w in work_orders if not w.sector)
        if missing_sector > 0:
            issues.append(DataQualityIssue(
                field="sector",
                issue_type="missing",
                count=missing_sector,
                percentage=missing_sector / total * 100,
                description=f"{missing_sector} work orders have missing sector values"
            ))
        
        # Missing execution status
        missing_exec_status = sum(1 for w in work_orders if not w.execution_status)
        if missing_exec_status > 0:
            issues.append(DataQualityIssue(
                field="execution_status",
                issue_type="missing",
                count=missing_exec_status,
                percentage=missing_exec_status / total * 100,
                description=f"{missing_exec_status} work orders have missing execution status"
            ))
        
        # Missing billing values
        missing_billed = sum(1 for w in work_orders if w.billed_value is None)
        if missing_billed > 0:
            issues.append(DataQualityIssue(
                field="billed_value",
                issue_type="missing",
                count=missing_billed,
                percentage=missing_billed / total * 100,
                description=f"{missing_billed} work orders have missing billed value"
            ))
        
        # Missing owner
        missing_owner = sum(1 for w in work_orders if not w.owner)
        if missing_owner > 0:
            issues.append(DataQualityIssue(
                field="owner",
                issue_type="missing",
                count=missing_owner,
                percentage=missing_owner / total * 100,
                description=f"{missing_owner} work orders have missing owner"
            ))
        
        # Missing customer
        missing_customer = sum(1 for w in work_orders if not w.customer)
        if missing_customer > 0:
            issues.append(DataQualityIssue(
                field="customer",
                issue_type="missing",
                count=missing_customer,
                percentage=missing_customer / total * 100,
                description=f"{missing_customer} work orders have missing customer"
            ))
        
        # Calculate completeness score
        key_fields = ["sector", "execution_status", "billed_value", "owner", "customer"]
        total_fields = total * len(key_fields)
        missing_total = missing_sector + missing_exec_status + missing_billed + missing_owner + missing_customer
        completeness_score = (1 - missing_total / total_fields) * 100 if total_fields > 0 else 0
        
        return BoardDataQuality(
            board_name="Work Orders",
            total_items=total,
            issues=issues,
            completeness_score=completeness_score
        )
    
    @staticmethod
    def get_relevant_issues(quality_report: BoardDataQuality, mentioned_fields: List[str]) -> List[str]:
        """Get data quality issues relevant to mentioned fields.
        
        Args:
            quality_report: Data quality report
            mentioned_fields: Fields mentioned in query
            
        Returns:
            List of relevant issue descriptions
        """
        relevant = []
        
        for issue in quality_report.issues:
            if any(field.lower() in issue.field.lower() for field in mentioned_fields):
                relevant.append(issue.description)
        
        return relevant
