"""
Ollama LLM integration module.
Handles communication with local Ollama instance for trade analysis.
"""

import json
import logging
from typing import Dict, Any, Optional
import aiohttp
import asyncio
from .config import Config
from .schemas import TradingAnalysis, IntentClassification
from .prompts import SYSTEM_PROMPT, get_market_analysis_prompt, get_intent_selector_prompt

logger = logging.getLogger(__name__)


class OllamaHandler:
    """Handles communication with Ollama LLM."""
    
    def __init__(self, config: Config):
        """Initialize Ollama handler with configuration."""
        self.config = config
        self.base_url = config.ollama_base_url
        self.model = config.ollama_model
    
    async def analyze_market_data(self, user_message: str, price_data: str) -> TradingAnalysis:
        """
        Send market data and user message to Ollama for analysis.
        
        Args:
            user_message: The user's message/question
            price_data: Formatted price data string
            
        Returns:
            TradingAnalysis object with LLM's response
        """
        prompt = self._build_analysis_prompt(user_message, price_data)
        
        try:
            response = await self._call_ollama(prompt)
            return self._parse_ollama_response(response)
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            # Return safe default response
            return TradingAnalysis(
                intention="nothing",
                analysis=f"Error occurred during analysis: {str(e)}",
                suggested_action="Unable to analyze market data at this time. Please try again later.",
                confidence=0.0,
                risk_level="high"
            )
    
    async def classify_user_intent(self, user_message: str) -> IntentClassification:
        """
        Classify user intent to determine which prompt/function to use.
        
        Args:
            user_message: The user's message to classify
            
        Returns:
            IntentClassification object with classified intent
        """
        prompt = get_intent_selector_prompt(user_message)
        
        try:
            response = await self._call_ollama(prompt)
            return self._parse_intent_response(response)
        except Exception as e:
            logger.error(f"Error in intent classification: {e}")
            # Return safe default response
            return IntentClassification(
                intent="error_recovery",
                confidence=0.0,
                reasoning=f"Error occurred during classification: {str(e)}",
                suggested_prompt_function="get_error_recovery_prompt",
                required_data=["error_info", "available_data"],
                user_query_type="consultation"
            )
    
    def _build_analysis_prompt(self, user_message: str, price_data: str) -> str:
        """Build the analysis prompt for Ollama using centralized prompts."""
        # Combine system prompt with specific market analysis prompt
        market_prompt = get_market_analysis_prompt(user_message, price_data)
        
        return f"{SYSTEM_PROMPT}\n\n{market_prompt}"
    
    async def _call_ollama(self, prompt: str) -> str:
        """Make HTTP request to Ollama API."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for more consistent JSON
                "top_p": 0.9,
                "max_tokens": 1000
            }
        }
        
        timeout = aiohttp.ClientTimeout(total=60)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Ollama API error: {response.status}")
                
                result = await response.json()
                return result.get("response", "")
    
    def _parse_ollama_response(self, response: str) -> TradingAnalysis:
        """Parse Ollama's JSON response into TradingAnalysis object."""
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
            logger.error(f"Failed to parse JSON response: {e}")
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
            logger.error(f"Error parsing Ollama response: {e}")
            
            return TradingAnalysis(
                intention="nothing",
                analysis=f"Error processing response: {str(e)}",
                suggested_action="Technical error occurred. Please try again.",
                confidence=0.0,
                risk_level="high"
            )
    
    def _parse_intent_response(self, response: str) -> IntentClassification:
        """Parse Ollama's JSON response into IntentClassification object."""
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
            intent_data = {
                "intent": data.get("intent", "error_recovery"),
                "confidence": min(max(data.get("confidence", 0.5), 0.0), 1.0),  # Clamp between 0-1
                "reasoning": data.get("reasoning", "Intent classification completed"),
                "suggested_prompt_function": data.get("suggested_prompt_function", "get_error_recovery_prompt"),
                "required_data": data.get("required_data", []),
                "user_query_type": data.get("user_query_type", "consultation")
            }
            
            # Validate intent against allowed values
            valid_intents = [
                "btc_price_info", "usdt_balance_info", "portfolio_value", 
                "market_analysis", "risk_assessment", "trading_decision", 
                "volatile_market", "portfolio_analysis", "general_consult", "error_recovery"
            ]
            
            if intent_data["intent"] not in valid_intents:
                intent_data["intent"] = "error_recovery"
                intent_data["reasoning"] = f"Unknown intent detected: {data.get('intent')}"
            
            return IntentClassification(**intent_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in intent classification: {e}")
            logger.error(f"Raw response: {response}")
            
            return IntentClassification(
                intent="error_recovery",
                confidence=0.0,
                reasoning=f"JSON parsing error: {str(e)}",
                suggested_prompt_function="get_error_recovery_prompt",
                required_data=["error_info", "available_data"],
                user_query_type="consultation"
            )
        except Exception as e:
            logger.error(f"Error parsing intent response: {e}")
            
            return IntentClassification(
                intent="error_recovery",
                confidence=0.0,
                reasoning=f"Intent parsing error: {str(e)}",
                suggested_prompt_function="get_error_recovery_prompt",
                required_data=["error_info", "available_data"],
                user_query_type="consultation"
            )
    
    async def health_check(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            url = f"{self.base_url}/api/tags"
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False


async def main():
    """Test Ollama connection."""
    print("🔍 Testing Ollama Connection")
    print("=" * 40)
    
    try:
        # Import config here to avoid circular imports
        from .config import load_config
        
        # Load configuration
        config = load_config()
        print(f"✅ Configuration loaded")
        print(f"🤖 Ollama Model: {config.ollama_model}")
        print(f"🔗 Base URL: {config.ollama_base_url}")
        
        # Create Ollama handler
        handler = OllamaHandler(config)
        print("✅ Ollama handler created")
        
        # Test health check
        print("🔄 Testing connection...")
        is_healthy = await handler.health_check()
        
        if is_healthy:
            print("✅ Ollama connection successful!")
            
            # Test intent classification
            print("\n🧪 Testing intent classification...")
            test_message = "What's the current BTC price?"
            
            intent_result = await handler.classify_user_intent(test_message)
            print(f"✅ Intent classification completed!")
            print(f"🎯 Intent: {intent_result.intent}")
            print(f"🎯 Confidence: {intent_result.confidence}")
            print(f"💭 Reasoning: {intent_result.reasoning[:80]}...")
            
            # Test market analysis
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
            print("❌ Ollama connection failed!")
            print("💡 Make sure Ollama is running: ollama serve")
            
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
