"""
Unified email reply generator that combines AI and template approaches.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.template_generator import generate_template_reply
from utils.ai_generator import AIGenerator
from config import Config

class ReplyGenerator:
    def __init__(self):
        self.ai_generator = AIGenerator()
        self.use_ai = Config.USE_AI and (Config.OPENROUTER_API_KEY or Config.OPENAI_API_KEY)
        self.fallback_to_templates = Config.FALLBACK_TO_TEMPLATES
    
    def generate_reply(self, email_text: str, force_template: bool = False) -> tuple[str, str]:
        """
        Generate a reply using AI or templates.
        Returns: (reply_text, mode_used)
        """
        if not email_text.strip():
            return "No email content provided.", "error"
        
        # Force template mode if requested
        if force_template:
            reply = generate_template_reply(email_text)
            return reply, "template"
        
        # Try AI first if available and enabled
        if self.use_ai and not force_template:
            try:
                ai_reply = self.ai_generator.generate_ai_reply(email_text)
                if ai_reply:
                    return ai_reply, "ai"
                else:
                    # AI failed, fallback to template
                    if self.fallback_to_templates:
                        template_reply = generate_template_reply(email_text)
                        return f"AI generation failed. Using template reply:\n\n{template_reply}", "template"
                    else:
                        return "AI generation failed and fallback is disabled.", "error"
            except Exception as e:
                print(f"AI generation failed: {e}")
                if self.fallback_to_templates:
                    template_reply = generate_template_reply(email_text)
                    return f"AI generation failed. Using template reply:\n\n{template_reply}", "template"
                else:
                    return f"AI generation failed: {str(e)}", "error"
        
        # Fallback to templates
        if self.fallback_to_templates:
            template_reply = generate_template_reply(email_text)
            return template_reply, "template"
        
        return "Unable to generate reply.", "error"
    
    def get_available_modes(self) -> list:
        """Get list of available generation modes"""
        modes = ["template"]
        if self.use_ai:
            modes.append("ai")
        return modes
    
    def is_ai_available(self) -> bool:
        """Check if AI generation is available"""
        return self.use_ai
    
    def get_ai_status(self) -> str:
        """Get detailed AI status information"""
        if Config.USE_OPENROUTER and Config.OPENROUTER_API_KEY:
            return f"✅ OpenRouter: {Config.OPENROUTER_MODEL}"
        elif Config.OPENAI_API_KEY:
            return f"✅ OpenAI: {Config.OPENAI_MODEL}"
        else:
            return "❌ No API key configured" 