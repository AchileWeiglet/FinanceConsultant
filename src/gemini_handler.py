"""
Google Gemini LLM integration module.
Handles communication with Google Gemini API for trade analysis.
"""

import json
import logging
from typing import Dict, Any, Optional
import asyncio
import google.generativeai as genai
from .config import Config
from .schemas import TradingAnalysis
from .prompts import SYSTEM_PROMPT, get_market_analysis_prompt

logger = logging.getLogger(__name__)


class GeminiHandler:
    """Handles communication with Google Gemini API."""
    
    def __init__(self, config: Config):
        """Initialize Gemini handler with configuration."""
        self.config = config
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
    
    async def analyze_market_data(self, user_message: str, price_data: str) -> TradingAnalysis:
        """
        Send market data and user message to Gemini for analysis.
        
        Args:
            user_message: The user's message/question
            price_data: Formatted price data string
            
        Returns:
            TradingAnalysis object with LLM's response
        """
        prompt = self._build_analysis_prompt(user_message, price_data)
        
        try:
            response = await self._call_gemini(prompt)
            return self._parse_gemini_response(response)
        except Exception as e:
            logger.error(f"Error in Gemini market analysis: {e}")
            # Return safe default response
            return TradingAnalysis(
                intention="nothing",
                analysis=f"Error occurred during analysis: {str(e)}",
                suggested_action="Unable to analyze market data at this time. Please try again later.",
                confidence=0.0,
                risk_level="high"
            )
    
    def _build_analysis_prompt(self, user_message: str, price_data: str) -> str:
        """Build the analysis prompt for Gemini using centralized prompts."""
        # Use centralized prompt system
        return get_market_analysis_prompt(user_message, price_data)
    
    async def _call_gemini(self, prompt: str) -> str:
        """Make API request to Gemini."""
        try:
            # Run in thread pool since Gemini client is not async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3,
                        max_output_tokens=1000,
                    )
                )
            )
            
            return response.text or ""
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise
    
    def _parse_gemini_response(self, response: str) -> TradingAnalysis:
        """Parse Gemini's JSON response into TradingAnalysis object."""
        try:
            # Clean the response - remove any non-JSON content
            response = response.strip()
            
            # Find JSON content between braces
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No valid JSON found in response")
            
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
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
            logger.error(f"Failed to parse Gemini JSON response: {e}")
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
            logger.error(f"Error parsing Gemini response: {e}")
            
            return TradingAnalysis(
                intention="nothing",
                analysis=f"Error processing response: {str(e)}",
                suggested_action="Technical error occurred. Please try again.",
                confidence=0.0,
                risk_level="high"
            )
    
    async def health_check(self) -> bool:
        """Check if Gemini API is accessible."""
        try:
            # Simple test call to check API connectivity
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content("Hello", 
                    generation_config=genai.types.GenerationConfig(max_output_tokens=1))
            )
            return True
                    
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False
