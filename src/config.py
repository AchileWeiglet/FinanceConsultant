"""
Configuration management for the trading bot.
Handles environment variables and security settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    """Configuration settings for the trading bot."""
    
    # Telegram settings
    telegram_bot_token: str
    telegram_chat_id: str
    
    # Binance settings
    binance_api_key: str
    binance_secret_key: str
    binance_testnet: bool = True
    
    # AI Provider settings
    ai_provider: str = "ollama"  # "ollama", "openai", or "gemini" - for intent classification (always ollama)
    analysis_ai_provider: str = "ollama"  # "ollama", "openai", or "gemini" - for trading analysis
    
    # Ollama settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2-vision:11b"
    
    # OpenAI settings
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    
    # Gemini settings
    gemini_api_key: str = ""
    gemini_model: str = "gemini-pro"
    
    # Trading settings
    default_trade_amount: float = 0.001
    price_analysis_days: int = 15
    enable_trading: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @field_validator('telegram_bot_token')
    @classmethod
    def validate_telegram_token(cls, v):
        # Allow dummy values for WhatsApp testing
        if not v or (v == "your_telegram_bot_token_here" and not v.startswith("dummy_")):
            raise ValueError("Telegram bot token must be set")
        return v
    
    @field_validator('binance_api_key', 'binance_secret_key')
    @classmethod
    def validate_binance_keys(cls, v):
        # Allow dummy values for WhatsApp testing
        if not v or (v.startswith("your_") and not v.startswith("dummy_")):
            raise ValueError("Binance API keys must be set")
        return v


def load_config() -> Config:
    """Load configuration from environment variables."""
    load_dotenv()
    
    # Create config with environment variables
    config_data = {
        'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
        'binance_api_key': os.getenv('BINANCE_API_KEY', ''),
        'binance_secret_key': os.getenv('BINANCE_SECRET_KEY', ''),
        'binance_testnet': os.getenv('BINANCE_TESTNET', 'true').lower() == 'true',
        'ai_provider': os.getenv('AI_PROVIDER', 'ollama'),
        'analysis_ai_provider': os.getenv('ANALYSIS_AI_PROVIDER', 'ollama'),
        'ollama_base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
        'ollama_model': os.getenv('OLLAMA_MODEL', 'llama3.2-vision:11b'),
        'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-4'),
        'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
        'gemini_model': os.getenv('GEMINI_MODEL', 'gemini-pro'),
        'default_trade_amount': float(os.getenv('DEFAULT_TRADE_AMOUNT', '0.001')),
        'price_analysis_days': int(os.getenv('PRICE_ANALYSIS_DAYS', '15')),
        'enable_trading': os.getenv('ENABLE_TRADING', 'false').lower() == 'true',
    }
    
    return Config(**config_data)


def get_binance_base_url(testnet: bool = True) -> str:
    """Get the appropriate Binance API base URL."""
    if testnet:
        return "https://testnet.binance.vision"
    return "https://api.binance.com"
