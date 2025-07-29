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
            "error_recovery": self._handle_error_recovery,
            "price_alerts": self._handle_price_alerts,
            "trade_history": self._handle_trade_history,
            "technical_analysis": self._handle_technical_analysis,
            "news_sentiment": self._handle_news_sentiment,
            "stop_loss_management": self._handle_stop_loss_management,
            "dca_strategy": self._handle_dca_strategy,
            "multi_timeframe": self._handle_multi_timeframe,
            "educational_mode": self._handle_educational_mode
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
            # Quick manual override for news sentiment (expanded keywords)
            news_keywords = [
                "news sentiment", "sentiment analysis", "news of btc", "news about bitcoin", 
                "crypto news", "bitcoin news", "btc news", "market news", "latest news",
                "news affecting", "news impact", "social media sentiment", "news mood"
            ]
            
            if any(keyword in user_message.lower() for keyword in news_keywords):
                logger.info(f"Manual override: News sentiment detected in '{user_message}'")
                # Create a mock intent
                class MockIntent:
                    intent = "news_sentiment"
                    confidence = 0.95
                    reasoning = "Manual override for news sentiment - detected news keywords"
                    suggested_prompt_function = "get_news_sentiment_prompt"
                    required_data = ["news", "sentiment"]
                    user_query_type = "analysis"
                    premium_ai_requested = "openai" in user_message.lower() or "gemini" in user_message.lower()
                    requested_ai_provider = "openai" if "openai" in user_message.lower() else ("gemini" if "gemini" in user_message.lower() else "none")
                    comparison_analysis = False
                
                return await self._handle_news_sentiment(user_message, MockIntent())
            
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
            
            # Check if premium AI comparison is requested
            if intent.premium_ai_requested and intent.requested_ai_provider in ["openai", "gemini"]:
                return await self._handle_premium_ai_comparison(user_message, formatted_data, intent, "market_analysis")
            
            # Standard analysis (Ollama only)
            return await self._get_standard_analysis(user_message, formatted_data, "market_analysis")
            
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
            
            # Check if premium AI was requested
            if intent.premium_ai_requested and intent.requested_ai_provider != "none":
                return await self._handle_premium_ai_comparison(
                    user_message, formatted_data, intent, "trading_decision"
                )
            
            # Standard analysis with configured AI
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
    
    async def _handle_news_sentiment(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle news sentiment analysis requests."""
        try:
            # Get market data for context
            price_data = await self.binance.fetch_btc_price_history(7)  # Last week for context
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Mock news and sentiment data (in production, integrate with news APIs)
            mock_social_sentiment = "Neutral to slightly bullish sentiment on social media. Bitcoin discussions show cautious optimism."
            mock_news_data = "Recent news: Major institutions continue Bitcoin adoption, regulatory clarity improving, ETF approvals ongoing."
            mock_fear_greed = "Fear & Greed Index: 52 (Neutral) - Market showing balanced sentiment between fear and greed."
            
            # Check if premium AI comparison is requested
            if intent.premium_ai_requested and intent.requested_ai_provider in ["openai", "gemini"]:
                return await self._handle_premium_ai_comparison(user_message, formatted_data, intent, "news_sentiment")
            
            # Standard sentiment analysis
            from .prompts import get_sentiment_analysis_prompt
            prompt = get_sentiment_analysis_prompt(
                social_sentiment=mock_social_sentiment,
                news_data=mock_news_data,
                fear_greed_index=mock_fear_greed,
                technical_data=formatted_data,
                user_query=user_message
            )
            
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, prompt)
            
            message = f"""📰 News & Sentiment Analysis:
🌐 Social Sentiment: {mock_social_sentiment}
📰 Recent News: {mock_news_data}
😨😍 Fear/Greed Index: {mock_fear_greed}

📊 AI Analysis: {analysis.analysis}
💡 Recommendation: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}

