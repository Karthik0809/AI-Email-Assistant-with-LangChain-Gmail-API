
def detect_intent(email_text):
    email_text = email_text.lower()
    if "meeting" in email_text or "schedule" in email_text:
        return "schedule"
    elif "thank you" in email_text or "thanks" in email_text:
        return "gratitude"
    elif "complaint" in email_text or "issue" in email_text:
        return "complaint"
    elif "invoice" in email_text or "payment" in email_text:
        return "billing"
    elif "job" in email_text or "application" in email_text:
        return "job_inquiry"
    else:
        return "general"
