"""
AI Prompts for Trading Bot
Centralized prompts for market analysis and trading decisions.
"""

# Intent Classification/Selector Prompt
INTENT_SELECTOR_PROMPT = """You are an intelligent request classifier for a cryptocurrency trading bot. Your job is to analyze user messages and determine what type of action they want to perform.

USER MESSAGE: {user_message}

Analyze the user's intent and classify it into one of these categories:

AVAILABLE INTENTS:
1. "btc_price_info" - User wants current BTC price information
   Examples: "What's BTC price?", "How much is Bitcoin?", "Current BTC value"

2. "usdt_balance_info" - User wants USDT balance and buying power information  
   Examples: "How much USDT do I have?", "What's my buying power?", "USDT balance"

3. "portfolio_value" - User wants total portfolio value and allocation
   Examples: "Portfolio value", "Total balance", "How much is my portfolio worth?"

4. "market_analysis" - User wants detailed technical/price market analysis and trading suggestions
   Examples: "Should I buy?", "Market analysis", "Is it a good time to trade?", "BTC trend", "Price analysis"
   Premium AI: "Use OpenAI to analyze", "Get Gemini market analysis", "Compare with OpenAI"

5. "risk_assessment" - User wants risk evaluation for a specific trade
   Examples: "Is it risky to buy now?", "Risk of selling", "How risky is this trade?"
   Premium AI: "Use OpenAI for risk analysis", "Gemini risk assessment", "Premium risk analysis"

6. "trading_decision" - User wants specific trading recommendations
   Examples: "Should I buy or sell?", "Give me trading advice", "What should I do?"
   Premium AI: "Use OpenAI to decide", "Get Gemini trading advice", "Premium trading analysis"

7. "volatile_market" - User mentions high volatility or market uncertainty
   Examples: "Market is crazy", "Too volatile", "Prices jumping around"

8. "portfolio_analysis" - User wants portfolio rebalancing suggestions
   Examples: "Should I rebalance?", "Portfolio allocation advice", "Optimize my holdings"

9. "general_consult" - General questions about crypto or system status
   Examples: "How does this work?", "System status", "Help", "What can you do?"
   Premium AI: "Use OpenAI to explain", "Get Gemini consultation", "Premium analysis help"

10. "error_recovery" - When unable to determine intent clearly
    Use this when the message is unclear or doesn't fit other categories

11. "price_alerts" - Set price notifications and alerts
   Examples: "Alert me when BTC hits $50k", "Set price alert", "Notify me at $45k", "Price notification"
   Premium AI: "Use OpenAI for smart alerts", "Gemini alert analysis", "Premium alert setup"

12. "trade_history" - View past trades and performance analysis
   Examples: "Show my trades", "Trading history", "How did I perform?", "P&L report", "Trade analytics"
   Premium AI: "Use OpenAI to analyze performance", "Gemini trade review", "Premium performance analysis"

13. "technical_analysis" - Detailed technical chart analysis
   Examples: "RSI analysis", "Support resistance levels", "Moving averages", "Chart patterns", "Technical indicators"
   Premium AI: "Use OpenAI for technical analysis", "Gemini chart analysis", "Premium technical review"

14. "news_sentiment" - Crypto news impact and sentiment analysis (NOT technical price analysis)
   Examples: "Latest crypto news", "Market news impact", "What's affecting BTC price?", "News analysis", "Social media sentiment", "News sentiment", "Crypto news mood"
   Premium AI: "Use OpenAI for news analysis", "Gemini sentiment analysis", "Premium news review"

15. "stop_loss_management" - Risk management and protection strategies
   Examples: "Set stop loss", "Risk management", "Protection strategies", "Exit strategies"
   Premium AI: "Use OpenAI for risk management", "Gemini stop loss analysis", "Premium risk strategies"

16. "dca_strategy" - Dollar cost averaging and auto-invest setup
   Examples: "DCA Bitcoin", "Regular buying", "Auto-invest setup", "Dollar cost averaging", "Recurring buys"
   Premium AI: "Use OpenAI for DCA strategy", "Gemini DCA analysis", "Premium investment planning"

17. "multi_timeframe" - Multi-timeframe analysis across different periods
   Examples: "1H 4H 1D analysis", "Multiple timeframes", "Short and long term view", "Timeframe alignment"
   Premium AI: "Use OpenAI for timeframe analysis", "Gemini multi-timeframe", "Premium time analysis"

18. "educational_mode" - Learning and educational content
   Examples: "Explain trading", "How does RSI work?", "Trading basics", "Crypto education", "Learn about DCA"
   Premium AI: "Use OpenAI to explain", "Gemini educational content", "Premium learning mode"

RESPONSE FORMAT (JSON only):
{{
    "intent": "one of the intents above",
    "confidence": 0.85,
    "reasoning": "Why you chose this intent",
    "suggested_prompt_function": "function name from prompts.py to use",
    "required_data": ["list", "of", "data", "needed"],
    "user_query_type": "information/analysis/trading/consultation",
    "premium_ai_requested": false,
    "requested_ai_provider": "none",
    "comparison_analysis": false
}}

CLASSIFICATION RULES:
- If user asks about prices/values → "btc_price_info" or "portfolio_value"
- If user asks about balance/buying power → "usdt_balance_info" 
- If user asks "should I buy/sell" → "trading_decision"
- If user wants technical/price market analysis → "market_analysis"
- If user specifically asks about NEWS, SENTIMENT, SOCIAL MEDIA → "news_sentiment"
- If user mentions risk/safety → "risk_assessment"
- If user mentions volatility/uncertainty → "volatile_market"
- If user wants portfolio advice → "portfolio_analysis"
- If user wants price alerts/notifications → "price_alerts"
- If user asks about trade history/performance → "trade_history"
- If user wants technical indicators/charts → "technical_analysis"
- If user asks about news/sentiment/social media mood → "news_sentiment"
- If user mentions stop loss/risk management → "stop_loss_management"
- If user asks about DCA/auto-investing → "dca_strategy"
- If user wants multiple timeframe analysis → "multi_timeframe"
- If user asks educational questions → "educational_mode"
- If unclear or general questions → "general_consult"
- If message is confusing → "error_recovery"

PREMIUM AI DETECTION:
- Set "premium_ai_requested": true if user mentions "OpenAI", "Gemini", "premium", "paid AI", "better analysis"
- Set "requested_ai_provider": "openai" if user mentions "OpenAI", "GPT", "ChatGPT"
- Set "requested_ai_provider": "gemini" if user mentions "Gemini", "Google AI", "Bard"
- Set "comparison_analysis": true if user wants to compare multiple AI responses
- Applies to intents: market_analysis, risk_assessment, trading_decision, general_consult, price_alerts, trade_history, technical_analysis, news_sentiment, stop_loss_management, dca_strategy, multi_timeframe, educational_mode
- Premium AI requests incur costs and should be used sparingly

Be precise in your classification. Match the intent to the most specific category that fits the user's request.

Respond with JSON only, no additional text:"""