💡 Note: News sentiment analysis combines social media buzz, major headlines, and market psychology indicators."""
            
            return {
                "response_type": "news_sentiment",
                "data": analysis,
                "message": message,
                "success": True,
                "requires_trade_confirmation": analysis.intention in ["buy", "sell"] and analysis.amount > 0
            }
            
        except Exception as e:
            logger.error(f"Error handling news sentiment: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error processing news sentiment analysis: {e}",
                "success": False
            }
    
    async def _handle_technical_analysis(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle technical analysis requests."""
        try:
            # Get price data for technical analysis
            price_data = await self.binance.fetch_btc_price_history(self.config.price_analysis_days)
            formatted_data = self.binance.format_price_data_for_llm(price_data)
            
            # Check if premium AI comparison is requested
            if intent.premium_ai_requested and intent.requested_ai_provider in ["openai", "gemini"]:
                return await self._handle_premium_ai_comparison(user_message, formatted_data, intent, "technical_analysis")
            
            # Standard technical analysis
            analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            
            message = f"""📊 Technical Analysis:
📈 Technical Analysis: {analysis.analysis}
💡 Recommendation: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}

📋 Note: Analysis includes price trends, support/resistance levels, volume patterns, and momentum indicators."""
            
            return {
                "response_type": "technical_analysis",
                "data": analysis,
                "message": message,
                "success": True,
                "requires_trade_confirmation": analysis.intention in ["buy", "sell"] and analysis.amount > 0
            }
            
        except Exception as e:
            logger.error(f"Error handling technical analysis: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error processing technical analysis: {e}",
                "success": False
            }
    
    async def _handle_educational_mode(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle educational content requests."""
        try:
            # Check if premium AI comparison is requested
            if intent.premium_ai_requested and intent.requested_ai_provider in ["openai", "gemini"]:
                # For educational content, use a simplified version of the data
                educational_data = "Educational content about cryptocurrency trading concepts"
                return await self._handle_premium_ai_comparison(user_message, educational_data, intent, "educational_mode")
            
            # Standard educational response
            message = f"""🎓 Crypto Trading Education:

📚 Your Question: {user_message}

🔰 Basic Concepts:
• Bitcoin (BTC): Digital currency and store of value
• USDT: Stablecoin pegged to US Dollar
• Support/Resistance: Key price levels where buying/selling occurs
• Volume: Number of coins traded (confirms price movements)
• Risk Management: Never invest more than you can afford to lose

⚠️ Important Warnings:
• Cryptocurrency is highly volatile
• Past performance doesn't guarantee future results  
• Always do your own research (DYOR)
• Start with small amounts to learn
• Never trade with borrowed money

📖 Next Steps:
• Learn about dollar-cost averaging (DCA)
• Understand technical indicators (RSI, MACD)
• Practice with small amounts first
• Keep learning about market analysis

💡 Use commands like "RSI analysis" or "What is DCA?" for specific topics."""
            
            # Create a basic educational analysis response
            from .schemas import TradingAnalysis
            educational_analysis = TradingAnalysis(
                intention="education",
                analysis=f"Educational response about: {user_message}",
                suggested_action="Continue learning about crypto trading fundamentals",
                confidence=1.0,
                risk_level="low"
            )
            
            return {
                "response_type": "educational_mode",
                "data": educational_analysis,
                "message": message,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling educational mode: {e}")
            return {
                "response_type": "error",
                "message": f"❌ Error processing educational request: {e}",
                "success": False
            }
    
    # Placeholder handlers for other new intents
    async def _handle_price_alerts(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle price alert requests."""
        return {
            "response_type": "price_alerts",
            "data": {},
            "message": "🔔 Price alerts feature coming soon! This will allow you to set intelligent price notifications with technical analysis.",
            "success": True
        }
    
    async def _handle_trade_history(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle trade history requests."""
        return {
            "response_type": "trade_history", 
            "data": {},
            "message": "📊 Trade history and performance analytics coming soon! This will track your trading performance and provide insights.",
            "success": True
        }
    
    async def _handle_stop_loss_management(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle stop loss management requests."""
        return {
            "response_type": "stop_loss_management",
            "data": {},
            "message": "🛡️ Stop loss management tools coming soon! This will help you set proper risk management levels.",
            "success": True
        }
    
    async def _handle_dca_strategy(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle DCA strategy requests."""
        return {
            "response_type": "dca_strategy",
            "data": {},
            "message": "💰 Dollar Cost Averaging (DCA) strategy tools coming soon! This will help you set up systematic investment plans.",
            "success": True
        }
    
    async def _handle_multi_timeframe(self, user_message: str, intent: IntentClassification) -> Dict[str, Any]:
        """Handle multi-timeframe analysis requests."""
        return {
            "response_type": "multi_timeframe",
            "data": {},
            "message": "⏱️ Multi-timeframe analysis coming soon! This will analyze 1H, 4H, 1D, and 1W charts for comprehensive insights.",
            "success": True
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
    
    async def _handle_premium_ai_comparison(self, user_message: str, formatted_data: str, intent: IntentClassification, analysis_type: str) -> Dict[str, Any]:
        """Handle premium AI comparison analysis."""
        try:
            # Create premium AI handler based on requested provider
            if intent.requested_ai_provider == "openai":
                from .openai_handler import OpenAIHandler
                premium_handler = OpenAIHandler(self.config)
                provider_name = "OpenAI GPT-4"
            elif intent.requested_ai_provider == "gemini":
                from .gemini_handler import GeminiHandler
                premium_handler = GeminiHandler(self.config)
                provider_name = "Google Gemini"
            else:
                # Fallback to standard analysis
                return await self._get_standard_analysis(user_message, formatted_data, analysis_type)
            
            # Get both analyses in parallel
            import asyncio
            ollama_task = self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
            premium_task = premium_handler.analyze_market_data(user_message, formatted_data)
            
            ollama_analysis, premium_analysis = await asyncio.gather(ollama_task, premium_task)
            
            # Helper function to escape special characters for Telegram
            def escape_telegram_text(text: str) -> str:
                """Escape special characters that can cause Telegram parsing issues."""
                # Remove or replace problematic characters
                text = text.replace('*', '•')  # Replace asterisks with bullets
                text = text.replace('_', '-')  # Replace underscores with dashes
                text = text.replace('[', '(')  # Replace square brackets
                text = text.replace(']', ')')
                text = text.replace('`', "'")  # Replace backticks with quotes
                text = text.replace('~', '-')  # Replace tildes
                return text
            
            # Format comparison message with safe text
            safe_ollama_analysis = escape_telegram_text(ollama_analysis.analysis[:200])
            safe_premium_analysis = escape_telegram_text(premium_analysis.analysis[:200])
            
            message = f"""🤖 AI Comparison Analysis - {analysis_type.replace('_', ' ').title()}

📱 Ollama (Free) Analysis:
📊 Recommendation: {escape_telegram_text(ollama_analysis.suggested_action)}
🎯 Confidence: {ollama_analysis.confidence:.1%}
⚠️ Risk: {ollama_analysis.risk_level.upper()}
💭 Analysis: {safe_ollama_analysis}{'...' if len(ollama_analysis.analysis) > 200 else ''}

🧠 {provider_name} (Premium) Analysis:
📊 Recommendation: {escape_telegram_text(premium_analysis.suggested_action)}
🎯 Confidence: {premium_analysis.confidence:.1%}
⚠️ Risk: {premium_analysis.risk_level.upper()}
💭 Analysis: {safe_premium_analysis}{'...' if len(premium_analysis.analysis) > 200 else ''}

🔍 Comparison Summary:"""
            
            # Compare the results
            if ollama_analysis.intention == premium_analysis.intention:
                if abs(ollama_analysis.confidence - premium_analysis.confidence) < 0.2:
                    message += f"\n✅ Both AI models AGREE on the recommendation: {ollama_analysis.intention.upper()}"
                    message += f"\n🎯 Consensus confidence: {(ollama_analysis.confidence + premium_analysis.confidence) / 2:.1%}"
                    comparison_result = "agreement"
                else:
                    message += f"\n⚖️ Same action but different confidence levels"
                    comparison_result = "partial_agreement"
            else:
                message += f"\n⚠️ CONFLICTING RECOMMENDATIONS"
                message += f"\n• Ollama suggests: {ollama_analysis.intention.upper()}"
                message += f"\n• {provider_name} suggests: {premium_analysis.intention.upper()}"
                message += f"\n• Consider waiting for clearer market signals"
                comparison_result = "conflict"
            
            # Add cost notice
            cost_estimate = "~$0.01-0.03" if intent.requested_ai_provider == "openai" else "~$0.005-0.015"
            message += f"\n\n💰 Premium AI usage cost: {cost_estimate}"
            
            # Determine which analysis to use for trading decisions
            if comparison_result == "agreement":
                final_analysis = premium_analysis if premium_analysis.confidence > ollama_analysis.confidence else ollama_analysis
            elif comparison_result == "partial_agreement":
                final_analysis = premium_analysis  # Trust premium for partial agreement
            else:
                # For conflicts, create a conservative analysis
                final_analysis = TradingAnalysis(
                    intention="nothing",
                    analysis="AI models disagree - recommend waiting for clearer signals",
                    suggested_action="Hold position and monitor market conditions",
                    confidence=0.3,
                    risk_level="high",
                    amount=0.001
                )
            
            return {
                "response_type": f"premium_{analysis_type}",
                "data": final_analysis,
                "message": message,
                "success": True,
                "comparison_result": comparison_result,
                "ollama_analysis": ollama_analysis,
                "premium_analysis": premium_analysis,
                "premium_provider": intent.requested_ai_provider,
                "cost_estimate": cost_estimate,
                "requires_trade_confirmation": final_analysis.intention in ["buy", "sell"] and final_analysis.amount > 0
            }
            
        except Exception as e:
            logger.error(f"Error in premium AI comparison: {e}")
            # Fallback to standard analysis
            return await self._get_standard_analysis(user_message, formatted_data, analysis_type)
    
    async def _get_standard_analysis(self, user_message: str, formatted_data: str, analysis_type: str) -> Dict[str, Any]:
        """Get standard analysis as fallback."""
        analysis = await self.analysis_ai_handler.analyze_market_data(user_message, formatted_data)
        
        message = f"""🎯 {analysis_type.replace('_', ' ').title()}:
📊 Analysis: {analysis.analysis}
💡 Recommendation: {analysis.suggested_action}
🎯 Confidence: {analysis.confidence:.1%}
⚠️ Risk Level: {analysis.risk_level.upper()}"""
        
        return {
            "response_type": analysis_type,
            "data": analysis,
            "message": message,
            "success": True,
            "requires_trade_confirmation": analysis.intention in ["buy", "sell"] and analysis.amount > 0
        }
