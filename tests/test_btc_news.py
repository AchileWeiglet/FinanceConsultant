#!/usr/bin/env python3
"""Test BTC news intent classification."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.functionSelector import FunctionSelector
from src.config import load_config
from src.binance_handler import BinanceHandler
from src.ai_factory import AIFactory

async def test_btc_news():
    """Test BTC news request classification."""
    config = load_config()
    
    # Initialize required dependencies
    binance = BinanceHandler(config)
    ai_handler = AIFactory.create_handler(config)
    
    function_selector = FunctionSelector(config, binance, ai_handler)
    
    print("📰 Testing 'tell me about the news of btc'")
    print("=" * 50)
    
    test_message = "tell me about the news of btc"
    
    try:
        # Test intent classification first
        print("🔍 Step 1: Intent Classification")
        intent = await ai_handler.classify_user_intent(test_message)
        print(f"🎯 Intent: {intent.intent}")
        print(f"📊 Confidence: {intent.confidence}")
        print(f"🤖 Premium AI: {intent.premium_ai_requested}")
        print(f"🧠 AI Provider: {intent.requested_ai_provider}")
        print(f"💭 Reasoning: {intent.reasoning}")
        
        print("\n🔄 Step 2: Processing Request")
        # Process through function selector
        result = await function_selector.process_user_request(test_message)
        
        print(f"✅ Response Type: {result['response_type']}")
        print(f"✅ Success: {result['success']}")
        print(f"📄 Message Preview: {result['message'][:300]}...")
        
        # Check if Gemini was involved
        if 'Gemini' in result.get('message', ''):
            print("\n⚠️  GEMINI DETECTED in response!")
        
        if result['response_type'] == 'premium_news_sentiment':
            print("\n⚠️  PREMIUM AI was triggered!")
        elif result['response_type'] == 'premium_market_analysis':
            print("\n⚠️  PREMIUM MARKET ANALYSIS was triggered!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_btc_news())
