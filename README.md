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

### Railway Deployment

1. **Required Environment Variables:**
   - `ANTHROPIC_API_KEY` - Your Anthropic API key

2. **Optional Environment Variables:**
   - `MODEL_NAME` - Claude model (default: claude-3-5-sonnet-20241022)
   - `MAX_TOKENS` - Response limit (default: 4096)
   - `TEMPERATURE` - Response creativity (default: 0.7)

3. **Railway Configuration:**
   - PORT is automatically set by Railway
   - Logs are stored in the `/logs` directory
   - Health check available at `/health`

### Logging

The application creates structured JSON logs for all conversations:

- **Format**: JSONL (JSON Lines) for easy parsing
- **Location**: `logs/conversations_YYYY-MM-DD.jsonl`
- **Daily Rotation**: New file each day
- **Content**: User messages, assistant responses, tool usage, errors

**View logs:**
```bash
poetry run python view_logs.py                    # Today's logs
poetry run python view_logs.py logs/file.jsonl    # Specific file
```

**Log entry types:**
- `conversation` - Complete conversation (non-streaming)
- `user_message` / `assistant_response` - Streaming conversations
- `tool_usage` - Future tool usage tracking
- `error` - Error logging with context

## Development

Format code:
```bash
poetry run black .
```

Run tests:
```bash
poetry run pytest
```