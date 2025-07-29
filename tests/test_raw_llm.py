#!/usr/bin/env python3
"""Test specific news sentiment trigger that should work."""

import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.ai_factory import AIFactory
from src.config import load_config

async def test_raw_llm():
    """Test the raw LLM to see what's happening."""
    config = load_config()
    ai_handler = AIFactory.create_handler(config)
    
    # Test messages that should clearly be news sentiment
    test_message = "crypto news sentiment analysis please"
    
    print(f"🧪 Testing message: '{test_message}'")
    print("=" * 50)
    
    try:
        intent = await ai_handler.classify_user_intent(test_message)
        
        print(f"🎯 Intent: {intent.intent}")
        print(f"📊 Confidence: {intent.confidence}")
        print(f"💭 Reasoning: {intent.reasoning}")
        print(f"🔧 Function: {intent.suggested_prompt_function}")
        print(f"📋 Data Needed: {intent.required_data}")
        print(f"🎭 Query Type: {intent.user_query_type}")
        print(f"🧠 Premium AI: {intent.premium_ai_requested}")
        print(f"🤖 Provider: {intent.requested_ai_provider}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_raw_llm())
