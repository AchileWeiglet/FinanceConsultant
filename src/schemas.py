"""
JSON schemas for structured LLM communication.
Defines the expected format for Ollama responses.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class TradingAnalysis(BaseModel):
    """Schema for Ollama's trading analysis response."""
    
    intention: Literal["buy", "sell", "consult", "nothing"] = Field(
        description="The recommended action based on analysis"
    )
    analysis: str = Field(
        description="Detailed analysis of the current market situation"
    )
    suggested_action: str = Field(
        description="Human-readable suggestion for the user"
    )
    endpoint: Optional[str] = Field(
        default=None,
        description="Binance API endpoint to use (if applicable)"
    )
    amount: Optional[float] = Field(
        default=None,
        description="Suggested trade amount in BTC"
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence level of the analysis (0-1)"
    )
    risk_level: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Risk assessment of the suggested action"
    )


class UserMessage(BaseModel):
    """Schema for incoming user messages."""
    
    text: str = Field(description="The user's message text")
    user_id: str = Field(description="Telegram user ID")
    timestamp: str = Field(description="Message timestamp")


class BotResponse(BaseModel):
    """Schema for bot responses to users."""
    
    message: str = Field(description="Response message to send to user")
    show_confirmation: bool = Field(
        default=False,
        description="Whether to show trade confirmation buttons"
    )
    trade_data: Optional[TradingAnalysis] = Field(
        default=None,
        description="Trade data if confirmation is needed"
    )


class IntentClassification(BaseModel):
    """Schema for intent classification response."""
    
    intent: Literal[
        "btc_price_info", 
        "usdt_balance_info", 
        "portfolio_value", 
        "market_analysis", 
        "risk_assessment", 
        "trading_decision", 
        "volatile_market", 
        "portfolio_analysis", 
        "general_consult", 
        "error_recovery",
        "price_alerts",
        "trade_history",
        "technical_analysis",
        "news_sentiment",
        "stop_loss_management",
        "dca_strategy",
        "multi_timeframe",
        "educational_mode"
    ] = Field(description="Classified intent category")
    
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence level of the classification (0-1)"
    )
    
    reasoning: str = Field(
        description="Explanation of why this intent was chosen"
    )
    
    suggested_prompt_function: str = Field(
        description="Function name from prompts.py to use"
    )
    
    required_data: list[str] = Field(
        description="List of data needed to execute this intent"
    )
    
    user_query_type: Literal["information", "analysis", "trading", "consultation"] = Field(
        description="Type of user query"
    )
    
    premium_ai_requested: bool = Field(
        default=False,
        description="Whether user requested premium AI analysis"
    )
    
    requested_ai_provider: Literal["none", "openai", "gemini"] = Field(
        default="none",
        description="Specific AI provider requested by user"
    )
    
    comparison_analysis: bool = Field(
        default=False,
        description="Whether user wants comparison between multiple AI providers"
    )


class ComparisonAnalysis(BaseModel):
    """Schema for side-by-side AI comparison analysis."""
    
    ollama_analysis: TradingAnalysis = Field(
        description="Analysis from Ollama (free, default)"
    )
    
    premium_analysis: TradingAnalysis = Field(
        description="Analysis from premium AI (OpenAI/Gemini)"
    )
    
    premium_provider: Literal["openai", "gemini"] = Field(
        description="Which premium AI provider was used"
    )
    
    comparison_summary: str = Field(
        description="Summary comparing both analyses"
    )
    
    recommended_choice: Literal["ollama", "premium", "both_agree", "conflicting"] = Field(
        description="Which analysis is more reliable or if they agree/conflict"
    )
    
    cost_notice: str = Field(
        description="Notice about premium AI usage costs"
    )
