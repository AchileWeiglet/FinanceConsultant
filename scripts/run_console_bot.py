#!/usr/bin/env python3
"""
Console Trading Bot Runner
Run the trading bot in console mode for direct interaction.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import TradingBotApp

def main():
    """Run the console trading bot."""
    print("🚀 Console Trading Bot")
    print("=" * 30)
    
    try:
        # Run the bot
        bot = TradingBotApp()
        asyncio.run(bot.start())
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
