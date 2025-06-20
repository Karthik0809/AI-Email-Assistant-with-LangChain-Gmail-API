"""
AI-powered email reply generator using OpenRouter.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_generator import AIGenerator
from config import Config

class ReplyGenerator:
    def __init__(self):
        self.ai_generator = AIGenerator()
        self.use_ai = Config.USE_AI and (Config.OPENROUTER_API_KEY or Config.OPENAI_API_KEY)
    
    def generate_reply(self, email_text: str, force_template: bool = False) -> tuple[str, str]:
        """
        Generate a reply using AI.
        Returns: (reply_text, mode_used)
        """
        if not email_text.strip():
            return "No email content provided.", "error"
        
        # Try AI if available
        if self.use_ai:
            try:
                ai_reply = self.ai_generator.generate_ai_reply(email_text)
                if ai_reply:
                    return ai_reply, "ai"
                else:
                    return "AI generation failed. Please check your API key and try again.", "error"
            except Exception as e:
                print(f"AI generation failed: {e}")
                return f"AI generation failed: {str(e)}", "error"
        
        return "AI is not available. Please check your configuration.", "error"
    
    def get_available_modes(self) -> list:
        """Get list of available generation modes"""
        modes = []
        if self.use_ai:
            modes.append("ai")
        return modes
    
    def is_ai_available(self) -> bool:
        """Check if AI generation is available"""
        return self.use_ai
    
    def get_ai_status(self) -> str:
        """Get detailed AI status information"""
        if Config.USE_OPENROUTER and Config.OPENROUTER_API_KEY:
            return f"✅ Using OpenRouter with model: {Config.OPENROUTER_MODEL}"
        elif Config.OPENAI_API_KEY:
            return f"✅ Using OpenAI with model: {Config.OPENAI_MODEL}"
        else:
            return "❌ No API key configured" 