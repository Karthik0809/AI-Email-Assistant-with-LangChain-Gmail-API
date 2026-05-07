"""
AI-powered email reply generation using LangChain with OpenRouter support.
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from config import Config

class AIGenerator:
    def __init__(self):
        self.llm = None
        self.setup_llm()
    
    def setup_llm(self, model_name=None):
        """Setup the LangChain LLM with OpenRouter or OpenAI"""
        try:
            model = model_name or Config.OPENROUTER_MODEL
            if Config.USE_OPENROUTER and Config.OPENROUTER_API_KEY:
                # Use OpenRouter
                self.llm = ChatOpenAI(
                    model=model,
                    temperature=0.7,
                    api_key=Config.OPENROUTER_API_KEY,
                    base_url=Config.OPENROUTER_BASE_URL,
                    default_headers={
                        "HTTP-Referer": "https://github.com/your-repo/email-reply-helper",
                        "X-Title": "Email Reply Helper"
                    }
                )
                print(f"✅ Using OpenRouter with model: {model}")
            elif Config.OPENAI_API_KEY:
                # Use direct OpenAI
                model = model_name or Config.OPENAI_MODEL
                self.llm = ChatOpenAI(
                    model=model,
                    temperature=0.7,
                    api_key=Config.OPENAI_API_KEY
                )
                print(f"✅ Using OpenAI with model: {model}")
            else:
                print("❌ No API key found for OpenRouter or OpenAI")
                self.llm = None
        except Exception as e:
            print(f"Error setting up AI model: {e}")
            self.llm = None
    
    def generate_ai_reply(self, email_text: str, model_name: str = None, tone: str = "Professional") -> str:
        """Generate an AI-powered reply using LangChain"""
        # Always re-setup if model_name is provided to ensure correct model is used
        if model_name:
            self.setup_llm(model_name)

        if not self.llm:
            return None
        
        try:
            # Create a system prompt for email reply generation
            system_prompt = f"""You are a professional email assistant. Your task is to generate polite, concise, and contextually appropriate email replies.
The desired tone for the reply is: {tone}.

Guidelines:
- Keep replies professional and courteous
- Match the requested tone: {tone}
- Match the formality of the original email where appropriate
- Be specific to the content and intent of the email
- Keep responses concise but complete
- End with "Best regards," (no name)
- If it's a thank you email, respond appropriately
- If it's about scheduling, offer to check availability
- If it's about documents, acknowledge receipt
- If it's a question, offer to help and follow up

Generate a natural, human-like response that feels personal and appropriate."""
            
            # Create the prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "Generate a reply to this email:\n\n{email_content}")
            ])
            
            # Generate the reply
            chain = prompt | self.llm
            response = chain.invoke({"email_content": email_text})
            
            return response.content.strip()
            
        except Exception as e:
            print(f"Error generating AI reply: {e}")
            return None
    
    def get_current_model(self) -> str:
        """Get the current model being used"""
        if Config.USE_OPENROUTER and Config.OPENROUTER_API_KEY:
            return f"OpenRouter: {Config.OPENROUTER_MODEL}"
        elif Config.OPENAI_API_KEY:
            return f"OpenAI: {Config.OPENAI_MODEL}"
        else:
            return "No AI model configured" 