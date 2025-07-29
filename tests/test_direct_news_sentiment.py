#!/usr/bin/env python3
"""Direct test news sentiment with the exact function."""

import asyncio
import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.functionSelector import FunctionSelector
from src.config import load_config
from src.binance_handler import BinanceHandler
from src.ai_factory import AIFactory

async def test_news_sentiment_directly():
    """Test news sentiment handler directly."""
    config = load_config()
    
    # Initialize required dependencies
    binance = BinanceHandler(config)
    ai_handler = AIFactory.create_handler(config)
    
    function_selector = FunctionSelector(config, binance, ai_handler)
    
    print("📰 Testing News Sentiment Handler Directly...")
    print("=" * 50)
    
    # Test direct handler call
    try:
        print("🧪 Testing _handle_news_sentiment directly...")
        
        # Mock intent object
        class MockIntent:
            premium_ai_requested = False
            requested_ai_provider = "none"
        
        result = await function_selector._handle_news_sentiment("Check crypto news sentiment", MockIntent())
        
        print("✅ Handler Result:")
        print(f"Response Type: {result['response_type']}")
        print(f"Success: {result['success']}")
        print(f"Message Preview: {result['message'][:300]}...")
        
        print("\n🧪 Testing with premium AI...")
        
        # Test with premium AI
        mock_premium_intent = MockIntent()
        mock_premium_intent.premium_ai_requested = True
        mock_premium_intent.requested_ai_provider = "openai"
        
        result_premium = await function_selector._handle_news_sentiment("Use OpenAI for news sentiment", mock_premium_intent)
        
        print("✅ Premium Handler Result:")
        print(f"Response Type: {result_premium['response_type']}")
        print(f"Success: {result_premium['success']}")
        print(f"Message Preview: {result_premium['message'][:300]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_news_sentiment_directly())
