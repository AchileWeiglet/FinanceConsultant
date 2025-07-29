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
            # Check if model supports json_object response format
            supports_json_format = self.model in ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo-1106", "gpt-4-turbo"]
            
            request_params = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a cryptocurrency trading analysis assistant. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,  # Lower temperature for more consistent JSON
                "max_tokens": 1000,
            }
            
            # Only add response_format for supported models
            if supports_json_format:
                request_params["response_format"] = {"type": "json_object"}
            
            response = await self.client.chat.completions.create(**request_params)
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _parse_openai_response(self, response: str) -> TradingAnalysis:
        """Parse OpenAI's JSON response into TradingAnalysis object."""
        try:
            data = json.loads(response)
            
            # Validate required fields and set defaults
            analysis_field = data.get("analysis", "Analysis unavailable")
            
            # Handle case where analysis is an object instead of string
            if isinstance(analysis_field, dict):
                # Convert object to readable string
                analysis_text = []
                for key, value in analysis_field.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            analysis_text.append(f"{subkey}: {subvalue}")
                    else:
                        analysis_text.append(f"{key}: {value}")
                analysis_field = "; ".join(analysis_text)
            elif not isinstance(analysis_field, str):
                analysis_field = str(analysis_field)
            
            analysis_data = {
                "intention": data.get("intention", "nothing"),
                "analysis": analysis_field,
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


async def main():
    """Test OpenAI connection."""
    print("🔍 Testing OpenAI Connection")
    print("=" * 40)
    
    try:
        # Import config here to avoid circular imports
        from .config import load_config
        
        # Load configuration
        config = load_config()
        print(f"✅ Configuration loaded")
        print(f"🤖 OpenAI Model: {config.openai_model}")
        print(f"🔑 API Key: {config.openai_api_key[:10]}..." if config.openai_api_key else "❌ No API key")
        
        if not config.openai_api_key:
            print("❌ OpenAI API key not found in configuration")
            return
        
        # Create OpenAI handler
        handler = OpenAIHandler(config)
        print("✅ OpenAI handler created")
        
        # Test health check
        print("🔄 Testing connection...")
        is_healthy = await handler.health_check()
        
        if is_healthy:
            print("✅ OpenAI connection successful!")
            
            # Test a simple analysis
            print("\n🧪 Testing market analysis...")
            test_message = "What's the current market sentiment?"
            test_price_data = "BTC Price: $45,000 (24h change: +2.5%)"
            
            result = await handler.analyze_market_data(test_message, test_price_data)
            print(f"✅ Analysis completed!")
            print(f"📊 Intention: {result.intention}")
            print(f"📈 Analysis: {result.analysis[:100]}...")
            print(f"🎯 Confidence: {result.confidence}")
            
        else:
            print("❌ OpenAI connection failed!")
            
    except Exception as e:
        print(f"❌ Error testing OpenAI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
