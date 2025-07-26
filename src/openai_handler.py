"""
OpenAI LLM integration module.
Handles communication with OpenAI API for trade analysis.
"""

import json
import logging
from typing import Dict, Any, Optional
import asyncio
from openai import AsyncOpenAI
from .config import Config
from .schemas import TradingAnalysis
from .prompts import SYSTEM_PROMPT, get_market_analysis_prompt

logger = logging.getLogger(__name__)


class OpenAIHandler:
    """Handles communication with OpenAI API."""
    
    def __init__(self, config: Config):
        """Initialize OpenAI handler with configuration."""
        self.config = config
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.model = config.openai_model
    
    async def analyze_market_data(self, user_message: str, price_data: str) -> TradingAnalysis:
        """
        Send market data and user message to OpenAI for analysis.
        
        Args:
            user_message: The user's message/question
            price_data: Formatted price data string
            
        Returns:
            TradingAnalysis object with LLM's response
        """
        prompt = self._build_analysis_prompt(user_message, price_data)
        
        try:
            response = await self._call_openai(prompt)
            return self._parse_openai_response(response)
        except Exception as e:
            logger.error(f"Error in OpenAI market analysis: {e}")
            # Return safe default response
            return TradingAnalysis(
                intention="nothing",
                analysis=f"Error occurred during analysis: {str(e)}",
                suggested_action="Unable to analyze market data at this time. Please try again later.",
                confidence=0.0,
                risk_level="high"
            )
    
    def _build_analysis_prompt(self, user_message: str, price_data: str) -> str:
        """Build the analysis prompt for OpenAI using centralized prompts."""
        # Use centralized prompt system
        return get_market_analysis_prompt(user_message, price_data)
    
    async def _call_openai(self, prompt: str) -> str:
        """Make API request to OpenAI."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cryptocurrency trading analysis assistant. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent JSON
                max_tokens=1000,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _parse_openai_response(self, response: str) -> TradingAnalysis:
        """Parse OpenAI's JSON response into TradingAnalysis object."""
        try:
            data = json.loads(response)
            
            # Validate required fields and set defaults
            analysis_data = {
                "intention": data.get("intention", "nothing"),
                "analysis": data.get("analysis", "Analysis unavailable"),
                "suggested_action": data.get("suggested_action", "No action recommended"),
                "endpoint": data.get("endpoint"),
                "amount": min(max(data.get("amount", 0.001), 0.001), 0.01),  # Clamp between 0.001-0.01
                "confidence": min(max(data.get("confidence", 0.5), 0.0), 1.0),  # Clamp between 0-1
                "risk_level": data.get("risk_level", "medium")
            }
            
            # Validate intention
            if analysis_data["intention"] not in ["buy", "sell", "consult", "nothing"]:
                analysis_data["intention"] = "nothing"
            
            # Validate risk_level
            if analysis_data["risk_level"] not in ["low", "medium", "high"]:
                analysis_data["risk_level"] = "medium"
            
            return TradingAnalysis(**analysis_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI JSON response: {e}")
            logger.error(f"Raw response: {response}")
            
            # Return safe fallback
            return TradingAnalysis(
                intention="nothing",
                analysis="Failed to parse analysis response",
                suggested_action="Unable to process market analysis. Please try again.",
                confidence=0.0,
                risk_level="high"
            )
        except Exception as e:
            logger.error(f"Error parsing OpenAI response: {e}")
            
            return TradingAnalysis(
                intention="nothing",
                analysis=f"Error processing response: {str(e)}",
                suggested_action="Technical error occurred. Please try again.",
                confidence=0.0,
                risk_level="high"
            )
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible."""
        try:
            # Simple test call to check API connectivity
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1
            )
            return True
                    
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
