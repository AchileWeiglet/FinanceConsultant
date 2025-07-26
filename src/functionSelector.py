"""
Function Selector module.
Analyzes user intent and returns the appropriate function to execute.
"""

import logging
from typing import Callable, Any, Dict
from .ai_factory import AIFactory
from .binance_handler import BinanceHandler
from .config import Config
from .schemas import IntentClassification, TradingAnalysis
from .prompts import (
    get_btc_price_info_prompt, 
    get_usdt_balance_info_prompt, 
    get_portfolio_value_prompt,
    get_market_analysis_prompt,
    get_risk_assessment_prompt,
    get_trading_decision_prompt,
    get_volatile_market_prompt,
    get_portfolio_analysis_prompt,
    get_error_recovery_prompt
)

logger = logging.getLogger(__name__)


class FunctionSelector:
    """Selects and executes the appropriate function based on user intent."""
    
    def __init__(self, config: Config, binance: BinanceHandler, ai_handler):
        """Initialize the function selector."""
        self.config = config
        self.binance = binance
        self.intent_ai_handler = ai_handler  # Always Ollama for intent classification
        
        # Create separate AI handler for analysis (can be different provider)
        self.analysis_ai_handler = AIFactory.create_analysis_handler(config)
        
        logger.info(f"Intent classification AI: {config.ai_provider}")
        logger.info(f"Trading analysis AI: {config.analysis_ai_provider}")
        
        # Map intents to their corresponding functions
        self.intent_function_map = {
            "btc_price_info": self._handle_btc_price_info,
            "usdt_balance_info": self._handle_usdt_balance_info,
            "portfolio_value": self._handle_portfolio_value,
            "market_analysis": self._handle_market_analysis,
            "risk_assessment": self._handle_risk_assessment,
            "trading_decision": self._handle_trading_decision,
            "volatile_market": self._handle_volatile_market,
            "portfolio_analysis": self._handle_portfolio_analysis,
            "general_consult": self._handle_general_consult,
            "error_recovery": self._handle_error_recovery
        }
    
    async def process_user_request(self, user_message: str) -> Dict[str, Any]:
        """
        Process user request and return the appropriate response.
        
        Args:
            user_message: The user's message to process
            
        Returns:
            Dictionary with response data and metadata
        """
        try:
            # Classify the user's intent
            logger.info(f"Classifying intent for: {user_message[:50]}...")
            # Use intent AI handler (always Ollama) for classification
            intent = await self.intent_ai_handler.classify_user_intent(user_message)
            
            logger.info(f"Classified intent: {intent.intent} (confidence: {intent.confidence:.2f})")
            
            # Get the appropriate function
            handler_function = self.intent_function_map.get(intent.intent, self._handle_error_recovery)
            
            # Execute the function
            result = await handler_function(user_message, intent)
            
            # Add metadata
            result["intent_info"] = {
                "intent": intent.intent,
                "confidence": intent.confidence,
                "reasoning": intent.reasoning,
                "function_used": handler_function.__name__
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in function selector: {e}")
            return await self._handle_error_recovery(user_message, None, str(e))
    
    async def _handle_btc_price_info(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle BTC price information requests."""
        try:
            # Get current BTC price
            current_price = await self.binance.get_current_btc_price()
            
            # Get recent price history for context
            price_data = await self.binance.fetch_btc_price_history(3)  # Last 3 days
            formatted_history = self.binance.format_price_data_for_llm(price_data)
            
            return {
                "response_type": "btc_price_info",
                "data": {
                    "current_price": current_price,
                    "price_history": formatted_history
                },
                "message": f"₿ Current BTC Price: ${current_price:,.2f}",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling BTC price info: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error fetching BTC price: {e}",
                "success": False
            }
    
    async def _handle_usdt_balance_info(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle USDT balance and buying power requests."""
        try:
            # Get USDT balance
            usdt_balance = await self.binance.get_usdt_balance()
            
            # Get buying power
            buying_power = await self.binance.get_btc_buying_power()
            
            message = f"""💰 USDT Balance Information:
  💵 Total USDT: {usdt_balance:.2f} USDT
  📈 Current BTC Price: ${buying_power['btc_price']:,.2f}
  🔢 Usable USDT (after fees): {buying_power['usable_usdt']:.2f}
  ₿ Max BTC Buyable: {buying_power['max_btc_buyable']:.6f} BTC"""
            
            if self.config.binance_testnet:
                message += "\n  ℹ️ This is testnet data"
            
            return {
                "response_type": "usdt_balance_info",
                "data": {
                    "usdt_balance": usdt_balance,
                    "buying_power": buying_power
                },
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling USDT balance info: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error fetching USDT balance: {e}",
                "success": False
            }
    
    async def _handle_portfolio_value(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle portfolio value requests."""
        try:
            # Get portfolio information
            portfolio = await self.binance.get_portfolio_value_usdt()
            
            message = f"""📊 Portfolio Summary:
  ₿ BTC Holdings: {portfolio['btc_balance']:.6f} BTC
  📈 BTC Price: ${portfolio['btc_price']:,.2f}
  💰 BTC Value: ${portfolio['btc_value_usdt']:,.2f} USDT
  💵 USDT Balance: ${portfolio['usdt_balance']:,.2f} USDT
  {"="*40}
  🏦 Total Portfolio: ${portfolio['total_value_usdt']:,.2f} USDT
  📊 BTC Allocation: {portfolio['btc_allocation_percent']:.1f}%
  📊 USDT Allocation: {portfolio['usdt_allocation_percent']:.1f}%"""
            
            if self.config.binance_testnet:
                message += "\n  ℹ️ This is testnet data"
            
            return {
                "response_type": "portfolio_value",
                "data": portfolio,
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling portfolio value: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error calculating portfolio value: {e}",
                "success": False
            }
    
    async def _handle_market_analysis(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle market analysis requests."""
        try:
            # Fetch price data
            price_data = await self.binance.fetch_btc_price_history(self.config.price_analysis_days)
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Get AI analysis
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            
            message = f"""📊 Market Analysis:
📊 Analysis: {analysis.analysis}
💡 Suggestion: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}"""
            
            return {
                "response_type": "market_analysis",
                "data": analysis,
                "message": message,
                "success": True,
                "requires_trade_confirmation": analysis.intention in ["buy", "sell"] and analysis.amount > 0
            }
            
        except Exception as e:
            logger.error(f"Error handling market analysis: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error processing market analysis: {e}",
                "success": False
            }
    
    async def _handle_risk_assessment(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle risk assessment requests."""
        try:
            # Get current market data
            price_data = await self.binance.fetch_btc_price_history(self.config.price_analysis_days)
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Analyze for risk - use market analysis for now
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            
            message = f"""⚠️ Risk Assessment:
📊 Analysis: {analysis.analysis}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}
💡 Recommendation: {analysis.suggested_action}"""
            
            return {
                "response_type": "risk_assessment",
                "data": analysis,
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling risk assessment: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error processing risk assessment: {e}",
                "success": False
            }
    
    async def _handle_trading_decision(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle trading decision requests."""
        try:
            # Get market data and portfolio info
            price_data = await self.binance.fetch_btc_price_history(self.config.price_analysis_days)
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Get AI trading decision
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            
            message = f"""🎯 Trading Decision:
📊 Analysis: {analysis.analysis}
💡 Recommendation: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}"""
            
            if analysis.intention in ["buy", "sell"] and analysis.amount > 0:
                message += f"\n🔄 Suggested Action: {analysis.intention.upper()} {analysis.amount} BTC"
            
            return {
                "response_type": "trading_decision",
                "data": analysis,
                "message": message,
                "success": True,
                "requires_trade_confirmation": analysis.intention in ["buy", "sell"] and analysis.amount > 0
            }
            
        except Exception as e:
            logger.error(f"Error handling trading decision: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error processing trading decision: {e}",
                "success": False
            }
    
    async def _handle_volatile_market(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle volatile market concerns."""
        try:
            # Get recent price data to assess volatility
            price_data = await self.binance.fetch_btc_price_history(7)  # Last week
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Analyze with conservative approach
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            
            message = f"""🌪️ Volatile Market Analysis:
📊 Analysis: {analysis.analysis}
💡 Conservative Recommendation: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}
⚠️ Note: Extra caution recommended during volatile periods"""
            
            return {
                "response_type": "volatile_market",
                "data": analysis,
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling volatile market: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error analyzing volatile market: {e}",
                "success": False
            }
    
    async def _handle_portfolio_analysis(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle portfolio analysis and rebalancing requests."""
        try:
            # Get current portfolio
            portfolio = await self.binance.get_portfolio_value_usdt()
            
            # Get market data for context
            price_data = await self.binance.fetch_btc_price_history(self.config.price_analysis_days)
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Analyze portfolio with market context
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            
            message = f"""📊 Portfolio Analysis:
Current Allocation:
  🏦 Total Value: ${portfolio['total_value_usdt']:,.2f} USDT
  ₿ BTC: {portfolio['btc_allocation_percent']:.1f}% (${portfolio['btc_value_usdt']:,.2f})
  💵 USDT: {portfolio['usdt_allocation_percent']:.1f}% (${portfolio['usdt_balance']:,.2f})

Market-Based Recommendation:
📊 Analysis: {analysis.analysis}
💡 Suggestion: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}"""
            
            return {
                "response_type": "portfolio_analysis",
                "data": {
                    "portfolio": portfolio,
                    "analysis": analysis
                },
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling portfolio analysis: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error analyzing portfolio: {e}",
                "success": False
            }
    
    async def _handle_general_consult(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle general consultation requests."""
        try:
            # Simple informational response
            message = """🤖 Crypto Trading Bot Help:

Available Functions:
• 📈 Price Information - Get current BTC prices
• 💰 Balance Checking - Check USDT balance and buying power  
• 📊 Portfolio Analysis - View total portfolio value
• 🎯 Market Analysis - Get AI-powered market insights
• ⚠️ Risk Assessment - Evaluate trading risks
• 🔄 Trading Decisions - Get trading recommendations

Commands:
/price, /balance, /usdt, /portfolio, /status, /ai, /help

💬 Natural Language: Just ask questions like:
"What's BTC price?", "Should I buy?", "How's my portfolio?"

⚠️ Note: All trades require your explicit confirmation!"""
            
            return {
                "response_type": "general_consult",
                "data": {},
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling general consult: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error in general consultation: {e}",
                "success": False
            }
    
    async def _handle_error_recovery(self, user_message: str, intent: IntentClassification, error_msg: str = None) -> Dict[str, Any]:
        """Handle error recovery and unclear requests."""
        try:
            if error_msg:
                message = f"""❌ Error Processing Request:
{error_msg}

Please try:
• Being more specific with your request
• Using simpler language
• Trying a command like /help, /price, or /balance
• Asking direct questions like "What's BTC price?" or "How much USDT do I have?"

The bot understands:
📈 Price queries, 💰 Balance questions, 📊 Portfolio requests, 🎯 Trading advice"""
            else:
                message = """❓ I didn't quite understand your request.

Please try:
• Being more specific with your question
• Using commands like /help, /price, /balance
• Asking direct questions like:
  - "What's the current BTC price?"
  - "How much USDT do I have?"
  - "Should I buy Bitcoin now?"
  - "What's my portfolio worth?"

Type /help for more information."""
            
            return {
                "response_type": "error_recovery",
                "data": {},
                "message": message,
                "success": False
            }
            
        except Exception as e:
            logger.error(f"Error in error recovery: {e}")
            return {
                "response_type": "critical_error",
                "data": {},
                "message": "❌ Critical error occurred. Please restart the bot.",
                "success": False
            }
