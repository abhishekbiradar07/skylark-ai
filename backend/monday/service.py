"""Monday.com data service - transforms raw data to business entities."""
import logging
from typing import Dict, List, Any, Optional
from data.models import Deal, WorkOrder, BoardMetadata, ColumnMetadata
from data.normalizer import DataNormalizer

logger = logging.getLogger(__name__)


class ColumnMapper:
    """Maps Monday.com columns to semantic fields."""
    
    def __init__(self, columns: List[Dict[str, Any]]):
        """Initialize column mapper.
        
        Args:
            columns: List of column metadata from Monday.com
        """
        self.columns = columns
        self.id_to_title = {col["id"]: col["title"].lower() for col in columns}
        self.title_to_id = {col["title"].lower(): col["id"] for col in columns}
    
    def find_column(self, *aliases: str) -> Optional[str]:
        """Find column ID by alias matching.
        
        Args:
            aliases: Possible column names/aliases
            
        Returns:
            Column ID or None
        """
        for alias in aliases:
            alias_lower = alias.lower()
            
            # Exact match
            if alias_lower in self.title_to_id:
                return self.title_to_id[alias_lower]
            
            # Partial match
            for title, col_id in self.title_to_id.items():
                if alias_lower in title or title in alias_lower:
                    return col_id
        
        return None
    
    def get_value(self, item: Dict[str, Any], *aliases: str) -> Any:
        """Get value from item by column aliases.
        
        Args:
            item: Monday.com item
            aliases: Possible column names
            
        Returns:
            Column value or None
        """
        col_id = self.find_column(*aliases)
        if not col_id:
            return None
        
        column_values = item.get("column_values", [])
        for col_val in column_values:
            if col_val.get("id") == col_id:
                return DataNormalizer.extract_column_value(col_val)
        
        return None


