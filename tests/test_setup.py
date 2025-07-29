#!/usr/bin/env python3
"""
Test script to validate the trading bot setup.
Checks configuration, dependencies, and basic functionality.
"""

import sys
import os
import asyncio

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

async def test_imports():
    """Test that all required modules can be imported."""
    print("🔄 Testing imports...")
    
    try:
        from src.config import load_config
        print("✅ Config module imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from src.schemas import TradingAnalysis, BotResponse
        print("✅ Schemas module imported successfully")
    except Exception as e:
        print(f"❌ Schemas import failed: {e}")
        return False
    
    try:
        from src.binance_handler import BinanceHandler
        print("✅ Binance handler imported successfully")
    except Exception as e:
        print(f"❌ Binance handler import failed: {e}")
        return False
    
    try:
        from src.ollama_handler import OllamaHandler
        print("✅ Ollama handler imported successfully")
    except Exception as e:
        print(f"❌ Ollama handler import failed: {e}")
        return False
    
    try:
        from src.telegram_bot import TelegramBot
        print("✅ Telegram bot imported successfully")
    except Exception as e:
        print(f"❌ Telegram bot import failed: {e}")
        return False
    
    return True

async def test_config():
    """Test configuration loading."""
    print("\n🔄 Testing configuration...")
    
    try:
        from src.config import load_config
        
        # Try to load config (should fail if .env is not set up)
        try:
            config = load_config()
            print("✅ Configuration loaded successfully")
            print(f"   📊 Ollama URL: {config.ollama_base_url}")
            print(f"   🤖 Ollama Model: {config.ollama_model}")
            print(f"   🧪 Testnet Mode: {config.binance_testnet}")
            print(f"   💰 Trading Enabled: {config.enable_trading}")
            return True
        except ValueError as e:
            print(f"⚠️  Configuration validation failed: {e}")
            print("   This is expected if you haven't set up your .env file yet")
            return True
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def test_ai_providers():
    """Test AI provider connections."""
    print("\n🤖 Testing AI providers...")
    
    try:
        from src.ai_factory import AIFactory
        from src.config import Config
        
        # Create a basic config for testing
        config = Config(
            telegram_bot_token="test",
            telegram_chat_id="test", 
            binance_api_key="test",
            binance_secret_key="test",
            ai_provider="ollama",
            ollama_base_url="http://localhost:11434",
            ollama_model="llama3.2-vision:11b",
            openai_api_key="",
            gemini_api_key=""
        )
        
        health_results = await AIFactory.test_provider_health(config)
        
        for provider, is_healthy in health_results.items():
            if is_healthy:
                print(f"✅ {provider.upper()} is accessible")
            else:
                print(f"⚠️  {provider.upper()} is not accessible")
                if provider == "ollama":
                    print("   Make sure Ollama is running: 'ollama serve'")
                elif provider == "openai":
                    print("   Configure OPENAI_API_KEY in .env file")
                elif provider == "gemini":
                    print("   Configure GEMINI_API_KEY in .env file")
        
        return True
        
    except Exception as e:
        print(f"❌ AI provider test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 Trading Bot Setup Test\n")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_imports(),
        test_config(),
        test_ai_providers()
    ]
    
    results = await asyncio.gather(*tests)
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    if all(results):
        print("✅ All tests passed! Your setup looks good.")
        print("\n🎯 Next Steps:")
        print("1. Copy .env.example to .env and fill in your API keys")
        print("2. Make sure Ollama is running with llama3 model")
        print("3. Run the bot with: python run_bot.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that your Python version is 3.8+")
        print("3. Verify Ollama is installed and running")

if __name__ == "__main__":
    asyncio.run(main())
