"""
Main application entry point.
Orchestrates the trading bot components.
"""

import asyncio
import logging
import signal
import sys
from .config import load_config
from .binance_handler import BinanceHandler
from .ai_factory import AIFactory
from .functionSelector import FunctionSelector

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class TradingBotApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the trading bot application."""
        self.config = None
        self.binance = None
        self.ai_handler = None
        self.function_selector = None
        self.running = False
    
    async def start(self):
        """Start the trading bot application."""
        try:
            # Load configuration
            logger.info("Loading configuration...")
            self.config = load_config()
            
            # Initialize components
            logger.info("Initializing trading components...")
            self.binance = BinanceHandler(self.config)
            self.ai_handler = AIFactory.create_handler(self.config)
            self.function_selector = FunctionSelector(self.config, self.binance, self.ai_handler)
            
            # Start console interface
            logger.info("Starting console interface...")
            await self._show_welcome()
            await self._console_loop()
            
        except Exception as e:
            logger.error(f"Error starting application: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Stop the trading bot application."""
        logger.info("Shutting down trading bot...")
        self.running = False
        logger.info("Trading bot stopped.")
    
    async def _show_welcome(self):
        """Show welcome message."""
        print("\n" + "="*60)
        print("🤖 CRYPTO TRADING BOT - CONSOLE MODE")
        print("="*60)
        print("💡 Commands:")
        print("   /help     - Show help")
        print("   /quit     - Exit bot")
        print("")
        print("💬 Ask me anything:")
        print("   'What's the current BTC price?'")
        print("   'How much USDT do I have?'")
        print("   'What's my portfolio worth?'")
        print("   'Should I buy Bitcoin now?'")
        print("   'What's the market trend?'")
        print("   '/status' - System status")
        print("   '/ai' - AI provider status")
        print("   '/test' - Test intent classification")
        print("="*60)
        print("⚠️  Note: All trades require your confirmation!")
        print("="*60 + "\n")
    
    async def _console_loop(self):
        """Main console interaction loop."""
        self.running = True
        
        while self.running:
            try:
                # Get user input
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Process the input
                if user_input.startswith('/'):
                    await self._handle_command(user_input)
                else:
                    await self._handle_natural_language(user_input)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Console error: {e}")
    
    async def _handle_command(self, command: str):
        """Handle console commands."""
        command = command.lower().strip()
        
        if command == '/help':
            await self._show_welcome()
            
        elif command == '/quit' or command == '/exit':
            print("👋 Shutting down...")
            self.running = False
        
        else:
            # All other commands are handled by function selector
            await self._handle_natural_language(command)
    
    async def _handle_natural_language(self, text: str):
        """Handle natural language queries using function selector."""
        try:
            print("🤖 Analyzing your request...")
            
            # Use function selector to process the request
            result = await self.function_selector.process_user_request(text)
            
            # Display the response
            print(f"\n🤖 Bot:")
            print(result["message"])
            
            print("")  # Add spacing
            
        except Exception as e:
            print(f"❌ Error processing request: {e}")
            logger.error(f"Natural language error: {e}")
    
    def handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())


async def main():
    """Main entry point."""
    app = TradingBotApp()
    
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
