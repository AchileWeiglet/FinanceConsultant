#!/usr/bin/env python3
"""Test intent classification directly."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.ai_factory import AIFactory
from src.config import load_config

async def test_intent_classification():
    """Test intent classification for news sentiment."""
    config = load_config()
    ai_handler = AIFactory.create_handler(config)
    
    print("🎯 Testing Intent Classification for News Sentiment...")
    print("=" * 60)
    
    # Very specific news sentiment test messages
    test_messages = [
        "crypto news analysis",
        "news sentiment on Bitcoin",
        "latest news affecting BTC price",
        "social media sentiment",
        "news impact analysis",
        "sentiment analysis crypto",
        "What's the news sentiment?",
        "Check crypto news mood",
        "news affecting market"
    ]
    
    for i, test_message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: '{test_message}'")
        print("-" * 50)
        
        try:
            intent_result = await ai_handler.classify_user_intent(test_message)
            print(f"🎯 Intent: {intent_result.intent}")
            print(f"📊 Confidence: {intent_result.confidence}")
            print(f"💭 Reasoning: {intent_result.reasoning}")
            print(f"🔧 Function: {intent_result.suggested_prompt_function}")
            print(f"📋 Data Needed: {intent_result.required_data}")
            
            if intent_result.intent == "news_sentiment":
                print("✅ CORRECT - News sentiment detected!")
            else:
                print(f"❌ INCORRECT - Expected 'news_sentiment', got '{intent_result.intent}'")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_intent_classification())