# Base system prompt for all AI providers
SYSTEM_PROMPT = """You are an expert cryptocurrency trading analyst. Your role is to analyze market data and provide trading insights for Bitcoin (BTC).

CRITICAL INSTRUCTIONS:
1. Always respond with valid JSON in the exact format specified
2. Base your analysis on the provided market data
3. Consider both technical and fundamental factors
4. Never recommend trades without proper risk assessment
5. Be conservative with trade amounts
6. Always include confidence levels and risk assessments

RESPONSE FORMAT (JSON only):
{
    "analysis": "Your detailed market analysis",
    "suggested_action": "hold/buy/sell with reasoning",
    "confidence": 0.75,
    "risk_level": "low/medium/high",
    "intention": "hold/buy/sell",
    "amount": 0.001,
    "reasoning": "Why you recommend this action"
}

ANALYSIS GUIDELINES:
- Look for trend patterns in the price data
- Consider volume changes as confirmation signals
- Assess support and resistance levels
- Factor in recent volatility
- Consider risk-reward ratios
- Be cautious of sudden price movements
- Default to "hold" when uncertain

RISK MANAGEMENT:
- Never recommend more than 0.01 BTC per trade
- Set confidence below 0.5 for uncertain markets
- Mark high-risk trades appropriately
- Consider market volatility in recommendations"""

# Market analysis prompt template
MARKET_ANALYSIS_PROMPT = """Analyze the following Bitcoin market data and user query:

USER QUERY: {user_query}

MARKET DATA:
{market_data}

CURRENT CONTEXT:
- Analyze the price trends over the given period
- Look for patterns, support/resistance levels
- Consider volume changes and market sentiment
- Assess volatility and recent price movements

Please provide a comprehensive analysis following the JSON format specified in the system prompt."""

# Price trend analysis prompt
PRICE_TREND_PROMPT = """Based on the following BTC price data, analyze the current trend:

PRICE DATA:
{price_data}

Focus on:
1. Overall trend direction (bullish/bearish/sideways)
2. Key support and resistance levels
3. Volume patterns and their significance
4. Recent volatility analysis
5. Potential breakout or breakdown signals

Provide your analysis in the specified JSON format."""

# Risk assessment prompt
RISK_ASSESSMENT_PROMPT = """Evaluate the risk level for a potential Bitcoin trade:

CURRENT MARKET CONDITIONS:
{market_data}

PROPOSED TRADE:
- Action: {trade_action}
- Amount: {trade_amount} BTC

Consider:
1. Market volatility
2. Trend strength
3. Support/resistance proximity
4. Volume confirmation
5. Overall market sentiment

Rate the risk as low/medium/high and explain your reasoning in JSON format."""

