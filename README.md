# Artemis - Personal AI Chatbot

Artemis is a personal AI assistant that provides information about Peter Wills, powered by Claude 3.5 Sonnet.

## Features

- FastAPI backend with streaming support
- LangChain integration for conversation management
- Anthropic Claude 3.5 Sonnet for intelligent responses
- Server-Sent Events (SSE) for real-time streaming
- Extensible tool system for future enhancements

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Set environment variables:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. Run the server:
```bash
poetry run python run.py
```

## Testing

### API Testing
Test the API endpoints:
```bash
poetry run python test_chat.py
```

### Command Line Interface
For interactive local testing:
```bash
poetry run python cli_chat.py
```

Available commands:
- `exit` or `quit` - End the conversation
- `clear` - Clear conversation history  
- `history` - Show conversation history
- `stream` - Toggle streaming mode on/off

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/chat` - Chat with Artemis (supports streaming)

## Deployment

The application is configured for easy deployment on Railway. Environment variables will be automatically picked up from the Railway environment.

## Development

Format code:
```bash
poetry run black .
```

Run tests:
```bash
poetry run pytest
```