#!/usr/bin/env python3
"""
Simple Telegram bot runner script.
"""

import logging
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.telegram_bot import TelegramBot
from src.config import load_config

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Run the Telegram bot."""
    try:
        print("🤖 Starting Telegram Trading Bot")
        print("=" * 40)
        
        # Load configuration
        config = load_config()
        
        # Validate configuration
        if not config.telegram_bot_token or config.telegram_bot_token.startswith('dummy_'):
            print("❌ Please set a valid TELEGRAM_BOT_TOKEN in .env file")
            return
        
        if not config.telegram_chat_id or config.telegram_chat_id.startswith('dummy_'):
            print("❌ Please set a valid TELEGRAM_CHAT_ID in .env file")
            return
        
        print(f"✅ Bot token configured")
        print(f"✅ Chat ID: {config.telegram_chat_id}")
        print(f"🔗 Bot: @finance_helper_norman_bot")
        print("🚀 Starting bot...")
        
        # Create and start bot
        bot = TelegramBot(config)
        
        # Use the synchronous run_polling method
        bot.application.run_polling()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