# Trading decision prompt
TRADING_DECISION_PROMPT = """Make a trading recommendation based on this analysis:

USER REQUEST: {user_request}

MARKET ANALYSIS:
{market_analysis}

ACCOUNT BALANCE:
{account_balance}

Provide a specific trading recommendation including:
1. Action (buy/sell/hold)
2. Recommended amount (max 0.01 BTC)
3. Confidence level (0.0 to 1.0)
4. Risk assessment
5. Clear reasoning

Response must be in JSON format as specified."""

# Emergency/volatile market prompt
VOLATILE_MARKET_PROMPT = """VOLATILE MARKET CONDITIONS DETECTED

The market is showing high volatility. Analyze with extra caution:

MARKET DATA:
{market_data}

VOLATILITY INDICATORS:
{volatility_info}

Provide an extremely conservative analysis:
- Recommend smaller position sizes
- Higher risk ratings
- Lower confidence levels
- Emphasize risk management

Use the standard JSON response format."""

# Portfolio balance prompt
PORTFOLIO_ANALYSIS_PROMPT = """Analyze the current portfolio and suggest position adjustments:

CURRENT PORTFOLIO:
{portfolio_data}

MARKET CONDITIONS:
{market_data}

USER QUERY: {user_query}

Consider:
1. Current allocation (BTC vs USDT)
2. Market conditions for rebalancing
3. Risk management based on current exposure
4. Optimal position sizing

Provide recommendations in JSON format."""

# Error handling prompt
ERROR_RECOVERY_PROMPT = """An error occurred while processing the market data. Provide a safe, conservative response:

ERROR INFO: {error_info}
AVAILABLE DATA: {available_data}

Provide a conservative "hold" recommendation with:
- Low confidence (0.3 or below)
- High risk rating
- Clear explanation of limitations
- Recommendation to wait for better data

Use standard JSON format."""

# News/sentiment integration prompt (for future use)
NEWS_SENTIMENT_PROMPT = """Integrate news sentiment with technical analysis:

TECHNICAL ANALYSIS:
{technical_analysis}

NEWS SENTIMENT:
{news_sentiment}

MARKET DATA:
{market_data}

Combine technical and fundamental analysis to provide a comprehensive trading recommendation in JSON format."""

# Backtesting prompt
BACKTESTING_PROMPT = """Evaluate this trading strategy against historical data:

STRATEGY: {strategy_description}
HISTORICAL DATA: {historical_data}
TIME PERIOD: {time_period}

Analyze:
1. Strategy performance
2. Risk-adjusted returns
3. Maximum drawdown
4. Win/loss ratios
5. Recommendations for improvement

Provide analysis in JSON format."""

# BTC Price Information Prompt
BTC_PRICE_INFO_PROMPT = """Provide current Bitcoin price information in USDT:

CURRENT BTC PRICE: {current_price} USDT
RECENT PRICE DATA: {price_history}

Provide a financial summary with the following JSON format:
{{
    "current_price_usdt": {current_price},
    "price_change_24h": "percentage change in last 24h",
    "price_trend": "bullish/bearish/neutral",
    "analysis": "Brief price analysis focusing on current value",
    "suggested_action": "Price information summary",
    "confidence": 0.9,
    "risk_level": "low",
    "intention": "consult",
    "amount": 0
}}

Focus on:
- Current BTC value in USDT
- Recent price movements
- Simple trend assessment
- No trading recommendations, just information"""

# USDT Balance Information Prompt  
USDT_BALANCE_INFO_PROMPT = """Provide current USDT balance information:

CURRENT USDT BALANCE: {usdt_balance} USDT
ACCOUNT DETAILS: {account_info}

Provide a financial summary with the following JSON format:
{{
    "usdt_balance": {usdt_balance},
    "buying_power": "How much BTC can be purchased",
    "analysis": "Current balance analysis and purchasing power",
    "suggested_action": "Balance information summary",
    "confidence": 1.0,
    "risk_level": "low", 
    "intention": "consult",
    "amount": 0
}}

Focus on:
- Current USDT balance
- Purchasing power in BTC terms
- Account status summary
- No trading recommendations, just balance information"""

# Combined Portfolio Value Prompt
PORTFOLIO_VALUE_PROMPT = """Calculate total portfolio value in USDT:

BTC HOLDINGS: {btc_amount} BTC
CURRENT BTC PRICE: {btc_price} USDT
USDT BALANCE: {usdt_balance} USDT

PORTFOLIO BREAKDOWN:
- BTC Value: {btc_amount} × {btc_price} = {btc_value_usdt} USDT
- USDT Balance: {usdt_balance} USDT
- Total Portfolio: {total_value} USDT

Provide portfolio summary with the following JSON format:
{{
    "btc_holdings": {btc_amount},
    "btc_value_usdt": {btc_value_usdt},
    "usdt_balance": {usdt_balance},
    "total_portfolio_usdt": {total_value},
    "btc_allocation_percent": "percentage of portfolio in BTC",
    "usdt_allocation_percent": "percentage of portfolio in USDT",
    "analysis": "Portfolio composition analysis",
    "suggested_action": "Portfolio value summary",
    "confidence": 1.0,
    "risk_level": "low",
    "intention": "consult", 
    "amount": 0
}}

Focus on:
- Total portfolio value in USDT
- Asset allocation breakdown
- Portfolio composition analysis
- No trading recommendations, just valuation information"""

