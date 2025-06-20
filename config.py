import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the email reply helper"""
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    
    # Alternative: Direct OpenAI (if you prefer)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Agent Configuration
    USE_AI = os.getenv("USE_AI", "true").lower() == "true"
    FALLBACK_TO_TEMPLATES = os.getenv("FALLBACK_TO_TEMPLATES", "true").lower() == "true"
    USE_OPENROUTER = os.getenv("USE_OPENROUTER", "true").lower() == "true"
    
    @classmethod
    def validate_config(cls):
        """Validate the configuration"""
        if cls.USE_AI:
            if cls.USE_OPENROUTER and not cls.OPENROUTER_API_KEY:
                print("Warning: OpenRouter API key not found. Will use template-based replies.")
                return False
            elif not cls.USE_OPENROUTER and not cls.OPENAI_API_KEY:
                print("Warning: OpenAI API key not found. Will use template-based replies.")
                return False
        return True
    
    @classmethod
    def get_available_modes(cls):
        """Get list of available modes"""
        modes = ["template"]  # Always available
        modes.append("ai")  # Always show AI mode, even if API key is missing
        return modes
    
    @classmethod
    def get_available_models(cls):
        """Get list of available models for OpenRouter"""
        return [
            "openai/gpt-3.5-turbo",
            "openai/gpt-4",
            "openai/gpt-4-turbo",
            "anthropic/claude-3-haiku",
            "anthropic/claude-3-sonnet",
            "anthropic/claude-3-opus",
            "google/gemini-pro",
            "meta-llama/llama-2-13b-chat",
            "meta-llama/llama-2-70b-chat",
            "mistralai/mistral-7b-instruct",
            "mistralai/mixtral-8x7b-instruct"
        ] 