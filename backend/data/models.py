"""Data models for board items."""
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ColumnMetadata(BaseModel):
    """Monday.com column metadata."""
    id: str
    title: str
    type: str
    settings: Optional[Dict[str, Any]] = None


class BoardMetadata(BaseModel):
    """Monday.com board metadata."""
    board_id: str
    board_name: str
    description: Optional[str] = None
    columns: List[ColumnMetadata]


class NormalizedValue(BaseModel):
    """Normalized column value with original."""
    raw: Optional[str] = None
    normalized: Optional[Any] = None
    is_missing: bool = False
    data_type: str = "unknown"


class BoardItem(BaseModel):
    """Normalized board item."""
    item_id: str
    item_name: str
    raw_values: Dict[str, Any] = Field(default_factory=dict)
    normalized_values: Dict[str, NormalizedValue] = Field(default_factory=dict)


class DataQualityIssue(BaseModel):
    """Data quality issue."""
    field: str
    issue_type: str
    count: int
    percentage: float
    description: str


class BoardDataQuality(BaseModel):
    """Data quality report for a board."""
    board_name: str
    total_items: int
    issues: List[DataQualityIssue]
    completeness_score: float
    
    
class WorkOrder(BaseModel):
    """Work order business entity."""
    work_order_id: str
    work_order_name: str
    customer: Optional[str] = None
    customer_code: Optional[str] = None
    sector: Optional[str] = None
    owner: Optional[str] = None
    nature_of_work: Optional[str] = None
    execution_status: Optional[str] = None
    data_delivery_status: Optional[str] = None
    billing_status: Optional[str] = None
    billed_value: Optional[float] = None
    collected_amount: Optional[float] = None
    amount_to_bill: Optional[float] = None
    quantity: Optional[float] = None
    expected_billing_month: Optional[datetime] = None
    actual_billing_month: Optional[datetime] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class Deal(BaseModel):
    """Deal business entity."""
    deal_id: str
    deal_name: str
    customer: Optional[str] = None
    customer_code: Optional[str] = None
    sector: Optional[str] = None
    owner: Optional[str] = None
    deal_status: Optional[str] = None
    close_date: Optional[datetime] = None
    probability: Optional[float] = None
    probability_category: Optional[str] = None
    deal_value: Optional[float] = None
    masked_value: Optional[float] = None
    weighted_value: Optional[float] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)