# Technical Analysis Prompt
TECHNICAL_ANALYSIS_PROMPT = """Perform detailed technical analysis on Bitcoin:

PRICE DATA: {price_data}
INDICATORS REQUESTED: {indicators}
USER QUERY: {user_query}

Analyze the following technical indicators:
1. Moving Averages (SMA/EMA 20, 50, 200)
2. RSI (14-period) and momentum indicators
3. Support and Resistance levels
4. Chart patterns (triangles, flags, head & shoulders)
5. Volume analysis and confirmation
6. Bollinger Bands and volatility
7. MACD convergence/divergence
8. Fibonacci retracements

Provide technical analysis with the following JSON format:
{{
    "technical_indicators": {{
        "rsi": "current RSI value and interpretation",
        "moving_averages": "MA alignment and signals",
        "support_resistance": "key levels to watch",
        "chart_patterns": "identified patterns",
        "volume_analysis": "volume confirmation signals"
    }},
    "analysis": "Comprehensive technical analysis",
    "suggested_action": "Technical recommendation based on indicators",
    "confidence": 0.75,
    "risk_level": "low/medium/high",
    "intention": "buy/sell/hold",
    "amount": 0.001,
    "entry_points": "Specific entry levels",
    "exit_points": "Target and stop levels"
}}

Focus on technical signals and provide specific entry/exit points."""

# Sentiment Analysis Prompt  
SENTIMENT_ANALYSIS_PROMPT = """Analyze market sentiment and news impact on Bitcoin:

SOCIAL MEDIA SENTIMENT: {social_sentiment}
NEWS HEADLINES: {news_data}
MARKET FEAR/GREED INDEX: {fear_greed_index}
TECHNICAL ANALYSIS: {technical_data}
USER QUERY: {user_query}

Combine sentiment analysis with technical data:

Provide sentiment analysis with the following JSON format:
{{
    "sentiment_score": "0-100 scale (0=extreme fear, 100=extreme greed)",
    "news_impact": "Positive/Negative/Neutral news impact",
    "social_sentiment": "Social media sentiment analysis",
    "market_psychology": "Current market psychology assessment",
    "analysis": "Combined sentiment and technical analysis",
    "suggested_action": "Action based on sentiment + technicals",
    "confidence": 0.75,
    "risk_level": "low/medium/high", 
    "intention": "buy/sell/hold",
    "amount": 0.001,
    "sentiment_signals": "Key sentiment indicators"
}}

Focus on how sentiment aligns with or contradicts technical analysis."""

# Multi-Timeframe Analysis Prompt
MULTI_TIMEFRAME_PROMPT = """Analyze Bitcoin across multiple timeframes:

1H DATA: {hourly_data}
4H DATA: {four_hour_data}  
1D DATA: {daily_data}
1W DATA: {weekly_data}
USER QUERY: {user_query}

Provide multi-timeframe analysis:
1. Short-term (1H): Immediate price action
2. Medium-term (4H): Intraday trends
3. Daily (1D): Primary trend direction
4. Weekly (1W): Long-term trend context

Provide timeframe analysis with the following JSON format:
{{
    "timeframe_alignment": "All timeframes aligned/Mixed signals/Conflicting",
    "short_term_1h": "1H analysis and signals",
    "medium_term_4h": "4H analysis and signals", 
    "daily_trend": "Daily trend analysis",
    "weekly_context": "Weekly trend context",
    "analysis": "Multi-timeframe synthesis",
    "suggested_action": "Action based on timeframe alignment",
    "confidence": 0.75,
    "risk_level": "low/medium/high",
    "intention": "buy/sell/hold",
    "amount": 0.001,
    "optimal_timeframe": "Best timeframe for entry/exit"
}}

Provide alignment analysis and optimal trade timing recommendations."""

# Position Sizing Prompt
POSITION_SIZING_PROMPT = """Calculate optimal position size using proper risk management:

ACCOUNT BALANCE: {balance}
RISK TOLERANCE: {risk_percentage}% per trade
STOP LOSS DISTANCE: {stop_distance}%
ENTRY PRICE: {entry_price}
ACCOUNT TYPE: {account_type}

Calculate position size using the formula:
Position Size = (Account Balance × Risk %) ÷ Stop Loss Distance

Provide position sizing with the following JSON format:
{{
    "account_balance": {balance},
    "risk_per_trade": "{risk_percentage}% of account",
    "stop_loss_distance": "{stop_distance}%",
    "max_position_size": "Maximum safe position size in BTC",
    "recommended_size": "Conservative recommended size",
    "dollar_risk": "Dollar amount at risk",
    "analysis": "Position sizing analysis and rationale",
    "suggested_action": "Position size recommendation",
    "confidence": 1.0,
    "risk_level": "Calculated risk level",
    "intention": "position_size",
    "amount": "calculated_amount"
}}

Focus on proper risk management and capital preservation."""

