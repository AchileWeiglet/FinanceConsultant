"""
WhatsApp bot integration module.
Handles user interactions via WhatsApp using whatsapp-web.js bridge.
"""

import logging
import asyncio
import json
import subprocess
import os
from typing import Dict, Any, Optional
from .config import Config
from .schemas import TradingAnalysis, BotResponse
from .binance_handler import BinanceHandler
from .ai_factory import AIFactory

logger = logging.getLogger(__name__)


class WhatsAppBot:
    """WhatsApp bot for trading interactions."""
    
    def __init__(self, config: Config):
        """Initialize the WhatsApp bot."""
        self.config = config
        self.binance = BinanceHandler(config)
        self.ai_handler = AIFactory.create_handler(config)
        self.pending_trades: Dict[str, TradingAnalysis] = {}
        self.whatsapp_process = None
        self.is_running = False
        
    async def start(self):
        """Start the WhatsApp bot."""
        logger.info("Starting WhatsApp bot...")
        
        # Check if Node.js WhatsApp bridge exists
        bridge_path = os.path.join(os.path.dirname(__file__), '..', 'whatsapp_bridge', 'index.js')
        
        if not os.path.exists(bridge_path):
            logger.error("WhatsApp bridge not found. Please run setup first.")
            return False
        
        try:
            # Start the Node.js WhatsApp bridge
            self.whatsapp_process = subprocess.Popen(
                ['node', bridge_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.is_running = True
            logger.info("WhatsApp bot started successfully!")
            
            # Start message monitoring
            await self._monitor_messages()
            
        except Exception as e:
            logger.error(f"Failed to start WhatsApp bot: {e}")
            return False
    
    async def stop(self):
        """Stop the WhatsApp bot."""
        logger.info("Stopping WhatsApp bot...")
        self.is_running = False
        
        if self.whatsapp_process:
            self.whatsapp_process.terminate()
            self.whatsapp_process.wait()
        
        logger.info("WhatsApp bot stopped.")
    
    async def _monitor_messages(self):
        """Monitor incoming WhatsApp messages."""
        while self.is_running:
            try:
                # Check for new messages from the bridge
                await self._check_bridge_messages()
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error monitoring messages: {e}")
                await asyncio.sleep(5)
    
    async def _check_bridge_messages(self):
        """Check for messages from the WhatsApp bridge."""
        # This would read from a message queue or file that the Node.js bridge writes to
        message_file = os.path.join(os.path.dirname(__file__), '..', 'whatsapp_bridge', 'messages.json')
        
        if os.path.exists(message_file):
            try:
                with open(message_file, 'r') as f:
                    messages = json.load(f)
                
                for message in messages:
                    await self._process_message(message)
                
                # Clear processed messages
                with open(message_file, 'w') as f:
                    json.dump([], f)
                    
            except Exception as e:
                logger.error(f"Error reading messages: {e}")
    
    async def _process_message(self, message: Dict[str, Any]):
        """Process an incoming WhatsApp message."""
        try:
            sender = message.get('from', '')
            text = message.get('body', '')
            
            logger.info(f"Received message from {sender}: {text}")
            
            # Check if it's a command
            if text.startswith('/'):
                await self._handle_command(sender, text)
            else:
                await self._handle_natural_language(sender, text)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def _handle_command(self, sender: str, command: str):
        """Handle WhatsApp commands."""
        command = command.lower().strip()
        
        if command == '/start' or command == '/help':
            response = """🤖 *Crypto Trading Bot*

I'm your AI-powered trading assistant! I can help you:

• Analyze BTC price trends
• Suggest trading opportunities  
• Execute trades (with your confirmation)
• Monitor your portfolio

*Commands:*
/help - Show this help message
/balance - Check your account balance
/price - Get current BTC price
/status - Check system status
/ai - Check AI provider status

*Natural Language:*
Just ask me questions like:
• "How's BTC looking today?"
• "Should I buy some Bitcoin?"
• "Is BTC dropping too fast?"

⚠️ *Important:* I'll never execute trades without your explicit confirmation!"""

        elif command == '/balance':
            try:
                balances = await self.binance.get_account_balance()
                response = "*💰 Account Balance:*\n\n"
                for asset, balance in balances.items():
                    total = balance['free'] + balance['locked']
                    response += f"*{asset}:* {total:.6f}\n"
                    response += f"  • Available: {balance['free']:.6f}\n"
                    response += f"  • Locked: {balance['locked']:.6f}\n\n"
                
                if self.config.binance_testnet:
                    response += "ℹ️ _This is testnet data_"
                    
            except Exception as e:
                response = "❌ Error fetching balance. Please try again."
        
        elif command == '/price':
            try:
                price = await self.binance.get_current_btc_price()
                response = f"₿ *Current BTC Price:* ${price:,.2f}"
            except Exception as e:
                response = "❌ Error fetching price. Please try again."
        
        elif command == '/status':
            response = await self._get_status_message()
        
        elif command == '/ai':
            response = await self._get_ai_status_message()
        
        else:
            response = "❌ Unknown command. Send /help for available commands."
        
        await self._send_message(sender, response)
    
    async def _handle_natural_language(self, sender: str, text: str):
        """Handle natural language messages."""
        try:
            # Fetch price data
            price_data = await self.binance.fetch_btc_price_history(self.config.price_analysis_days)
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Get AI analysis
            analysis = await self.ai_handler.analyze_market_data(text, formatted_data)
            
            # Generate response
            response = self._generate_response(analysis, sender)
            
            # Send response
            await self._send_response(sender, response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self._send_message(sender, "❌ Sorry, I encountered an error processing your request. Please try again.")
    
    def _generate_response(self, analysis: TradingAnalysis, sender: str) -> BotResponse:
        """Generate bot response based on analysis."""
        # Build the main message
        message = f"🤖 *Analysis:*\n{analysis.analysis}\n\n"
        message += f"💡 *Suggestion:* {analysis.suggested_action}\n"
        message += f"🎯 *Confidence:* {analysis.confidence:.1%}\n"
        message += f"⚠️ *Risk Level:* {analysis.risk_level.upper()}\n"
        
        # Check if we should show confirmation
        show_confirmation = analysis.intention in ["buy", "sell"] and analysis.amount > 0
        
        if show_confirmation:
            # Store pending trade
            trade_id = f"{sender}_{len(self.pending_trades)}"
            self.pending_trades[trade_id] = analysis
            
            message += f"\n🔄 *Proposed Action:* {analysis.intention.upper()} {analysis.amount} BTC\n"
            message += "Reply with 'YES' to execute this trade or 'NO' to cancel."
            
            return BotResponse(
                message=message,
                show_confirmation=True,
                trade_data=analysis
            )
        else:
            return BotResponse(
                message=message,
                show_confirmation=False
            )
    
    async def _send_response(self, sender: str, response: BotResponse):
        """Send response message to user."""
        await self._send_message(sender, response.message)
    
    async def _send_message(self, to: str, message: str):
        """Send a WhatsApp message."""
        try:
            # Write message to outgoing queue for the Node.js bridge
            outgoing_file = os.path.join(os.path.dirname(__file__), '..', 'whatsapp_bridge', 'outgoing.json')
            
            outgoing_message = {
                'to': to,
                'message': message,
                'timestamp': asyncio.get_event_loop().time()
            }
            
            # Read existing outgoing messages
            outgoing_messages = []
            if os.path.exists(outgoing_file):
                try:
                    with open(outgoing_file, 'r') as f:
                        outgoing_messages = json.load(f)
                except:
                    outgoing_messages = []
            
            # Add new message
            outgoing_messages.append(outgoing_message)
            
            # Write back to file
            with open(outgoing_file, 'w') as f:
                json.dump(outgoing_messages, f, indent=2)
                
            logger.info(f"Queued message to {to}: {message[:50]}...")
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def _get_status_message(self) -> str:
        """Get system status message."""
        message = "🔄 *System Status:*\n\n"
        
        # Check AI provider
        try:
            ai_status = await self.ai_handler.health_check()
            provider_name = self.config.ai_provider.upper()
            message += f"🤖 {provider_name} AI: {'✅ Online' if ai_status else '❌ Offline'}\n"
        except:
            message += f"🤖 AI: ❌ Error\n"
        
        # Check Binance
        try:
            await self.binance.get_current_btc_price()
            binance_status = "✅ Online"
        except Exception:
            binance_status = "❌ Offline"
        
        message += f"📈 Binance API: {binance_status}\n"
        message += f"🔒 Trading: {'✅ Enabled' if self.config.enable_trading else '❌ Disabled'}\n"
        message += f"🧪 Testnet: {'Yes' if self.config.binance_testnet else 'No'}\n"
        
        return message
    
    async def _get_ai_status_message(self) -> str:
        """Get AI provider status message."""
        try:
            health_results = await AIFactory.test_provider_health(self.config)
            
            message = "🤖 *AI Provider Status:*\n\n"
            message += f"*Current Provider:* {self.config.ai_provider.upper()}\n\n"
            
            for provider, is_healthy in health_results.items():
                status = "✅ Available" if is_healthy else "❌ Unavailable"
                message += f"• *{provider.upper()}:* {status}\n"
                
                if provider == "ollama" and is_healthy:
                    message += f"  Model: {self.config.ollama_model}\n"
                elif provider == "openai" and is_healthy:
                    message += f"  Model: {self.config.openai_model}\n"
                elif provider == "gemini" and is_healthy:
                    message += f"  Model: {self.config.gemini_model}\n"
            
            message += f"\nℹ️ To change AI provider, update the `AI_PROVIDER` setting in your .env file."
            
            return message
            
        except Exception as e:
            return f"❌ Error checking AI provider status: {str(e)}"
