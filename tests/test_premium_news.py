#!/usr/bin/env python3
"""Test premium news sentiment functionality."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.functionSelector import FunctionSelector
from src.config import load_config
from src.binance_handler import BinanceHandler
from src.ai_factory import AIFactory

async def test_premium_news_sentiment():
    """Test premium news sentiment analysis."""
    config = load_config()
    
    # Initialize required dependencies
    binance = BinanceHandler(config)
    ai_handler = AIFactory.create_handler(config)
    
    function_selector = FunctionSelector(config, binance, ai_handler)
    
    print("🤖 Testing Premium News Sentiment Analysis...")
    print("=" * 60)
    
    # Test premium AI requests
    test_messages = [
        "Use OpenAI for news sentiment analysis",
        "news sentiment with Gemini analysis",
        "sentiment analysis using openai",
        "premium news analysis with gemini"
    ]
    
    for i, test_message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: '{test_message}'")
        print("-" * 50)
        
        try:
            result = await function_selector.process_user_request(test_message)
            print(f"✅ Response Type: {result['response_type']}")
            print(f"✅ Success: {result['success']}")
            
            if result['response_type'] == 'premium_news_sentiment':
                print("🎯 SUCCESS - Premium news sentiment detected!")
            elif result['response_type'] == 'news_sentiment':
                print("🎯 PARTIAL - Standard news sentiment (premium not detected)")
            else:
                print(f"❌ MISS - Got '{result['response_type']}'")
            
            print(f"📄 Message Preview: {result['message'][:200]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_premium_news_sentiment())