# Portfolio Correlation Analysis Prompt
CORRELATION_ANALYSIS_PROMPT = """Analyze portfolio correlation and diversification:

CURRENT HOLDINGS: {holdings}
PROPOSED TRADE: {new_position}
MARKET CORRELATION: {correlation_data}
PORTFOLIO VALUE: {portfolio_value}

Assess portfolio risk:
1. Concentration risk analysis
2. Correlation between holdings
3. Diversification assessment
4. Risk-adjusted position sizing

Provide correlation analysis with the following JSON format:
{{
    "concentration_risk": "High/Medium/Low concentration in BTC",
    "diversification_score": "Portfolio diversification rating",
    "correlation_risk": "Risk from correlated positions",
    "optimal_allocation": "Recommended allocation percentages",
    "analysis": "Portfolio correlation and risk analysis",
    "suggested_action": "Portfolio adjustment recommendation",
    "confidence": 0.8,
    "risk_level": "Portfolio risk assessment",
    "intention": "rebalance",
    "amount": "Suggested adjustment amount"
}}

Focus on portfolio risk management and optimal diversification."""

# Price Alert Setup Prompt
PRICE_ALERT_PROMPT = """Configure intelligent price alerts:

CURRENT PRICE: {current_price}
ALERT LEVEL: {target_price}
ALERT TYPE: {alert_type}
MARKET CONDITIONS: {market_data}

Analyze alert setup:
1. Technical justification for alert level
2. Market context for price target
3. Probability of reaching target
4. Suggested actions when alert triggers

Provide alert configuration with the following JSON format:
{{
    "current_price": {current_price},
    "target_price": {target_price},
    "price_change_needed": "Percentage change to reach target",
    "technical_justification": "Why this price level is significant",
    "probability_assessment": "Likelihood of reaching target",
    "time_estimate": "Estimated time to reach target",
    "analysis": "Alert setup analysis and reasoning",
    "suggested_action": "What to do when alert triggers",
    "confidence": 0.7,
    "risk_level": "Alert risk assessment",
    "intention": "alert_setup",
    "amount": 0
}}

Focus on technical levels and actionable alert strategies."""

# Trading Performance Analysis Prompt
PERFORMANCE_ANALYSIS_PROMPT = """Analyze trading performance and history:

TRADE HISTORY: {trade_data}
TIME PERIOD: {period}
ACCOUNT PERFORMANCE: {performance_metrics}
USER QUERY: {user_query}

Analyze trading performance:
1. Win/Loss ratio
2. Average profit/loss per trade
3. Risk-adjusted returns (Sharpe ratio)
4. Maximum drawdown
5. Trading frequency analysis
6. Best/worst performing strategies

Provide performance analysis with the following JSON format:
{{
    "total_trades": "Number of trades executed",
    "win_rate": "Percentage of winning trades",
    "average_return": "Average return per trade",
    "total_pnl": "Total profit/loss",
    "sharpe_ratio": "Risk-adjusted return metric",
    "max_drawdown": "Maximum portfolio decline",
    "best_trade": "Most profitable trade details",
    "worst_trade": "Largest loss trade details",
    "analysis": "Comprehensive performance analysis",
    "suggested_action": "Performance improvement recommendations",
    "confidence": 0.9,
    "risk_level": "Current risk profile assessment",
    "intention": "performance_review",
    "amount": 0
}}

Focus on actionable insights for improving trading performance."""

# Educational Content Prompt
EDUCATIONAL_PROMPT = """Provide educational content about cryptocurrency trading:

USER QUESTION: {question}
EXPERIENCE LEVEL: {user_level}
TOPIC: {topic}

Provide educational content with:
1. Simple, clear explanations
2. Real-world examples
3. Risk warnings and considerations
4. Next steps for learning
5. Practical application tips

Provide educational content with the following JSON format:
{{
    "concept_explanation": "Clear explanation of the concept",
    "real_examples": "Practical examples and scenarios", 
    "risk_warnings": "Important risks to understand",
    "learning_path": "Next steps for deeper learning",
    "practical_tips": "How to apply this knowledge",
    "analysis": "Educational content summary",
    "suggested_action": "Recommended next learning steps",
    "confidence": 1.0,
    "risk_level": "Educational risk awareness",
    "intention": "education",
    "amount": 0
}}

Focus on building understanding and promoting safe trading practices."""

