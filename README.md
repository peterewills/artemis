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

## Live API

Artemis is deployed on Railway and accessible at: https://artemis-production-9690.up.railway.app

### Example API Calls

#### Health Check
```bash
curl https://artemis-production-9690.up.railway.app/health
```

#### Chat (Non-streaming)
```bash
curl -X POST https://artemis-production-9690.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tell me about Peter Wills"}
    ],
    "stream": false
  }'
```

#### Chat (Streaming)
```bash
curl -X POST https://artemis-production-9690.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What are Peter'"'"'s technical skills?"}
    ],
    "stream": true
  }'
```

#### Chat with Calculator Tool
```bash
curl -X POST https://artemis-production-9690.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Can you calculate the square root of 256 for me?"}
    ],
    "stream": true
  }'
```

## Deployment

### Railway Deployment

Artemis is deployed on Railway, a modern platform for deploying web applications. Railway automatically builds and deploys the application from the GitHub repository.

#### How It Works

1. **Automatic Builds**: Railway detects the Python/Poetry project and uses Nixpacks to build the application
2. **GitHub Integration**: Pushes to the main branch trigger automatic deployments
3. **Environment Management**: Railway securely manages environment variables
4. **Health Monitoring**: Railway uses the `/health` endpoint to monitor application status

#### Configuration

1. **Required Environment Variables:**
   - `ANTHROPIC_API_KEY` - Your Anthropic API key

2. **Optional Environment Variables:**
   - `MODEL_NAME` - Claude model (default: claude-3-5-sonnet-20241022)
   - `MAX_TOKENS` - Response limit (default: 4096)
   - `TEMPERATURE` - Response creativity (default: 0.7)

3. **Railway Configuration (railway.json):**
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python run.py",
       "healthcheckPath": "/health"
     }
   }
   ```

4. **Automatic Features:**
   - PORT is automatically set by Railway
   - HTTPS is provided by default
   - Logs are available in the Railway dashboard
   - Automatic restarts on crashes

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