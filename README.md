# Krimi Backend

A robust backend API for a conversational AI chat application, built with FastAPI and integrated with Supabase for authentication and data persistence. The system leverages LangChain and LangGraph to power an intelligent AI assistant capable of handling tool-based interactions.

## Project Overview

Krimi Backend provides a scalable REST API for managing chat conversations with an AI assistant. It features user authentication via Supabase JWT tokens, persistent conversation storage, and an AI agent that can perform calculations and respond contextually using OpenAI's GPT-4o-mini model.

## Features

- **AI-Powered Chat**: Interactive conversations with a helpful AI assistant using LangChain and OpenAI
- **Tool Integration**: Built-in tools for mathematical operations (multiplication and division)
- **Conversation Management**: Create, retrieve, and manage chat sessions with persistent message history
- **Secure Authentication**: JWT-based authentication using Supabase Auth
- **Real-time Responses**: Asynchronous message handling for responsive user interactions
- **Health Monitoring**: Built-in health check endpoint for system monitoring

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **AI/ML**: LangChain, LangGraph, OpenAI GPT-4o-mini
- **Database**: Supabase (PostgreSQL with real-time capabilities)
- **Authentication**: Supabase Auth with JWT tokens
- **State Management**: LangGraph checkpointer with PostgreSQL
- **Dependencies**:
  - fastapi: Web framework
  - uvicorn: ASGI server
  - langchain-openai: OpenAI integration
  - supabase-py: Supabase client
  - python-jose: JWT handling
  - pydantic: Data validation

## Setup Instructions

### Prerequisites

- Python 3.12+
- Supabase account and project
- OpenAI API key

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd chatprac
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv chatprac
   source chatprac/bin/activate  # On Windows: chatprac\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (see Environment Variables section below)

5. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
SUPABASE_DATABASE_URL=your_supabase_database_connection_string

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

### Obtaining Supabase Credentials

1. Go to your Supabase project dashboard
2. Navigate to Settings > API
3. Copy the Project URL and anon/service_role keys
4. For JWT secret: Settings > API > JWT Secret
5. Database URL: Settings > Database > Connection string (use the one with password)

## API Usage

### Authentication

All API endpoints require authentication via Bearer token in the Authorization header:

```
Authorization: Bearer <your_supabase_jwt_token>
```

### Endpoints

#### Health Check

- **GET** `/health`
- Returns system status

#### Send Chat Message

- **POST** `/api/chat`
- **Request Body**:
  ```json
  {
    "conversation_id": "optional-existing-conversation-id",
    "message": "Your message here"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "conversation-id",
    "reply": "AI response",
    "title": "Conversation title (if new)"
  }
  ```

#### Get Conversation Messages

- **GET** `/api/conversations/{conversation_id}/messages`
- **Response**: Array of message objects
  ```json
  [
    {
      "id": "message-id",
      "role": "user|assistant",
      "content": "message content",
      "created_at": "timestamp"
    }
  ]
  ```

### Example Usage

```python
import requests

# Send a message
headers = {"Authorization": "Bearer your-jwt-token"}
data = {"message": "Hello, can you multiply 5 by 3?"}
response = requests.post("http://localhost:8000/api/chat", json=data, headers=headers)
print(response.json())
```

## Folder Structure

```
chatprac/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README_AGENT.md         # Agent-specific documentation
├── chatprac/               # Virtual environment
├── agent/
│   └── myagent.py          # LangGraph AI agent with tools
├── api/
│   ├── __init__.py
│   └── chat.py             # Chat API endpoints
├── core/
│   ├── __init__.py
│   ├── auth.py             # Authentication middleware
│   └── security.py         # JWT verification utilities
├── infra/
│   ├── chat_repository.py  # Database operations for chats
│   └── supabase_client.py  # Supabase client configuration
├── models/
│   ├── __init__.py
│   └── chat.py             # Pydantic models for requests/responses
└── services/
    ├── __init__.py
    └── chat_service.py     # Business logic for chat handling
```

## Notes for Contributors

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Use type hints for function parameters and return values
- Write descriptive commit messages
- Add docstrings to functions and classes
- Test API endpoints thoroughly

### Adding New Tools

To extend the AI agent's capabilities:

1. Define new tools in `agent/myagent.py` using the `@tool` decorator
2. Add tools to the `tools` list
3. Update the `tools_by_name` dictionary
4. Rebind the LLM with updated tools: `llm_with_tools = model.bind_tools(tools)`

### Database Schema

The application expects the following Supabase tables:

- `chat_sessions`: Stores conversation metadata
- `chat_messages`: Stores individual messages within conversations

Ensure your Supabase project has these tables configured with appropriate RLS policies.

### Security Considerations

- Never commit `.env` files or API keys
- Use environment variables for all sensitive configuration
- Implement proper error handling to avoid exposing sensitive information
- Regularly rotate API keys and database credentials

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Submit a pull request

For major changes, please open an issue first to discuss the proposed changes.