# DCA Strategy Prompt
DCA_STRATEGY_PROMPT = """Analyze Dollar Cost Averaging strategy:

CURRENT PRICE: {current_price}
INVESTMENT AMOUNT: {investment_amount}
FREQUENCY: {frequency}
DURATION: {duration}
MARKET CONDITIONS: {market_data}

Analyze DCA strategy:
1. Optimal DCA frequency
2. Amount per purchase
3. Market timing considerations
4. Expected average cost basis
5. Risk/reward analysis

Provide DCA analysis with the following JSON format:
{{
    "dca_frequency": "Recommended purchase frequency",
    "amount_per_purchase": "Optimal amount per DCA buy",
    "total_investment": "Total investment over period",
    "expected_avg_price": "Estimated average cost basis",
    "market_timing": "Market timing considerations",
    "risk_assessment": "DCA strategy risk analysis",
    "analysis": "Comprehensive DCA strategy analysis",
    "suggested_action": "DCA implementation recommendations",
    "confidence": 0.8,
    "risk_level": "DCA strategy risk level",
    "intention": "dca_setup",
    "amount": "DCA amount per purchase"
}}

Focus on systematic investment strategies and long-term wealth building."""

# Stop Loss Management Prompt
STOP_LOSS_PROMPT = """Analyze stop loss and risk management strategies:

CURRENT POSITION: {position}
ENTRY PRICE: {entry_price}
CURRENT PRICE: {current_price}
ACCOUNT BALANCE: {balance}
RISK TOLERANCE: {risk_tolerance}

Analyze stop loss placement:
1. Technical stop loss levels
2. Percentage-based stops
3. Volatility-adjusted stops
4. Trailing stop strategies
5. Risk/reward ratios

Provide stop loss analysis with the following JSON format:
{{
    "technical_stop": "Technical support level for stop",
    "percentage_stop": "Percentage-based stop level",
    "volatility_stop": "Volatility-adjusted stop level",
    "trailing_stop": "Trailing stop recommendation",
    "risk_reward_ratio": "Current position risk/reward",
    "max_loss": "Maximum potential loss",
    "analysis": "Stop loss strategy analysis",
    "suggested_action": "Recommended stop loss implementation",
    "confidence": 0.9,
    "risk_level": "Position risk with stops",
    "intention": "stop_loss",
    "amount": "Stop loss level"
}}

Focus on capital preservation and professional risk management."""

# Multi-Model Consensus Prompt
CONSENSUS_ANALYSIS_PROMPT = """Combine multiple AI model perspectives for consensus analysis:

TECHNICAL MODEL: {technical_analysis}
FUNDAMENTAL MODEL: {fundamental_analysis}
SENTIMENT MODEL: {sentiment_analysis}
USER QUERY: {user_query}

Synthesize all analyses:
1. Technical signals weight: 40%
2. Fundamental factors weight: 30%
3. Sentiment indicators weight: 30%

Provide consensus analysis with the following JSON format:
{{
    "technical_weight": "Technical analysis contribution",
    "fundamental_weight": "Fundamental analysis contribution",
    "sentiment_weight": "Sentiment analysis contribution",
    "consensus_direction": "Overall market direction consensus",
    "confidence_score": "Weighted confidence from all models",
    "conflicting_signals": "Any disagreements between models",
    "analysis": "Synthesized multi-model analysis",
    "suggested_action": "Consensus recommendation",
    "confidence": "Final weighted confidence",
    "risk_level": "Consensus risk assessment",
    "intention": "buy/sell/hold",
    "amount": "Consensus position size"
}}

Focus on creating a balanced, well-rounded trading perspective."""

# Strategy Backtesting Enhancement Prompt
STRATEGY_BACKTEST_PROMPT = """Enhanced backtesting analysis for trading strategies:

STRATEGY RULES: {strategy}
HISTORICAL DATA: {data_period}
PERFORMANCE METRICS: {metrics}
BENCHMARK: {benchmark}

Comprehensive backtesting analysis:
1. Strategy performance vs benchmark
2. Risk-adjusted returns (Sharpe, Sortino ratios)
3. Maximum drawdown analysis
4. Win/loss ratios and streaks
5. Performance across market conditions
6. Transaction costs impact
7. Strategy optimization suggestions

Provide backtesting analysis with the following JSON format:
{{
    "total_return": "Strategy total return %",
    "benchmark_return": "Benchmark return %",
    "sharpe_ratio": "Risk-adjusted return metric",
    "sortino_ratio": "Downside risk-adjusted return",
    "max_drawdown": "Maximum peak-to-trough decline",
    "win_rate": "Percentage of winning trades",
    "profit_factor": "Gross profit / Gross loss",
    "best_year": "Best performing year",
    "worst_year": "Worst performing year",
    "analysis": "Comprehensive strategy analysis",
    "suggested_action": "Strategy optimization recommendations",
    "confidence": 0.85,
    "risk_level": "Strategy risk assessment",
    "intention": "strategy_review",
    "amount": 0
}}

Focus on statistical significance and practical implementation insights."""

