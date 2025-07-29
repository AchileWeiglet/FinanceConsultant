#!/usr/bin/env python3
"""Test news sentiment functionality."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.functionSelector import FunctionSelector
from src.config import load_config
from src.binance_handler import BinanceHandler
from src.ai_factory import AIFactory

async def test_news_sentiment():
    """Test news sentiment analysis."""
    config = load_config()
    
    # Initialize required dependencies
    binance = BinanceHandler(config)
    ai_handler = AIFactory.create_handler(config)
    
    function_selector = FunctionSelector(config, binance, ai_handler)
    
    print("📰 Testing News Sentiment Analysis...")
    print("=" * 50)
    
    # Test messages for news sentiment
    test_messages = [
        "Latest crypto news",
        "What news is affecting Bitcoin price?",
        "Social media sentiment analysis",
        "Use OpenAI for news sentiment analysis",
        "Market news impact on BTC",
        "Crypto news analysis today"
    ]
    
    for i, test_message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: '{test_message}'")
        print("-" * 40)
        
        try:
            # Test intent classification
            intent = await ai_handler.classify_user_intent(test_message)
            print(f"🎯 Detected Intent: {intent.intent}")
            print(f"🧠 Premium AI: {intent.premium_ai_requested}")
            print(f"🤖 Provider: {intent.requested_ai_provider}")
            
            # Process request
            result = await function_selector.process_user_request(test_message)
            print(f"✅ Response Type: {result['response_type']}")
            print(f"✅ Success: {result['success']}")
            print(f"📄 Message Preview: {result['message'][:200]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_news_sentiment())
