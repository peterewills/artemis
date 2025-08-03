# Artemis Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                               GitHub Pages                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                          React Frontend                               │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │ HTTPS
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                              Railway Platform                              │
│                                                                            │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                          Artemis Process                              │ │
│  │                                                                       │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │                                                                  │ │ │
│  │  │                    LangChain Agent                               │ │ │
│  │  │                  (Chat Controller)                               │ │ │
│  │  │                                                                  │ │ │
│  │  └──────────┬──────────────┬──────────────┬─────────────────────────┘ │ │
│  │             │              │              │                           │ │
│  │             ▼              ▼              ▼                           │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                   │ │
│  │  │              │ │              │ │              │                   │ │
│  │  │ Resume Info  │ │   Research   │ │   Personal   │                   │ │
│  │  │    Tool      │ │  Deep Dive   │ │  Info Tool   │                   │ │
│  │  │              │ │    Tool      │ │              │                   │ │
│  │  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘                   │ │
│  │         │                │                │                           │ │
│  │         ▼                ▼                ▼                           │ │
│  │  ┌────────────────────────────────────────────────────┐               │ │
│  │  │                  Data Sources                      │               │ │
│  │  │  ┌─────────┐  ┌───────────────┐  ┌──────────────┐  │               │ │
│  │  │  │ Resume  │  │   Research    │  │   Personal   │  │               │ │
│  │  │  │  PDF    │  │ Papers (PDFs) │  │     Info     │  │               │ │
│  │  │  │         │  │  & Summaries  │  │    (JSON)    │  │               │ │
│  │  │  └─────────┘  └───────────────┘  └──────────────┘  │               │ │
│  │  └────────────────────────────────────────────────────┘               │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │                      FastAPI Server                             │  │ │
│  │  │                                                                 │  │ │
│  │  │  Endpoints:                                                     │  │ │
│  │  │  • GET  /                    (Health check)                     │  │ │
│  │  │  • POST /api/chat            (Chat endpoint)                    │  │ │
│  │  │  • GET  /api/chat/stream     (SSE streaming)                    │  │ │
│  │  │                                                                 │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

## Architecture Components

### Frontend Layer - GitHub Pages
- **Platform**: GitHub Pages (Static hosting)
- **Application**: React single-page application
- **Repository**: artemis-react-frontend
- **Communication**: HTTPS requests to Railway backend
- **Features**:
  - Chat interface with streaming support
  - Message history
  - Responsive design

### Backend Layer - Railway Platform
- **Deployment Platform**: Railway (Cloud PaaS)
- **Environment**: Production deployment
- **URL**: `https://artemis-production-9690.up.railway.app`
- **Auto-deployment**: Triggered on GitHub pushes

### Artemis Process Components

#### LangChain Agent (Chat Controller)
- **Role**: Central orchestrator for all chat interactions
- **Model**: Claude 3.5 Sonnet (Anthropic)
- **Responsibilities**:
  - Process incoming chat messages
  - Determine which tools to use based on query
  - Coordinate tool responses
  - Generate final response to user

#### Tools Layer
Three specialized tools that the agent can invoke:

1. **Resume Info Tool**
   - Extracts information from PDF resume
   - Provides professional experience, skills, education details
   - Uses PyPDF for text extraction

2. **Research Deep Dive Tool**
   - Returns research paper summaries
   - Focuses on Peter's academic publications
   - Emphasizes graph/network analysis research
   - No longer makes separate LLM calls

3. **Personal Info Tool**
   - Provides basic personal information
   - Sources data from JSON configuration
   - Simple key-value lookup

#### Data Sources
- **Resume PDF**: Professional resume document (`resources/resume.pdf`)
- **Research Papers**:
  - PDF files in `resources/research/`
  - Markdown summaries for each paper
- **Personal Info**: JSON configuration file

#### FastAPI Server
- **Framework**: FastAPI for high-performance async operations
- **Features**:
  - Server-Sent Events (SSE) for streaming responses
  - CORS support for cross-origin requests from GitHub Pages
  - Async request handling
  - JSON request/response handling

## Data Flow

1. **User Interaction** → React Frontend (GitHub Pages)
2. **HTTPS Request** → Railway Platform → FastAPI Server
3. **FastAPI** → LangChain Agent
4. **Agent** analyzes query and selects appropriate tools
5. **Tools** access their respective data sources
6. **Tools** return information to Agent
7. **Agent** synthesizes response using Claude 3.5 Sonnet
8. **Response** streams back: FastAPI → Railway → React Frontend
9. **Frontend** displays streaming response to user

## Key Design Decisions

- **Separation of Concerns**: Frontend and backend deployed separately
- **Static Frontend**: No server required for UI, reducing complexity
- **Tool-based Architecture**: Modular design for easy capability extension
- **Streaming Responses**: Better UX for long responses via SSE
- **CORS Configuration**: Enables cross-origin communication
- **No Database**: All data embedded in deployment as static files