# Market Summary Quick Status Prompt
MARKET_SUMMARY_PROMPT = """Provide quick market snapshot for busy traders:

CURRENT DATA: {market_data}
KEY LEVELS: {support_resistance}
VOLUME: {volume_data}

Generate concise 3-line summary:
1. Current trend direction and strength
2. Key level to watch (support/resistance)
3. Suggested action with rationale

Provide market summary with the following JSON format:
{{
    "trend_direction": "Current market trend (Strong Bull/Bull/Neutral/Bear/Strong Bear)",
    "trend_strength": "Trend strength (1-10 scale)",
    "key_level": "Most important price level to watch",
    "volume_confirmation": "Volume supporting trend (Yes/No)",
    "market_phase": "Accumulation/Markup/Distribution/Decline",
    "analysis": "3-line market summary",
    "suggested_action": "Quick actionable recommendation",
    "confidence": 0.75,
    "risk_level": "Current market risk",
    "intention": "quick_summary",
    "amount": 0
}}

Keep it concise and immediately actionable for time-sensitive decisions."""

# Risk Warning Generation Prompt  
RISK_WARNING_PROMPT = """Generate appropriate risk warnings based on market conditions:

RISK FACTORS: {risk_factors}
ACCOUNT STATUS: {account_info}
MARKET CONDITIONS: {market_status}
POSITION SIZE: {position_size}

Assess risk levels:
1. Market volatility risk
2. Position concentration risk
3. Leverage risk (if applicable)
4. Liquidity risk
5. Regulatory risk
6. Technical risk

Provide risk warning with the following JSON format:
{{
    "risk_level": "Low/Medium/High/Extreme",
    "primary_risks": "Top 3 risk factors",
    "volatility_warning": "Volatility-specific warnings",
    "position_warning": "Position size warnings",
    "market_warning": "Market condition warnings",
    "mitigation_steps": "Risk mitigation recommendations",
    "analysis": "Comprehensive risk assessment",
    "suggested_action": "Risk management actions",
    "confidence": 1.0,
    "risk_level": "Overall risk rating",
    "intention": "risk_warning",
    "amount": 0
}}

Focus on protecting capital and promoting responsible trading."""

def get_market_analysis_prompt(user_query: str, market_data: str) -> str:
    """Get formatted market analysis prompt."""
    return MARKET_ANALYSIS_PROMPT.format(
        user_query=user_query,
        market_data=market_data
    )

def get_price_trend_prompt(price_data: str) -> str:
    """Get formatted price trend analysis prompt."""
    return PRICE_TREND_PROMPT.format(price_data=price_data)

def get_risk_assessment_prompt(market_data: str, trade_action: str, trade_amount: float) -> str:
    """Get formatted risk assessment prompt."""
    return RISK_ASSESSMENT_PROMPT.format(
        market_data=market_data,
        trade_action=trade_action,
        trade_amount=trade_amount
    )

def get_trading_decision_prompt(user_request: str, market_analysis: str, account_balance: str) -> str:
    """Get formatted trading decision prompt."""
    return TRADING_DECISION_PROMPT.format(
        user_request=user_request,
        market_analysis=market_analysis,
        account_balance=account_balance
    )

def get_volatile_market_prompt(market_data: str, volatility_info: str) -> str:
    """Get formatted volatile market prompt."""
    return VOLATILE_MARKET_PROMPT.format(
        market_data=market_data,
        volatility_info=volatility_info
    )

def get_portfolio_analysis_prompt(portfolio_data: str, market_data: str, user_query: str) -> str:
    """Get formatted portfolio analysis prompt."""
    return PORTFOLIO_ANALYSIS_PROMPT.format(
        portfolio_data=portfolio_data,
        market_data=market_data,
        user_query=user_query
    )

def get_error_recovery_prompt(error_info: str, available_data: str) -> str:
    """Get formatted error recovery prompt."""
    return ERROR_RECOVERY_PROMPT.format(
        error_info=error_info,
        available_data=available_data
    )

def get_btc_price_info_prompt(current_price: float, price_history: str) -> str:
    """Get formatted BTC price information prompt."""
    return BTC_PRICE_INFO_PROMPT.format(
        current_price=current_price,
        price_history=price_history
    )

def get_usdt_balance_info_prompt(usdt_balance: float, account_info: str) -> str:
    """Get formatted USDT balance information prompt."""
    return USDT_BALANCE_INFO_PROMPT.format(
        usdt_balance=usdt_balance,
        account_info=account_info
    )

def get_portfolio_value_prompt(btc_amount: float, btc_price: float, usdt_balance: float) -> str:
    """Get formatted portfolio value prompt."""
    btc_value_usdt = btc_amount * btc_price
    total_value = btc_value_usdt + usdt_balance
    
    return PORTFOLIO_VALUE_PROMPT.format(
        btc_amount=btc_amount,
        btc_price=btc_price,
        usdt_balance=usdt_balance,
        btc_value_usdt=btc_value_usdt,
        total_value=total_value
    )

def get_intent_selector_prompt(user_message: str) -> str:
    """Get formatted intent selector prompt."""
    return INTENT_SELECTOR_PROMPT.format(user_message=user_message)

