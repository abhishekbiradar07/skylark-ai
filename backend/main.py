"""Skylark BI Agent - FastAPI application."""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from config import config
from monday.client import MondayClient, MondayAPIError
from monday.service import MondayService
from data.cache import data_cache
from data.quality import DataQualityAnalyzer
from agent.router import AgentRouter
from mock_data import generate_mock_deals, generate_mock_work_orders

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Skylark Business Intelligence Agent",
    description="AI-powered business intelligence from Monday.com",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
monday_client = MondayClient()
agent_router = AgentRouter()


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    answer: str
    data_sources: List[str]
    metrics: Dict[str, Any]
    data_quality: List[str]
    requires_clarification: bool = False
    intent: Optional[str] = None


# API Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    errors = config.validate()
    
    if errors:
        return {
            "status": "unhealthy",
            "errors": errors
        }
    
    return {
        "status": "healthy",
        "llm_provider": "Groq",
        "monday_configured": bool(config.MONDAY_API_TOKEN),
        "groq_configured": bool(config.GROQ_API_KEY),
        "cache_info": data_cache.get_cache_info()
    }


@app.post("/api/refresh")
async def refresh_data():
    """Refresh data from Monday.com."""
    try:
        logger.info("Refreshing data from Monday.com")
        
        # Fetch deals
        deals_data = await monday_client.get_all_board_data(config.MONDAY_DEALS_BOARD_ID)
        deals = MondayService.parse_deals(deals_data)
        data_cache.set_deals(deals, deals_data)
        
        # Fetch work orders
        wo_data = await monday_client.get_all_board_data(config.MONDAY_WORK_ORDERS_BOARD_ID)
        work_orders = MondayService.parse_work_orders(wo_data)
        data_cache.set_work_orders(work_orders, wo_data)
        
        logger.info(f"Data refreshed: {len(deals)} deals, {len(work_orders)} work orders")
        
        return {
            "status": "success",
            "deals_count": len(deals),
            "work_orders_count": len(work_orders),
            "cache_info": data_cache.get_cache_info()
        }
        
    except MondayAPIError as e:
        logger.error(f"Monday API error: {e}")
        raise HTTPException(status_code=502, detail=f"Failed to fetch data from Monday.com: {str(e)}")
    except Exception as e:
        logger.exception("Error refreshing data")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


async def _ensure_data_loaded():
    """Ensure data is loaded in cache."""
    deals = data_cache.get_deals()
    work_orders = data_cache.get_work_orders()
    
    if deals is None or work_orders is None:
        logger.info("Cache expired or empty, refreshing data")
        
        # Fetch deals
        deals_data = await monday_client.get_all_board_data(config.MONDAY_DEALS_BOARD_ID)
        deals = MondayService.parse_deals(deals_data)
        data_cache.set_deals(deals, deals_data)
        
        # Fetch work orders
        wo_data = await monday_client.get_all_board_data(config.MONDAY_WORK_ORDERS_BOARD_ID)
        work_orders = MondayService.parse_work_orders(wo_data)
        data_cache.set_work_orders(work_orders, wo_data)
    
    return deals, work_orders


@app.get("/api/data/deals")
async def get_deals():
    """Get deals data summary."""
    try:
        deals, _ = await _ensure_data_loaded()
        
        return {
            "total_deals": len(deals),
            "board_name": "Skylark — Deals",
            "sample": [
                {
                    "deal_name": d.deal_name,
                    "customer": d.customer,
                    "sector": d.sector,
                    "deal_value": d.deal_value,
                    "status": d.deal_status
                }
                for d in deals[:5]
            ]
        }
        
    except Exception as e:
        logger.exception("Error fetching deals")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data/work-orders")
async def get_work_orders():
    """Get work orders data summary."""
    try:
        _, work_orders = await _ensure_data_loaded()
        
        return {
            "total_work_orders": len(work_orders),
            "board_name": "Skylark — Work Orders",
            "sample": [
                {
                    "work_order_name": w.work_order_name,
                    "customer": w.customer,
                    "sector": w.sector,
                    "execution_status": w.execution_status,
                    "billed_value": w.billed_value
                }
                for w in work_orders[:5]
            ]
        }
        
    except Exception as e:
        logger.exception("Error fetching work orders")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data-quality")
async def get_data_quality():
    """Get data quality report."""
    try:
        deals, work_orders = await _ensure_data_loaded()
        
        deals_quality = DataQualityAnalyzer.analyze_deals(deals)
        wo_quality = DataQualityAnalyzer.analyze_work_orders(work_orders)
        
        return {
            "deals": deals_quality.dict(),
            "work_orders": wo_quality.dict()
        }
        
    except Exception as e:
        logger.exception("Error analyzing data quality")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for business intelligence queries."""
    try:
        logger.info(f"Chat request: {request.message}")
        
        # Ensure data is loaded
        deals, work_orders = await _ensure_data_loaded()
        
        # Handle query
        response = await agent_router.handle_query(
            request.message,
            deals,
            work_orders
        )
        
        return ChatResponse(**response)
        
    except MondayAPIError as e:
        logger.error(f"Monday API error: {e}")
        raise HTTPException(
            status_code=502,
            detail="I couldn't access the Monday.com data right now. Please check the Monday.com connection or try again."
        )
    except Exception as e:
        logger.exception("Error handling chat")
        raise HTTPException(
            status_code=500,
            detail=f"I encountered an error processing your question. Please try again or rephrase your question."
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Skylark Business Intelligence Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "refresh": "/api/refresh",
            "deals": "/api/data/deals",
            "work_orders": "/api/data/work-orders",
            "data_quality": "/api/data-quality"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration
    errors = config.validate()
    if errors:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        exit(1)
    
    logger.info("Starting Skylark BI Agent server")
    uvicorn.run(app, host="0.0.0.0", port=config.BACKEND_PORT)
