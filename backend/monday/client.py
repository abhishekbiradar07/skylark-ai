"""Monday.com GraphQL API client."""
import logging
from typing import Any, Dict, List, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import config
from monday.queries import BOARD_METADATA_QUERY, SIMPLE_BOARD_QUERY

logger = logging.getLogger(__name__)


class MondayAPIError(Exception):
    """Monday.com API error."""
    pass


class MondayClient:
    """Monday.com GraphQL API client (READ ONLY)."""
    
    def __init__(self, api_token: Optional[str] = None):
        """Initialize Monday client.
        
        Args:
            api_token: Monday.com API token. If not provided, uses config.
        """
        self.api_token = api_token or config.MONDAY_API_TOKEN
        self.api_url = config.MONDAY_API_URL
        
        if not self.api_token:
            raise ValueError("Monday API token is required")
        
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "API-Version": "2023-10"
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        reraise=True
    )
    async def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL query with retry logic.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Query response data
            
        Raises:
            MondayAPIError: If API request fails
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload
                )
                
                response.raise_for_status()
                data = response.json()
                
                if "errors" in data:
                    error_msg = data["errors"][0].get("message", "Unknown error")
                    logger.error(f"Monday GraphQL error: {error_msg}")
                    raise MondayAPIError(f"Monday API error: {error_msg}")
                
                if "data" not in data:
                    raise MondayAPIError("Invalid API response: missing data field")
                
                return data["data"]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise MondayAPIError("Invalid or expired Monday.com API token")
            elif e.response.status_code == 403:
                raise MondayAPIError("Permission denied accessing Monday.com board")
            elif e.response.status_code == 429:
                raise MondayAPIError("Rate limit exceeded")
            else:
                raise MondayAPIError(f"HTTP error: {e.response.status_code}")
        except httpx.TimeoutException:
            raise MondayAPIError("Request timeout connecting to Monday.com")
        except httpx.NetworkError:
            raise MondayAPIError("Network error connecting to Monday.com")
        except Exception as e:
            logger.exception("Unexpected error in Monday API call")
            raise MondayAPIError(f"Unexpected error: {str(e)}")
    
    async def get_board_metadata(self, board_id: str) -> Dict[str, Any]:
        """Get board metadata including columns.
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            Board metadata with columns
        """
        logger.info(f"Fetching metadata for board {board_id}")
        
        data = await self._execute_query(
            BOARD_METADATA_QUERY,
            {"boardId": int(board_id)}
        )
        
        if not data.get("boards") or len(data["boards"]) == 0:
            raise MondayAPIError(f"Board {board_id} not found")
        
        board = data["boards"][0]
        logger.info(f"Found board: {board.get('name')}")
        
        return board
    
    async def get_board_items(self, board_id: str) -> List[Dict[str, Any]]:
        """Get all items from a board.
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of board items with column values
        """
        logger.info(f"Fetching items from board {board_id}")
        
        data = await self._execute_query(
            SIMPLE_BOARD_QUERY,
            {"boardId": int(board_id)}
        )
        
        if not data.get("boards") or len(data["boards"]) == 0:
            raise MondayAPIError(f"Board {board_id} not found")
        
        board = data["boards"][0]
        items_page = board.get("items_page", {})
        items = items_page.get("items", [])
        
        logger.info(f"Retrieved {len(items)} items from board {board.get('name')}")
        
        return items
    
    async def get_all_board_data(self, board_id: str) -> Dict[str, Any]:
        """Get complete board data including metadata and items.
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            Dictionary with board metadata and items
        """
        logger.info(f"Fetching complete data for board {board_id}")
        
        metadata = await self.get_board_metadata(board_id)
        items = await self.get_board_items(board_id)
        
        return {
            "board_id": board_id,
            "board_name": metadata.get("name"),
            "description": metadata.get("description"),
            "columns": metadata.get("columns", []),
            "items": items,
            "item_count": len(items)
        }