class MondayService:
    """Service for transforming Monday.com data."""
    
    @staticmethod
    def parse_deals(board_data: Dict[str, Any]) -> List[Deal]:
        """Parse deals from Monday.com board data.
        
        Args:
            board_data: Complete board data with columns and items
            
        Returns:
            List of Deal entities
        """
        columns = board_data.get("columns", [])
        items = board_data.get("items", [])
        
        mapper = ColumnMapper(columns)
        deals = []
        
        logger.info(f"Parsing {len(items)} deals")
        
        for item in items:
            try:
                # Extract raw values
                deal_name = item.get("name", "")
                customer = mapper.get_value(item, "customer", "customer name", "company", "customer name code")
                sector = mapper.get_value(item, "sector", "industry")
                owner = mapper.get_value(item, "owner", "account owner", "sales owner", "owner code")
                status = mapper.get_value(item, "status", "deal status", "stage")
                close_date_raw = mapper.get_value(item, "close date", "expected close", "closing date", "date")
                probability_raw = mapper.get_value(item, "probability", "win probability", "chance")
                deal_value_raw = mapper.get_value(item, "deal value", "value", "amount", "opportunity value")
                masked_value_raw = mapper.get_value(item, "masked deal value", "masked value")
                
                # Normalize
                customer_normalized = DataNormalizer.normalize_text(customer)
                customer_code = DataNormalizer.normalize_customer_code(customer)
                sector_normalized = DataNormalizer.normalize_text(sector)
                owner_normalized = DataNormalizer.normalize_text(owner)
                status_normalized = DataNormalizer.normalize_status(status)
                close_date = DataNormalizer.normalize_date(close_date_raw)
                deal_value = DataNormalizer.normalize_number(deal_value_raw)
                masked_value = DataNormalizer.normalize_number(masked_value_raw)
                
                # Handle probability
                probability = DataNormalizer.normalize_percentage(probability_raw)
                probability_category = None
                
                # If probability is text category
                if probability is None and isinstance(probability_raw, str):
                    probability_category = DataNormalizer.normalize_text(probability_raw)
                    probability = DataNormalizer.probability_category_to_value(probability_category)
                
                # Calculate weighted value
                weighted_value = None
                if deal_value is not None and probability is not None:
                    weighted_value = deal_value * probability
                
                deal = Deal(
                    deal_id=item.get("id", ""),
                    deal_name=deal_name,
                    customer=customer_normalized,
                    customer_code=customer_code,
                    sector=sector_normalized,
                    owner=owner_normalized,
                    deal_status=status_normalized,
                    close_date=close_date,
                    probability=probability,
                    probability_category=probability_category,
                    deal_value=deal_value,
                    masked_value=masked_value,
                    weighted_value=weighted_value,
                    raw_data={
                        "customer_raw": customer,
                        "sector_raw": sector,
                        "owner_raw": owner,
                        "status_raw": status,
                        "close_date_raw": close_date_raw,
                        "probability_raw": probability_raw,
                        "deal_value_raw": deal_value_raw,
                        "masked_value_raw": masked_value_raw
                    }
                )
                
                deals.append(deal)
                
            except Exception as e:
                logger.error(f"Error parsing deal {item.get('id')}: {e}")
                continue
        
        logger.info(f"Successfully parsed {len(deals)} deals")
        return deals
    
    @staticmethod
    def parse_work_orders(board_data: Dict[str, Any]) -> List[WorkOrder]:
        """Parse work orders from Monday.com board data.
        
        Args:
            board_data: Complete board data with columns and items
            
        Returns:
            List of WorkOrder entities
        """
        columns = board_data.get("columns", [])
        items = board_data.get("items", [])
        
        mapper = ColumnMapper(columns)
        work_orders = []
        
        logger.info(f"Parsing {len(items)} work orders")
        
        for item in items:
            try:
                # Extract raw values
                wo_name = item.get("name", "")
                customer = mapper.get_value(item, "customer", "customer name", "company", "customer name code")
                sector = mapper.get_value(item, "sector", "industry")
                owner = mapper.get_value(item, "owner", "owner code", "account owner")
                nature = mapper.get_value(item, "nature", "nature of work", "work type", "type of work")
                exec_status = mapper.get_value(item, "execution status", "execution", "status", "work status")
                data_delivery = mapper.get_value(item, "data delivery", "data delivery status", "delivery status")
                billing_status = mapper.get_value(item, "billing status", "billing", "invoice status")
                
                billed_value_raw = mapper.get_value(item, "billed value", "billed amount", "billed")
                collected_raw = mapper.get_value(item, "collected", "collected amount", "collection")
                to_bill_raw = mapper.get_value(item, "amount to be billed", "to be billed", "pending billing")
                quantity_raw = mapper.get_value(item, "quantity", "qty", "units")
                
                expected_billing_raw = mapper.get_value(item, "expected billing month", "expected billing", "billing month")
                actual_billing_raw = mapper.get_value(item, "actual billing month", "actual billing")
                
                # Normalize
                customer_normalized = DataNormalizer.normalize_text(customer)
                customer_code = DataNormalizer.normalize_customer_code(customer)
                sector_normalized = DataNormalizer.normalize_text(sector)
                owner_normalized = DataNormalizer.normalize_text(owner)
                nature_normalized = DataNormalizer.normalize_text(nature)
                exec_status_normalized = DataNormalizer.normalize_status(exec_status)
                data_delivery_normalized = DataNormalizer.normalize_status(data_delivery)
                billing_status_normalized = DataNormalizer.normalize_status(billing_status)
                
                billed_value = DataNormalizer.normalize_number(billed_value_raw)
                collected = DataNormalizer.normalize_number(collected_raw)
                to_bill = DataNormalizer.normalize_number(to_bill_raw)
                quantity = DataNormalizer.normalize_number(quantity_raw)
                
                expected_billing = DataNormalizer.normalize_date(expected_billing_raw)
                actual_billing = DataNormalizer.normalize_date(actual_billing_raw)
                
                work_order = WorkOrder(
                    work_order_id=item.get("id", ""),
                    work_order_name=wo_name,
                    customer=customer_normalized,
                    customer_code=customer_code,
                    sector=sector_normalized,
                    owner=owner_normalized,
                    nature_of_work=nature_normalized,
                    execution_status=exec_status_normalized,
                    data_delivery_status=data_delivery_normalized,
                    billing_status=billing_status_normalized,
                    billed_value=billed_value,
                    collected_amount=collected,
                    amount_to_bill=to_bill,
                    quantity=quantity,
                    expected_billing_month=expected_billing,
                    actual_billing_month=actual_billing,
                    raw_data={
                        "customer_raw": customer,
                        "sector_raw": sector,
                        "owner_raw": owner,
                        "nature_raw": nature,
                        "exec_status_raw": exec_status,
                        "data_delivery_raw": data_delivery,
                        "billing_status_raw": billing_status,
                        "billed_value_raw": billed_value_raw,
                        "collected_raw": collected_raw,
                        "to_bill_raw": to_bill_raw,
                        "quantity_raw": quantity_raw
                    }
                )
                
                work_orders.append(work_order)
                
            except Exception as e:
                logger.error(f"Error parsing work order {item.get('id')}: {e}")
                continue
        
        logger.info(f"Successfully parsed {len(work_orders)} work orders")
        return work_orders
