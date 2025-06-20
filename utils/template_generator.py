"""
Generates context-aware template-based email replies locally.
"""

def generate_template_reply(email_text: str) -> str:
    """
    Analyzes the email content and returns a relevant template-based reply.
    """
    email_lower = email_text.lower()
    words = email_lower.split()

    # Priority 1: Job-related
    if any(word in email_lower for word in ['job application', 'apply', 'application', 'resume', 'cv', 'position', 'vacancy']):
        return """Thank you for considering my application.

I appreciate the opportunity to apply for this position. I look forward to hearing from you soon.

Best regards,"""
    elif any(word in email_lower for word in ['job meeting', 'interview', 'recruiter', 'hr', 'screening']):
        return """Thank you for reaching out about the job meeting.

I'm looking forward to our discussion. Please let me know if there are any materials I should prepare.

Best regards,"""

    # Priority 2: Document Sharing
    elif any(word in email_lower for word in ['attached', 'attachment', 'document', 'file', 'pdf', 'share']):
        return """Thank you for sharing the document.

I've received the file and will review it as soon as possible.

Best regards,"""

    # Priority 3: Scheduling
    elif any(word in email_lower for word in ['meeting', 'schedule', 'appointment', 'calendar', 'available']):
        return """Thank you for reaching out about scheduling.

I'd be happy to meet. Let me check my calendar and I'll get back to you with some available time slots.

Best regards,"""

    # Priority 4: Questions
    elif any(word in email_lower for word in ['question', 'help', 'support', 'assist', 'how', 'what', 'why']):
        return """Thank you for your question.

I'd be happy to help. Let me look into this and I'll provide you with a detailed response shortly.

Best regards,"""
        
    # Priority 5: Gratitude
    elif any(word in email_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']):
        return """You're very welcome!

I'm glad I could help. Please don't hesitate to reach out if you need anything else.

Best regards,"""

    # Priority 6: Personalized Messages
    elif any(word in email_lower for word in ['birthday', 'anniversary', 'congratulations', 'condolences']):
        if 'birthday' in email_lower:
            return """Thank you so much for your birthday wishes!

I truly appreciate your kind words.

Best regards,"""
        elif 'congratulations' in email_lower:
            return """Thank you so much for your congratulations!

I appreciate your support.

Best regards,"""
        else:
            return """Thank you for your kind message.

I appreciate your thoughtfulness.

Best regards,"""

    # Default Catch-all
    else:
        return """Thank you for your email.

I've received your message and will get back to you shortly.

Best regards,""" 