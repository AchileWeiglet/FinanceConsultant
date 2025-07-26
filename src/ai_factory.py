"""
AI Factory module.
Creates the appropriate AI handler based on configuration.
"""

import logging
from typing import Union
from .config import Config
from .ollama_handler import OllamaHandler
from .openai_handler import OpenAIHandler
from .gemini_handler import GeminiHandler

logger = logging.getLogger(__name__)

# Type alias for AI handlers
AIHandler = Union[OllamaHandler, OpenAIHandler, GeminiHandler]


class AIFactory:
    """Factory class to create AI handlers based on configuration."""
    
    @staticmethod
    def create_handler(config: Config) -> AIHandler:
        """
        Create the appropriate AI handler based on configuration.
        This is for intent classification (always uses ai_provider, should be ollama).
        
        Args:
            config: Configuration object
            
        Returns:
            AI handler instance for intent classification
            
        Raises:
            ValueError: If AI provider is not supported
        """
        provider = config.ai_provider.lower()
        
        if provider == "ollama":
            logger.info(f"Creating Ollama handler for intent classification with model: {config.ollama_model}")
            return OllamaHandler(config)
        
        elif provider == "openai":
            if not config.openai_api_key:
                raise ValueError("OpenAI API key is required when using OpenAI provider")
            logger.info(f"Creating OpenAI handler for intent classification with model: {config.openai_model}")
            return OpenAIHandler(config)
        
        elif provider == "gemini":
            if not config.gemini_api_key:
                raise ValueError("Gemini API key is required when using Gemini provider")
            logger.info(f"Creating Gemini handler for intent classification with model: {config.gemini_model}")
            return GeminiHandler(config)
        
        else:
            raise ValueError(f"Unsupported AI provider: {provider}. "
                           "Supported providers: ollama, openai, gemini")
    
    @staticmethod
    def create_analysis_handler(config: Config) -> AIHandler:
        """
        Create the appropriate AI handler for trading analysis based on analysis_ai_provider.
        This allows using different models for analysis vs intent classification.
        
        Args:
            config: Configuration object
            
        Returns:
            AI handler instance for trading analysis
            
        Raises:
            ValueError: If analysis AI provider is not supported
        """
        provider = config.analysis_ai_provider.lower()
        
        if provider == "ollama":
            logger.info(f"Creating Ollama handler for analysis with model: {config.ollama_model}")
            return OllamaHandler(config)
        
        elif provider == "openai":
            if not config.openai_api_key:
                raise ValueError("OpenAI API key is required when using OpenAI analysis provider")
            logger.info(f"Creating OpenAI handler for analysis with model: {config.openai_model}")
            return OpenAIHandler(config)
        
        elif provider == "gemini":
            if not config.gemini_api_key:
                raise ValueError("Gemini API key is required when using Gemini analysis provider")
            logger.info(f"Creating Gemini handler for analysis with model: {config.gemini_model}")
            return GeminiHandler(config)
        
        else:
            raise ValueError(f"Unsupported analysis AI provider: {provider}. "
                           "Supported providers: ollama, openai, gemini")
    
    @staticmethod
    def get_available_providers() -> list[str]:
        """Get list of available AI providers."""
        return ["ollama", "openai", "gemini"]
    
    @staticmethod
    async def test_provider_health(config: Config) -> dict[str, bool]:
        """
        Test health of all configured AI providers.
        
        Args:
            config: Configuration object
            
        Returns:
            Dictionary mapping provider names to health status
        """
        results = {}
        
        # Test Ollama
        try:
            ollama_handler = OllamaHandler(config)
            results["ollama"] = await ollama_handler.health_check()
        except Exception as e:
            logger.error(f"Error testing Ollama: {e}")
            results["ollama"] = False
        
        # Test OpenAI (only if API key is configured)
        if config.openai_api_key and not config.openai_api_key.startswith("your_"):
            try:
                openai_handler = OpenAIHandler(config)
                results["openai"] = await openai_handler.health_check()
            except Exception as e:
                logger.error(f"Error testing OpenAI: {e}")
                results["openai"] = False
        else:
            results["openai"] = False  # Not configured
        
        # Test Gemini (only if API key is configured)
        if config.gemini_api_key and not config.gemini_api_key.startswith("your_"):
            try:
                gemini_handler = GeminiHandler(config)
                results["gemini"] = await gemini_handler.health_check()
            except Exception as e:
                logger.error(f"Error testing Gemini: {e}")
                results["gemini"] = False
        else:
            results["gemini"] = False  # Not configured
        
        return results
