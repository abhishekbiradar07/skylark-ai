"""LLM reasoning and response generation."""
import json
import logging
from typing import Dict, Any, Optional
import httpx
from config import config
from agent.prompts import (
    SYSTEM_PROMPT,
    INTENT_CLASSIFICATION_PROMPT,
    RESPONSE_GENERATION_PROMPT,
    LEADERSHIP_UPDATE_PROMPT
)

logger = logging.getLogger(__name__)


class GroqProvider:
    """Groq LLM provider - FAST inference."""
    
    def __init__(self, api_key: str):
        """Initialize Groq provider.
        
        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "openai/gpt-oss-120b"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using Groq API."""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    error_detail = response.text
                    logger.error(f"Groq API error response: {error_detail}")
                
                response.raise_for_status()
                result = response.json()
                
                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise RuntimeError(f"LLM generation failed: {str(e)}")


def get_llm_provider() -> GroqProvider:
    """Get configured Groq LLM provider.
    
    Returns:
        Groq provider instance
        
    Raises:
        ValueError: If Groq API key is not configured
    """
    if not config.GROQ_API_KEY:
        raise ValueError("Groq API key not configured")
    return GroqProvider(config.GROQ_API_KEY)


class AgentReasoning:
    """Agent reasoning using LLM."""
    
    def __init__(self, llm_provider: Optional[GroqProvider] = None):
        """Initialize agent reasoning.
        
        Args:
            llm_provider: Groq LLM provider (uses default if not provided)
        """
        self.llm = llm_provider or get_llm_provider()
    
    async def classify_intent(self, question: str) -> Dict[str, Any]:
        """Classify user question intent.
        
        Args:
            question: User question
            
        Returns:
            Intent classification
        """
        prompt = INTENT_CLASSIFICATION_PROMPT.format(question=question)
        
        try:
            response = await self.llm.generate(
                "You are an intent classification system. Respond only with valid JSON.",
                prompt
            )
            
            # Parse JSON response
            # Extract JSON from markdown if needed
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            intent_data = json.loads(response.strip())
            return intent_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse intent JSON: {e}")
            # Default fallback
            return {
                "intent": "PIPELINE_SUMMARY",
                "sector_filter": None,
                "owner_filter": None,
                "time_period": None,
                "requires_clarification": False,
                "clarification_question": None
            }
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return {
                "intent": "PIPELINE_SUMMARY",
                "sector_filter": None,
                "owner_filter": None,
                "time_period": None,
                "requires_clarification": False,
                "clarification_question": None
            }
    
    async def generate_response(
        self,
        question: str,
        intent: str,
        metrics: Dict[str, Any],
        data_quality: list[str],
        data_sources: list[str]
    ) -> str:
        """Generate business intelligence response.
        
        Args:
            question: User question
            intent: Classified intent
            metrics: Calculated metrics
            data_quality: Data quality issues
            data_sources: Data sources used
            
        Returns:
            Generated response
        """
        metrics_str = json.dumps(metrics, indent=2, default=str)
        data_quality_str = "\n".join(data_quality) if data_quality else "No significant data quality issues for this query"
        data_sources_str = ", ".join(data_sources)
        
        prompt = RESPONSE_GENERATION_PROMPT.format(
            question=question,
            intent=intent,
            metrics=metrics_str,
            data_quality=data_quality_str,
            data_sources=data_sources_str
        )
        
        response = await self.llm.generate(SYSTEM_PROMPT, prompt)
        return response
    
    async def generate_leadership_update(self, metrics: Dict[str, Any]) -> str:
        """Generate comprehensive leadership update.
        
        Args:
            metrics: All business metrics
            
        Returns:
            Leadership update
        """
        metrics_str = json.dumps(metrics, indent=2, default=str)
        prompt = LEADERSHIP_UPDATE_PROMPT.format(metrics=metrics_str)
        
        response = await self.llm.generate(SYSTEM_PROMPT, prompt)
        return response
