"""
Telegram bot integration module.
Handles user interactions using FunctionSelector like console bot.
"""

import logging
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from .config import Config
from .binance_handler import BinanceHandler
from .ai_factory import AIFactory
from .functionSelector import FunctionSelector

logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram bot for trading interactions using FunctionSelector."""
    
    def __init__(self, config: Config):
        """Initialize the Telegram bot."""
        self.config = config
        self.binance = BinanceHandler(config)
        self.ai_handler = AIFactory.create_handler(config)
        self.function_selector = FunctionSelector(config, self.binance, self.ai_handler)
        
        # Build application with error handling - compatible with v20+
        try:
            self.application = Application.builder().token(config.telegram_bot_token).build()
            self._setup_handlers()
            logger.info("Telegram bot initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Telegram bot: {e}")
            raise
    
    def _setup_handlers(self):
        """Set up message and command handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Message handler for all text (commands and natural language)
        self.application.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        
        # Callback handler for trade confirmations
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
🤖 **Crypto Trading Bot**

I'm your AI-powered trading assistant! I can help you:

• Analyze BTC price trends
• Get current prices and portfolio data
• Suggest trading opportunities
• Execute trades (with confirmation)

**Ask me anything:**
• "What's the current BTC price?"
• "How much USDT do I have?"
• "What's my portfolio worth?"
• "Should I buy Bitcoin now?"
• "What's the market trend?"
• "/status" - System status
• "/ai" - AI provider status
• "/test" - Test intent classification

⚠️ **Important:** All trades require your confirmation!
"""
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await self.start_command(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all messages (commands and natural language) using FunctionSelector."""
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        
        # Check if user is authorized
        if user_id != self.config.telegram_chat_id:
            await update.message.reply_text("❌ Unauthorized user.")
            return
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Handle basic bot commands
            if user_message.lower() in ['/quit', '/exit']:
                await update.message.reply_text("👋 Use /start to restart the conversation!")
                return
            
            # Use function selector to process the request (same as console bot)
            result = await self.function_selector.process_user_request(user_message)
            
            # Send the response
            await self._send_response(update, result)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "❌ Sorry, I encountered an error processing your request. Please try again."
            )
    
    async def _send_response(self, update: Update, result: Dict[str, Any]):
        """Send response message to user based on FunctionSelector result."""
        try:
            # Format the main response message
            message = f"🤖 **Bot Response:**\n\n{result['message']}"
            
            # Add intent info if available (for debugging/transparency)
            if "intent_info" in result:
                intent_info = result["intent_info"]
                message += f"\n\n🔍 **Debug Info:**\n"
                message += f"Intent: {intent_info['intent']} (confidence: {intent_info['confidence']:.2f})\n"
                message += f"Function: {intent_info['function_used']}\n"
                message += f"Intent AI: {self.config.ai_provider}"
                
                # Show intent AI model
                if self.config.ai_provider == "ollama":
                    message += f" ({self.config.ollama_model})\n"
                elif self.config.ai_provider == "openai":
                    message += f" ({self.config.openai_model})\n"
                elif self.config.ai_provider == "gemini":
                    message += f" ({self.config.gemini_model})\n"
                
                message += f"Analysis AI: {self.config.analysis_ai_provider}"
                
                # Show analysis AI model
                if self.config.analysis_ai_provider == "ollama":
                    message += f" ({self.config.ollama_model})"
                elif self.config.analysis_ai_provider == "openai":
                    message += f" ({self.config.openai_model})"
                elif self.config.analysis_ai_provider == "gemini":
                    message += f" ({self.config.gemini_model})"
            
            # Check if trade confirmation is needed
            if result.get("requires_trade_confirmation", False) and result.get("data"):
                analysis = result["data"]
                if hasattr(analysis, 'intention') and analysis.intention in ["buy", "sell"]:
                    message += f"\n\n🔄 **Proposed Action:** {analysis.intention.upper()} {analysis.amount} BTC"
                    
                    if self.config.enable_trading:
                        # Create confirmation buttons
                        keyboard = [
                            [
                                InlineKeyboardButton("✅ Execute Trade", callback_data=f"execute_{analysis.intention}_{analysis.amount}"),
                                InlineKeyboardButton("❌ Cancel", callback_data="cancel")
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        await update.message.reply_text(
                            message,
                            parse_mode='Markdown',
                            reply_markup=reply_markup
                        )
                        return
                    else:
                        message += "\n\nℹ️ Trading is disabled. Enable it in config to execute trades."
            
            # Send regular message without buttons
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error sending response: {e}")
            await update.message.reply_text("❌ Error sending response.")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline buttons."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "cancel":
            await query.edit_message_text("❌ Trade cancelled.")
            return
        
        if query.data.startswith("execute_"):
            try:
                # Parse the callback data
                parts = query.data.split("_")
                if len(parts) != 3:
                    await query.edit_message_text("❌ Invalid trade data.")
                    return
                
                intention = parts[1]  # buy or sell
                amount = float(parts[2])  # amount in BTC
                
                # Show execution message
                await query.edit_message_text("🔄 Executing trade...")
                
                # Execute the trade using binance handler
                if intention == "buy":
                    result = await self.binance.place_buy_order("BTCUSDT", amount)
                else:  # sell
                    result = await self.binance.place_sell_order("BTCUSDT", amount)
                
                # Format result message
                if result.get("status") == "simulated":
                    message = f"✅ **Trade Simulated!**\n\n"
                    message += f"Action: {intention.upper()}\n"
                    message += f"Amount: {amount} BTC\n"
                    message += f"Status: {result['message']}\n"
                    message += f"\nℹ️ This was a simulation since we're using public API only."
                elif result.get("status") == "success":
                    message = f"✅ **Trade Executed!**\n\n"
                    message += f"Order ID: {result.get('orderId', 'N/A')}\n"
                    message += f"Action: {intention.upper()}\n"
                    message += f"Amount: {amount} BTC\n"
                    message += f"Price: ${float(result.get('price', 0)):,.2f}\n"
                else:
                    message = f"❌ **Trade Failed:**\n{result.get('message', 'Unknown error')}"
                
                await query.edit_message_text(message, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"Error executing trade: {e}")
                await query.edit_message_text("❌ Error executing trade.")
    
    async def run(self):
        """Start the bot."""
        logger.info("Starting Telegram bot...")
        
        # For v20+, use run_polling directly
        await self.application.run_polling()
        
        logger.info("Telegram bot stopped.")
    
    async def stop(self):
        """Stop the bot."""
        logger.info("Stopping Telegram bot...")
        await self.application.stop()
        await self.application.shutdown()
        logger.info("Telegram bot stopped.")


async def main():
    """Main function to run the Telegram bot."""
    try:
        from .config import load_config
        
        print("🤖 Starting Telegram Trading Bot")
        print("=" * 40)
        
        # Load configuration
        config = load_config()
        
        # Create bot instance
        bot = TelegramBot(config)
        
        # Start the bot using run_polling which handles everything
        print("✅ Bot configured successfully!")
        print(f"🔗 Bot: @finance_helper_norman_bot")
        print(f"👤 Authorized user: {config.telegram_chat_id}")
        print("🚀 Starting bot...")
        
        await bot.run()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
