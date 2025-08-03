import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Set up logging early
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from artemis.api.routes import chat
from artemis.config import settings

logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Artemis Personal Chatbot",
    description="A personal AI assistant powered by Claude 4 Sonnet",
    version="0.1.0",
)

# Attach limiter to app state (required by slowapi)
app.state.limiter = limiter

# Add rate limit error handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.pwills.com",
        "https://pwills.com",
        "https://peterewills.github.io",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-API-Key"],
)

# Decorate the chat endpoint with rate limiting
chat.chat = limiter.limit("25/minute")(chat.chat)

app.include_router(chat.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Artemis Personal Chatbot"}


@app.get("/health")
@limiter.limit("60/minute")
async def health(request: Request):
    return {"status": "healthy"}
