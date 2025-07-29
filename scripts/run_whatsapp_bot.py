#!/usr/bin/env python3
"""
WhatsApp Trading Bot Runner
Starts the WhatsApp bot instead of Telegram bot.
"""

import asyncio
import logging
import signal
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import load_config
from src.whatsapp_bot import WhatsAppBot

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class WhatsAppTradingBotApp:
    """Main WhatsApp trading bot application."""
    
    def __init__(self):
        """Initialize the WhatsApp trading bot application."""
        self.config = None
        self.whatsapp_bot = None
        self.running = False
    
    async def start(self):
        """Start the WhatsApp trading bot application."""
        try:
            # Load configuration
            logger.info("Loading configuration...")
            self.config = load_config()
            
            # Initialize WhatsApp bot
            logger.info("Initializing WhatsApp bot...")
            self.whatsapp_bot = WhatsAppBot(self.config)
            
            # Start services
            logger.info("Starting WhatsApp bot...")
            await self.whatsapp_bot.start()
            
            self.running = True
            logger.info("WhatsApp trading bot started successfully!")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error starting application: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Stop the WhatsApp trading bot application."""
        logger.info("Shutting down WhatsApp trading bot...")
        self.running = False
        
        if self.whatsapp_bot:
            await self.whatsapp_bot.stop()
        
        logger.info("WhatsApp trading bot stopped.")
    
    def handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())


async def main():
    """Main entry point."""
    print("🚀 WhatsApp Trading Bot")
    print("=" * 30)
    
    app = WhatsAppTradingBotApp()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, app.handle_signal)
    signal.signal(signal.SIGTERM, app.handle_signal)
    
    try:
        await app.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
