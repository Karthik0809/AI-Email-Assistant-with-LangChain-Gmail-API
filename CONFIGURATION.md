# Configuration Guide

## Environment Variables Setup

Create a `.env` file in your project root with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Alternative Models (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Agent Configuration
DEFAULT_MODEL_TYPE=openai
FALLBACK_ENABLED=true

# Retry Configuration
MAX_RETRIES=3
BASE_DELAY=1.0

# Email Configuration
DEFAULT_SENDER_NAME=Your Name
DEFAULT_SENDER_EMAIL=your.email@example.com

# Gmail Configuration (if using Gmail API)
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
```

## Handling OpenAI Rate Limits

### Option 1: Use Template-Based Replies (Recommended for now)
Set `DEFAULT_MODEL_TYPE=template` in your `.env` file to use template-based replies that don't require API calls.

### Option 2: Add Credits to OpenAI Account
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to Billing
3. Add payment method and credits

### Option 3: Use Alternative Models
Configure alternative API keys for other providers:
- Anthropic Claude
- Google Gemini
- Local models

### Option 4: Implement Rate Limiting
The system now includes automatic retry logic with exponential backoff to handle temporary rate limits.

## Quick Fix for Current Issue

To immediately resolve the rate limit error, run:

```bash
# Set environment variable to use template mode
export DEFAULT_MODEL_TYPE=template
```

Or modify your `.env` file:
```bash
DEFAULT_MODEL_TYPE=template
```

## Testing the Setup

Run the application to test:

```bash
python main.py
```

The system will automatically fall back to template-based replies if OpenAI is unavailable. 