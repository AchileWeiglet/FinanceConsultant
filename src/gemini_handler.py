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
            # Clean the response - remove markdown code blocks and extra content
            response = response.strip()
            
            # Remove markdown code block markers
            if response.startswith('```json'):
                response = response[7:]  # Remove ```json
            if response.startswith('```'):
                response = response[3:]   # Remove ```
            if response.endswith('```'):
                response = response[:-3]  # Remove trailing ```
            
            response = response.strip()
            
            # Find JSON content between braces
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No valid JSON found in response")
            
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            # Extract analysis text - handle both string and nested object formats
            analysis_text = data.get("analysis", "Analysis unavailable")
            if isinstance(analysis_text, dict):
                # Convert nested analysis to readable text
                analysis_parts = []
                for key, value in analysis_text.items():
                    if isinstance(value, str):
                        clean_key = key.replace('_', ' ').replace('price', 'Price').replace('trend', 'Trend')
                        analysis_parts.append(f"{clean_key}: {value}")
                analysis_text = ". ".join(analysis_parts)
            
            # Ensure analysis is a string
            if not isinstance(analysis_text, str):
                analysis_text = str(analysis_text)
            
            # Validate and normalize the intention
            intention = str(data.get("intention", "nothing")).lower()
            if intention not in ["buy", "sell", "consult", "nothing"]:
                intention = "nothing"
            
            # Validate and normalize risk_level
            risk_level = str(data.get("risk_level", "medium")).lower()
            if risk_level not in ["low", "medium", "high"]:
                risk_level = "medium"
            
            # Create the analysis data with proper types
            analysis_data = {
                "intention": intention,
                "analysis": analysis_text,
                "suggested_action": str(data.get("suggested_action", "No action recommended")),
                "endpoint": data.get("endpoint"),  # Can be None
                "amount": min(max(float(data.get("amount", 0.001)), 0.001), 0.01),
                "confidence": min(max(float(data.get("confidence", 0.5)), 0.0), 1.0),
                "risk_level": risk_level
            }
            
            return TradingAnalysis(**analysis_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {e}")
            # Don't log the full response for security - it might contain sensitive data
            
            # Return safe fallback that matches expected format
            return TradingAnalysis(
                intention="nothing",
                analysis="Failed to parse analysis response",
                suggested_action="Unable to process market analysis. Please try again.",
                endpoint=None,
                amount=0.001,
                confidence=0.0,
                risk_level="high"
            )
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            
            return TradingAnalysis(
                intention="nothing",
                analysis="Error processing response. Please try again.",
                suggested_action="Technical error occurred. Please try again.",
                endpoint=None,
                amount=0.001,
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


async def main():
    """Test Gemini connection."""
    print("🔍 Testing Google Gemini Connection")
    print("=" * 40)
    
    try:
        # Import config here to avoid circular imports
        from .config import load_config
        
        # Load configuration
        config = load_config()
        print(f"✅ Configuration loaded")
        print(f"🤖 Gemini Model: {config.gemini_model}")
        print(f"🔑 API Key: {'✅ Configured' if config.gemini_api_key else '❌ Not found'}")
        
        if not config.gemini_api_key:
            print("❌ Gemini API key not found in configuration")
            return
        
        # Create Gemini handler
        handler = GeminiHandler(config)
        print("✅ Gemini handler created")
        
        # Test health check
        print("🔄 Testing connection...")
        is_healthy = await handler.health_check()
        
        if is_healthy:
            print("✅ Gemini connection successful!")
            
            # Test a simple analysis
            print("\n🧪 Testing market analysis...")
            test_message = "What's the current market sentiment?"
            test_price_data = "BTC Price: $45,000 (24h change: +2.5%)"
            
            result = await handler.analyze_market_data(test_message, test_price_data)
            print(f"✅ Analysis completed!")
            print(f"📊 Intention: {result.intention}")
            print(f"📈 Analysis: {result.analysis[:100]}...")
            print(f"🎯 Confidence: {result.confidence}")
            print(f"⚠️  Risk Level: {result.risk_level}")
            
        else:
            print("❌ Gemini connection failed!")
            
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
