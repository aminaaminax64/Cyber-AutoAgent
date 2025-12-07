"""
Configuration file for the Advanced AI Model Switching System
"""

# Default Google Gemini models
DEFAULT_GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro", 
    "gemini-1.0-pro"
]

# Default OpenRouter models
DEFAULT_OPENROUTER_MODELS = [
    "openai/gpt-4o",
    "openai/gpt-4o-mini", 
    "anthropic/claude-3.5-sonnet",
    "google/gemini-pro-vision",
    "mistralai/mistral-7b-instruct",
    "perplexity/pplx-7b-chat",
    "cohere/command-r-plus"
]

# API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Request settings
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TIMEOUT = 30

# Performance monitoring settings
MAX_RESPONSE_TIMES_TO_TRACK = 50  # Only keep the last 50 response times for each model

# Fallback settings
FALLBACK_ATTEMPTS = 3  # Number of fallback attempts before giving up

# Model selection settings
MIN_REQUESTS_FOR_SELECTION = 3  # Minimum requests before considering response time in model selection