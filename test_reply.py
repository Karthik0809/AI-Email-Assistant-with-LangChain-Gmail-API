#!/usr/bin/env python3
"""
Test script for email reply generation
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.reply_agent import EmailReplyAgent
from config import Config

def test_reply_generation():
    """Test reply generation with different models"""
    
    print("🧪 Testing Email Reply Generation")
    print("=" * 50)
    
    # Test email content
    test_emails = [
        "Hi, can we schedule a meeting for next week?",
        "Thank you for your help with the project!",
        "I have a question about the new feature implementation.",
        "URGENT: Need your input on the client proposal ASAP!",
        "Could you help me with the task assignment?",
        "Just wanted to check in on the project status."
    ]
    
    # Test with template mode
    print("\n📝 Testing Template Mode:")
    template_agent = EmailReplyAgent(model_type="template")
    
    for i, email in enumerate(test_emails[:3], 1):
        print(f"\nTest {i}:")
        print(f"Input: {email}")
        reply = template_agent.generate_reply(email)
        print(f"Reply: {reply}")
        print("-" * 30)
    
    # Test with OpenAI mode if available
    if Config.OPENAI_API_KEY:
        print("\n🤖 Testing OpenAI Mode:")
        openai_agent = EmailReplyAgent(model_type="openai")
        
        for i, email in enumerate(test_emails[3:], 1):
            print(f"\nTest {i}:")
            print(f"Input: {email}")
            try:
                reply = openai_agent.generate_reply(email)
                print(f"Reply: {reply}")
            except Exception as e:
                print(f"Error: {e}")
                print("Falling back to template mode...")
                reply = template_agent.generate_reply(email)
                print(f"Template Reply: {reply}")
            print("-" * 30)
    else:
        print("\n⚠️ OpenAI API key not found. Skipping OpenAI tests.")
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    test_reply_generation() 