#!/usr/bin/env python3
"""Test premium AI comparison functionality."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.functionSelector import FunctionSelector
from src.config import load_config
from src.binance_handler import BinanceHandler
from src.ai_factory import AIFactory

async def test_premium_ai():
    """Test premium AI comparison."""
    config = load_config()
    
    # Initialize required dependencies
    binance = BinanceHandler(config)
    ai_handler = AIFactory.create_handler(config)
    
    function_selector = FunctionSelector(config, binance, ai_handler)
    
    print("🧪 Testing Premium AI Comparison...")
    print("=" * 50)
    
    # Test message that requests OpenAI analysis for trading
    test_message = "Analyze BTC and recommend what to do. Use OpenAI analysis please."
    
    try:
        # First let's test intent classification to see if premium AI is detected
        print(f"🔍 Testing intent classification for: '{test_message}'")
        intent = await ai_handler.classify_user_intent(test_message)
        print(f"🎯 Detected Intent: {intent.intent}")
        print(f"🧠 Premium AI Requested: {intent.premium_ai_requested}")
        print(f"🤖 Requested Provider: {intent.requested_ai_provider}")
        print(f"🔍 Comparison Analysis: {intent.comparison_analysis}")
        print()
        
        result = await function_selector.process_user_request(test_message)
        
        print(f"✅ Response Type: {result['response_type']}")
        print(f"✅ Success: {result['success']}")
        
        # Show different output based on response type
        if result['response_type'].startswith('premium_'):
            print("🎉 PREMIUM AI COMPARISON SUCCESSFUL!")
            print(f"✅ Message:\n{result['message']}")
            
            if 'comparison_result' in result:
                print(f"\n🔍 Comparison Result: {result['comparison_result']}")
                print(f"💰 Cost Estimate: {result.get('cost_estimate', 'N/A')}")
            
            if 'premium_provider' in result:
                print(f"🧠 Premium Provider: {result['premium_provider']}")
        else:
            print("⚠️ Standard analysis returned (premium AI might have failed)")
            print(f"✅ Message:\n{result['message']}")
            
        print(f"\n📋 All Response Keys: {list(result.keys())}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_premium_ai())
