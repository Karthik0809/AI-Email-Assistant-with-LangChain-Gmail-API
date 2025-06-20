# Email Reply Helper

A smart, fast, and flexible Streamlit app that generates contextual email replies using AI (LangChain + OpenRouter), then opens them directly in your default email client.

## Features

- **🤖 AI-Powered Replies**: Uses LangChain with OpenRouter (multiple models)
- **🎯 Context-Aware**: Analyzes email content to generate relevant replies
- **🚀 One-Click Send**: Generates a "Send via Gmail" link that opens a pre-filled compose window
- **✏️ Editable Replies**: Edit generated replies directly in the app before sending
- **🎛️ Model Selection**: Choose from multiple AI models via OpenRouter
- **💰 Cost-Effective**: Very low cost per email (typically less than $0.001 per reply)

## How it Works

1. **Paste Email**: Copy the content of the email you received and paste it into the app
2. **Select Model**: Choose your preferred AI model in the sidebar
3. **Generate Reply**: Click "Generate AI Reply" to create a contextual response
4. **Edit & Send**: Review, edit if needed, and click "Send via Gmail" to open your email client

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd email_reply_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenRouter API key
   # Get your API key from: https://openrouter.ai/
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run main.py
```

The app will open in your web browser at `http://localhost:8501`

## Configuration

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and add your OpenRouter API key:
   ```bash
   # OpenRouter Configuration
   OPENROUTER_API_KEY=your_actual_api_key_here
   OPENROUTER_MODEL=openai/gpt-3.5-turbo
   USE_OPENROUTER=true
   USE_AI=true
   FALLBACK_TO_TEMPLATES=true
   ```

## Available AI Models (OpenRouter)

- **OpenAI Models**: gpt-3.5-turbo, gpt-4, gpt-4-turbo
- **Anthropic Models**: claude-3-haiku, claude-3-sonnet, claude-3-opus
- **Google Models**: gemini-pro
- **Meta Models**: llama-2-13b-chat, llama-2-70b-chat
- **Mistral Models**: mistral-7b-instruct, mixtral-8x7b-instruct

## Cost Information

The app uses OpenRouter API which charges per token used:

- **GPT-3.5-turbo**: ~$0.0015 per 1K tokens (cheapest)
- **GPT-4**: ~$0.03 per 1K tokens
- **Claude**: ~$0.008 per 1K tokens

**Typical costs:**
- Short email reply (~100 words): ~$0.0001-0.0003
- Medium email reply (~200 words): ~$0.0002-0.0006
- Long email reply (~500 words): ~$0.0005-0.0015

You'd need to generate hundreds of emails to spend even $1!

## Getting OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## Security

- **Your API key is private**: The `.env` file is excluded from git and won't be uploaded to GitHub
- **Template file**: Use `.env.example` as a template - it contains no real API keys
- **Never commit secrets**: Always use environment variables for sensitive data

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- OpenRouter API key

## Project Structure

```
email_reply_agent/
├── main.py                 # Streamlit app entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Template for environment variables
├── .env                  # Your actual environment variables (not in git)
└── utils/
    ├── ai_generator.py   # AI reply generation
    ├── reply_generator.py # Main reply orchestrator
    └── template_generator.py # Template system (fallback)
```

## License

MIT License 