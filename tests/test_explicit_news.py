#!/usr/bin/env python3
"""Test with very explicit news sentiment requests."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.functionSelector import FunctionSelector
from src.config import load_config
from src.binance_handler import BinanceHandler
from src.ai_factory import AIFactory

async def test_explicit_news_sentiment():
    """Test news sentiment with very explicit keywords."""
    config = load_config()
    
    # Initialize required dependencies  
    binance = BinanceHandler(config)
    ai_handler = AIFactory.create_handler(config)
    
    function_selector = FunctionSelector(config, binance, ai_handler)
    
    print("📰 Testing Explicit News Sentiment Requests...")
    print("=" * 60)
    
    # Very explicit news sentiment test messages
    test_messages = [
        "news sentiment",
        "sentiment analysis",
        "crypto news mood",
        "social media sentiment analysis",
        "show me news sentiment analysis",
        "analyze news sentiment",
        "news_sentiment analysis"
    ]
    
    for i, test_message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: '{test_message}'")
        print("-" * 40)
        
        try:
            result = await function_selector.process_user_request(test_message)
            print(f"✅ Response Type: {result['response_type']}")
            print(f"✅ Success: {result['success']}")
            
            if result['response_type'] in ['news_sentiment', 'premium_news_sentiment']:
                print("🎯 SUCCESS - News sentiment detected!")
            else:
                print(f"❌ MISS - Got '{result['response_type']}' instead of news_sentiment")
            
            print(f"📄 Message Preview: {result['message'][:150]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_explicit_news_sentiment())
