"""AI Service for chat functionality with OpenAI and Anthropic support"""
import os
import logging
from typing import List, Dict, Optional, Generator
from enum import Enum

logger = logging.getLogger(__name__)


class AIProvider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class AIService:
    """
    AI service for health economic modeling assistance.
    Supports both OpenAI and Anthropic APIs.
    """
    
    SYSTEM_PROMPT = """You are an expert health economics and outcomes research (HEOR) consultant with deep expertise in:
- Cost-effectiveness analysis (CEA)
- Cost-utility analysis (CUA)
- Budget impact analysis
- Decision tree modeling
- Markov cohort models
- Partitioned survival models (PSM)
- Probabilistic sensitivity analysis (PSA)
- Deterministic sensitivity analysis (DSA)
- ICER calculation and interpretation
- Quality-adjusted life years (QALYs)
- Willingness-to-pay thresholds

You help users build, validate, and interpret health economic models. You provide:
1. Methodological guidance
2. Parameter estimation help
3. Model structure recommendations
4. Results interpretation
5. Best practices for reporting

Be concise, accurate, and cite relevant guidelines (CHEERS, NICE, ISPOR) when appropriate.
"""
    
    def __init__(self, provider: str = None, api_key: str = None):
        """
        Initialize AI service with auto-fallback.
        Tries OpenAI first, falls back to Anthropic if OpenAI fails.
        
        Args:
            provider: 'openai' or 'anthropic'. If None, auto-detect with fallback.
            api_key: API key. If None, read from environment.
        """
        self.provider = None
        self.api_key = None
        self.client = None
        
        # Try to initialize with auto-fallback
        if provider:
            # User specified provider
            self.provider = AIProvider(provider.lower())
            self.api_key = api_key or self._get_api_key()
            if self.api_key:
                self._initialize_client()
        else:
            # Auto-detect with fallback: OpenAI -> Anthropic
            self._initialize_with_fallback()
    
    def _initialize_with_fallback(self):
        """Initialize with automatic fallback between providers"""
        # Try OpenAI first
        if os.getenv('OPENAI_API_KEY'):
            try:
                self.provider = AIProvider.OPENAI
                self.api_key = os.getenv('OPENAI_API_KEY')
                self._initialize_client()
                if self.client:
                    logger.info("AI service initialized with OpenAI")
                    return
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}, trying Anthropic...")
        
        # Fallback to Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            try:
                self.provider = AIProvider.ANTHROPIC
                self.api_key = os.getenv('ANTHROPIC_API_KEY')
                self._initialize_client()
                if self.client:
                    logger.info("AI service initialized with Anthropic (fallback)")
                    return
            except Exception as e:
                logger.warning(f"Anthropic initialization failed: {e}")
        
        logger.warning("No AI provider available - both OpenAI and Anthropic failed")
    
    def _determine_provider(self, provider: Optional[str]) -> AIProvider:
        """Determine which provider to use"""
        if provider:
            return AIProvider(provider.lower())
        
        # Auto-detect from environment
        if os.getenv('OPENAI_API_KEY'):
            return AIProvider.OPENAI
        elif os.getenv('ANTHROPIC_API_KEY'):
            return AIProvider.ANTHROPIC
        else:
            # Default to OpenAI
            return AIProvider.OPENAI
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment"""
        if self.provider == AIProvider.OPENAI:
            return os.getenv('OPENAI_API_KEY')
        elif self.provider == AIProvider.ANTHROPIC:
            return os.getenv('ANTHROPIC_API_KEY')
        return None
    
    def _initialize_client(self):
        """Initialize the appropriate client"""
        try:
            if self.provider == AIProvider.OPENAI:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized")
            elif self.provider == AIProvider.ANTHROPIC:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                logger.info("Anthropic client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider} client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None
    
    def chat(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Send a chat message and get a response.
        
        Args:
            message: User message
            conversation_history: Previous messages [{"role": "user/assistant", "content": "..."}]
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            AI response text
        """
        if not self.is_available():
            return "AI service is not configured. Please add your API key to environment variables."
        
        try:
            if self.provider == AIProvider.OPENAI:
                return self._chat_openai(message, conversation_history, temperature, max_tokens)
            elif self.provider == AIProvider.ANTHROPIC:
                return self._chat_anthropic(message, conversation_history, temperature, max_tokens)
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _chat_openai(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Chat using OpenAI API"""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def _chat_anthropic(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Chat using Anthropic API"""
        messages = []
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        response = self.client.messages.create(
            model=os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
            system=self.SYSTEM_PROMPT,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.content[0].text
    
    def stream_chat(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Generator[str, None, None]:
        """
        Stream chat response (for real-time UI updates).
        
        Yields:
            Chunks of response text
        """
        if not self.is_available():
            yield "AI service is not configured."
            return
        
        try:
            if self.provider == AIProvider.OPENAI:
                yield from self._stream_openai(message, conversation_history, temperature, max_tokens)
            elif self.provider == AIProvider.ANTHROPIC:
                yield from self._stream_anthropic(message, conversation_history, temperature, max_tokens)
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"Error: {str(e)}"
    
    def _stream_openai(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Generator[str, None, None]:
        """Stream using OpenAI API"""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        stream = self.client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def _stream_anthropic(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Generator[str, None, None]:
        """Stream using Anthropic API"""
        messages = []
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        with self.client.messages.stream(
            model=os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
            system=self.SYSTEM_PROMPT,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        ) as stream:
            for text in stream.text_stream:
                yield text


# Singleton instance
_ai_service = None


def get_ai_response(
    message: str,
    conversation_history: List[Dict[str, str]] = None,
    provider: str = None
) -> str:
    """
    Convenience function to get AI response.
    
    Args:
        message: User message
        conversation_history: Previous conversation
        provider: 'openai' or 'anthropic' (optional)
        
    Returns:
        AI response
    """
    global _ai_service
    
    if _ai_service is None or (provider and _ai_service.provider.value != provider):
        _ai_service = AIService(provider=provider)
    
    return _ai_service.chat(message, conversation_history)
