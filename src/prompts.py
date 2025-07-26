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

4. "market_analysis" - User wants detailed market analysis and trading suggestions
   Examples: "Should I buy?", "Market analysis", "Is it a good time to trade?", "BTC trend"

5. "risk_assessment" - User wants risk evaluation for a specific trade
   Examples: "Is it risky to buy now?", "Risk of selling", "How risky is this trade?"

6. "trading_decision" - User wants specific trading recommendations
   Examples: "Should I buy or sell?", "Give me trading advice", "What should I do?"

7. "volatile_market" - User mentions high volatility or market uncertainty
   Examples: "Market is crazy", "Too volatile", "Prices jumping around"

8. "portfolio_analysis" - User wants portfolio rebalancing suggestions
   Examples: "Should I rebalance?", "Portfolio allocation advice", "Optimize my holdings"

9. "general_consult" - General questions about crypto or system status
   Examples: "How does this work?", "System status", "Help", "What can you do?"

10. "error_recovery" - When unable to determine intent clearly
    Use this when the message is unclear or doesn't fit other categories

RESPONSE FORMAT (JSON only):
{{
    "intent": "one of the intents above",
    "confidence": 0.85,
    "reasoning": "Why you chose this intent",
    "suggested_prompt_function": "function name from prompts.py to use",
    "required_data": ["list", "of", "data", "needed"],
    "user_query_type": "information/analysis/trading/consultation"
}}

CLASSIFICATION RULES:
- If user asks about prices/values → "btc_price_info" or "portfolio_value"
- If user asks about balance/buying power → "usdt_balance_info" 
- If user asks "should I buy/sell" → "trading_decision"
- If user wants market analysis → "market_analysis"
- If user mentions risk/safety → "risk_assessment"
- If user mentions volatility/uncertainty → "volatile_market"
- If user wants portfolio advice → "portfolio_analysis"
- If unclear or general questions → "general_consult"
- If message is confusing → "error_recovery"

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
