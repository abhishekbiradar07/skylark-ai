"""Mock data for demo mode."""
from datetime import datetime, timedelta
from data.models import Deal, WorkOrder

def generate_mock_deals():
    """Generate mock deals for demo."""
    return [
        Deal(
            deal_id="1",
            deal_name="Mining Expansion Project - ABC Corp",
            customer="ABC Mining Corporation",
            customer_code="ABC",
            sector="Mining",
            owner="John Smith",
            deal_status="open",
            close_date=datetime.now() + timedelta(days=30),
            probability=0.7,
            deal_value=25000000.0,
            weighted_value=17500000.0
        ),
        Deal(
            deal_id="2",
            deal_name="Infrastructure Upgrade - XYZ Ltd",
            customer="XYZ Infrastructure Ltd",
            customer_code="XYZ",
            sector="Infrastructure",
            owner="Jane Doe",
            deal_status="open",
            close_date=datetime.now() + timedelta(days=45),
            probability=0.4,
            deal_value=15000000.0,
            weighted_value=6000000.0
        ),
        Deal(
            deal_id="3",
            deal_name="Energy Project - PowerTech",
            customer="PowerTech Energy",
            customer_code="POW",
            sector="Energy",
            owner="John Smith",
            deal_status="open",
            close_date=datetime.now() + timedelta(days=60),
            probability=0.7,
            deal_value=30000000.0,
            weighted_value=21000000.0
        ),
        Deal(
            deal_id="4",
            deal_name="Transportation System - TransCo",
            customer="TransCo Systems",
            customer_code="TRA",
            sector="Transportation",
            owner="Mike Johnson",
            deal_status="open",
            close_date=datetime.now() + timedelta(days=20),
            probability=0.15,
            deal_value=8000000.0,
            weighted_value=1200000.0
        ),
        Deal(
            deal_id="5",
            deal_name="Real Estate Development - BuildCorp",
            customer="BuildCorp Realty",
            customer_code="BUI",
            sector="Real Estate",
            owner="Sarah Williams",
            deal_status="open",
            close_date=datetime.now() + timedelta(days=90),
            probability=0.4,
            deal_value=12000000.0,
            weighted_value=4800000.0
        ),
    ]

def generate_mock_work_orders():
    """Generate mock work orders for demo."""
    return [
        WorkOrder(
            work_order_id="1",
            work_order_name="Site Survey - ABC Mining",
            customer="ABC Mining Corporation",
            customer_code="ABC",
            sector="Mining",
            owner="John Smith",
            nature_of_work="Surveying",
            execution_status="completed",
            data_delivery_status="delivered",
            billing_status="billed",
            billed_value=5000000.0,
            collected_amount=5000000.0,
            amount_to_bill=0.0,
            quantity=100.0
        ),
        WorkOrder(
            work_order_id="2",
            work_order_name="Design Services - XYZ Infrastructure",
            customer="XYZ Infrastructure Ltd",
            customer_code="XYZ",
            sector="Infrastructure",
            owner="Jane Doe",
            nature_of_work="Design",
            execution_status="ongoing",
            data_delivery_status="pending",
            billing_status="partially billed",
            billed_value=3000000.0,
            collected_amount=2000000.0,
            amount_to_bill=2000000.0,
            quantity=75.0
        ),
        WorkOrder(
            work_order_id="3",
            work_order_name="Engineering Study - PowerTech",
            customer="PowerTech Energy",
            customer_code="POW",
            sector="Energy",
            owner="John Smith",
            nature_of_work="Engineering",
            execution_status="completed",
            data_delivery_status="delivered",
            billing_status="billed",
            billed_value=8000000.0,
            collected_amount=7500000.0,
            amount_to_bill=0.0,
            quantity=120.0
        ),
        WorkOrder(
            work_order_id="4",
            work_order_name="Feasibility Study - TransCo",
            customer="TransCo Systems",
            customer_code="TRA",
            sector="Transportation",
            owner="Mike Johnson",
            nature_of_work="Consulting",
            execution_status="ongoing",
            data_delivery_status="in progress",
            billing_status="not billed",
            billed_value=0.0,
            collected_amount=0.0,
            amount_to_bill=1500000.0,
            quantity=50.0
        ),
        WorkOrder(
            work_order_id="5",
            work_order_name="Planning Services - BuildCorp",
            customer="BuildCorp Realty",
            customer_code="BUI",
            sector="Real Estate",
            owner="Sarah Williams",
            nature_of_work="Planning",
            execution_status="not started",
            data_delivery_status="not started",
            billing_status="not billed",
            billed_value=0.0,
            collected_amount=0.0,
            amount_to_bill=2500000.0,
            quantity=60.0
        ),
    ]