def get_technical_analysis_prompt(price_data: str, indicators: str, user_query: str) -> str:
    """Get formatted technical analysis prompt."""
    return TECHNICAL_ANALYSIS_PROMPT.format(
        price_data=price_data,
        indicators=indicators,
        user_query=user_query
    )

def get_sentiment_analysis_prompt(social_sentiment: str, news_data: str, fear_greed_index: str, technical_data: str, user_query: str) -> str:
    """Get formatted sentiment analysis prompt."""
    return SENTIMENT_ANALYSIS_PROMPT.format(
        social_sentiment=social_sentiment,
        news_data=news_data,
        fear_greed_index=fear_greed_index,
        technical_data=technical_data,
        user_query=user_query
    )

def get_multi_timeframe_prompt(hourly_data: str, four_hour_data: str, daily_data: str, weekly_data: str, user_query: str) -> str:
    """Get formatted multi-timeframe analysis prompt."""
    return MULTI_TIMEFRAME_PROMPT.format(
        hourly_data=hourly_data,
        four_hour_data=four_hour_data,
        daily_data=daily_data,
        weekly_data=weekly_data,
        user_query=user_query
    )

def get_position_sizing_prompt(balance: float, risk_percentage: float, stop_distance: float, entry_price: float, account_type: str) -> str:
    """Get formatted position sizing prompt."""
    return POSITION_SIZING_PROMPT.format(
        balance=balance,
        risk_percentage=risk_percentage,
        stop_distance=stop_distance,
        entry_price=entry_price,
        account_type=account_type
    )

def get_correlation_analysis_prompt(holdings: str, new_position: str, correlation_data: str, portfolio_value: float) -> str:
    """Get formatted correlation analysis prompt."""
    return CORRELATION_ANALYSIS_PROMPT.format(
        holdings=holdings,
        new_position=new_position,
        correlation_data=correlation_data,
        portfolio_value=portfolio_value
    )

def get_price_alert_prompt(current_price: float, target_price: float, alert_type: str, market_data: str) -> str:
    """Get formatted price alert prompt."""
    return PRICE_ALERT_PROMPT.format(
        current_price=current_price,
        target_price=target_price,
        alert_type=alert_type,
        market_data=market_data
    )

def get_performance_analysis_prompt(trade_data: str, period: str, performance_metrics: str, user_query: str) -> str:
    """Get formatted performance analysis prompt."""
    return PERFORMANCE_ANALYSIS_PROMPT.format(
        trade_data=trade_data,
        period=period,
        performance_metrics=performance_metrics,
        user_query=user_query
    )

def get_educational_prompt(question: str, user_level: str, topic: str) -> str:
    """Get formatted educational prompt."""
    return EDUCATIONAL_PROMPT.format(
        question=question,
        user_level=user_level,
        topic=topic
    )

def get_dca_strategy_prompt(current_price: float, investment_amount: float, frequency: str, duration: str, market_data: str) -> str:
    """Get formatted DCA strategy prompt."""
    return DCA_STRATEGY_PROMPT.format(
        current_price=current_price,
        investment_amount=investment_amount,
        frequency=frequency,
        duration=duration,
        market_data=market_data
    )

def get_stop_loss_prompt(position: str, entry_price: float, current_price: float, balance: float, risk_tolerance: float) -> str:
    """Get formatted stop loss prompt."""
    return STOP_LOSS_PROMPT.format(
        position=position,
        entry_price=entry_price,
        current_price=current_price,
        balance=balance,
        risk_tolerance=risk_tolerance
    )

def get_consensus_analysis_prompt(technical_analysis: str, fundamental_analysis: str, sentiment_analysis: str, user_query: str) -> str:
    """Get formatted consensus analysis prompt."""
    return CONSENSUS_ANALYSIS_PROMPT.format(
        technical_analysis=technical_analysis,
        fundamental_analysis=fundamental_analysis,
        sentiment_analysis=sentiment_analysis,
        user_query=user_query
    )

def get_strategy_backtest_prompt(strategy: str, data_period: str, metrics: str, benchmark: str) -> str:
    """Get formatted strategy backtesting prompt."""
    return STRATEGY_BACKTEST_PROMPT.format(
        strategy=strategy,
        data_period=data_period,
        metrics=metrics,
        benchmark=benchmark
    )

def get_market_summary_prompt(market_data: str, support_resistance: str, volume_data: str) -> str:
    """Get formatted market summary prompt."""
    return MARKET_SUMMARY_PROMPT.format(
        market_data=market_data,
        support_resistance=support_resistance,
        volume_data=volume_data
    )

def get_risk_warning_prompt(risk_factors: str, account_info: str, market_status: str, position_size: float) -> str:
    """Get formatted risk warning prompt."""
    return RISK_WARNING_PROMPT.format(
        risk_factors=risk_factors,
        account_info=account_info,
        market_status=market_status,
        position_size=position_size
    )
