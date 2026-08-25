"""Data validation layer."""
import logging
from typing import List, Dict, Any, Tuple
from data.models import Deal, WorkOrder

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate business entities after normalization."""
    
    @staticmethod
    def validate_deal(deal: Deal) -> Tuple[bool, List[str]]:
        """Validate a deal entity.
        
        Args:
            deal: Deal to validate
            
        Returns:
            Tuple of (is_valid, list of validation issues)
        """
        issues = []
        
        # Critical fields
        if not deal.deal_name or deal.deal_name.strip() == "":
            issues.append("Missing deal name")
        
        # Value validations
        if deal.deal_value is not None and deal.deal_value < 0:
            issues.append(f"Negative deal value: {deal.deal_value}")
        
        if deal.masked_value is not None and deal.masked_value < 0:
            issues.append(f"Negative masked value: {deal.masked_value}")
        
        # Probability validations
        if deal.probability is not None:
            if deal.probability < 0 or deal.probability > 1:
                issues.append(f"Invalid probability: {deal.probability} (should be 0-1)")
        
        # Weighted value consistency
        if deal.weighted_value is not None:
            if deal.deal_value is None or deal.probability is None:
                issues.append("Weighted value present but deal_value or probability missing")
        
        # Date validations (deals in future are ok, very old deals might be stale)
        # We don't reject old dates, just note them
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    @staticmethod
    def validate_work_order(work_order: WorkOrder) -> Tuple[bool, List[str]]:
        """Validate a work order entity.
        
        Args:
            work_order: Work order to validate
            
        Returns:
            Tuple of (is_valid, list of validation issues)
        """
        issues = []
        
        # Critical fields
        if not work_order.work_order_name or work_order.work_order_name.strip() == "":
            issues.append("Missing work order name")
        
        # Value validations - negative values are issues
        if work_order.billed_value is not None and work_order.billed_value < 0:
            issues.append(f"Negative billed value: {work_order.billed_value}")
        
        if work_order.collected_amount is not None and work_order.collected_amount < 0:
            issues.append(f"Negative collected amount: {work_order.collected_amount}")
        
        if work_order.amount_to_bill is not None and work_order.amount_to_bill < 0:
            issues.append(f"Negative amount to bill: {work_order.amount_to_bill}")
        
        # Business logic validations
        if work_order.collected_amount is not None and work_order.billed_value is not None:
            if work_order.collected_amount > work_order.billed_value * 1.1:  # 10% tolerance for rounding
                issues.append(f"Collected ({work_order.collected_amount}) exceeds billed ({work_order.billed_value})")
        
        # Quantity validation
        if work_order.quantity is not None and work_order.quantity < 0:
            issues.append(f"Negative quantity: {work_order.quantity}")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    @staticmethod
    def validate_deals_batch(deals: List[Deal]) -> Dict[str, Any]:
        """Validate a batch of deals.
        
        Args:
            deals: List of deals
            
        Returns:
            Validation report
        """
        total = len(deals)
        valid_count = 0
        invalid_count = 0
        all_issues = []
        
        for deal in deals:
            is_valid, issues = DataValidator.validate_deal(deal)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                all_issues.extend([f"Deal {deal.deal_name}: {issue}" for issue in issues])
        
        return {
            "total": total,
            "valid": valid_count,
            "invalid": invalid_count,
            "validation_rate": valid_count / total if total > 0 else 0,
            "issues": all_issues[:20]  # Limit to first 20 issues
        }
    
    @staticmethod
    def validate_work_orders_batch(work_orders: List[WorkOrder]) -> Dict[str, Any]:
        """Validate a batch of work orders.
        
        Args:
            work_orders: List of work orders
            
        Returns:
            Validation report
        """
        total = len(work_orders)
        valid_count = 0
        invalid_count = 0
        all_issues = []
        
        for wo in work_orders:
            is_valid, issues = DataValidator.validate_work_order(wo)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                all_issues.extend([f"WO {wo.work_order_name}: {issue}" for issue in issues])
        
        return {
            "total": total,
            "valid": valid_count,
            "invalid": invalid_count,
            "validation_rate": valid_count / total if total > 0 else 0,
            "issues": all_issues[:20]  # Limit to first 20 issues
        }
