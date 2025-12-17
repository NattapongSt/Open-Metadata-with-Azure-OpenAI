# Backend APIs (SSE Clients)

**Base URL:** `http://localhost:8010` (default)

## API Endpoints Overview

| Feature | Method | Endpoint | Description |
| :--- | :---: | :--- | :--- |
| **Check System Status** | `GET` | `/api/v1/health` | Verifies if the backend and MCP connection are active. |
| **Get Chat History** | `POST` | `/api/v1/get_history_conversations` | Retrieves past conversation logs based on session ID. |
| **Chat with AI** | `POST` | `/api/v1/chat` | Sends a prompt to the AI Agent (connected to OpenMetadata). |

---

## API Details

### 1. Check Backend Status
Used to verify service health.

- **URL:** `/api/v1/health`
- **Method:** `GET`
- **Response:**
    ```json
    {
        "status": "healthy",
        "mcp_connection": true
    }
    ```

### 2. Get History Conversations
Retrieve chat history for a specific session.

- **URL:** `/api/v1/get_history_conversations`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "session_id": "session-uuid"
    }
    ```
- **Response:**
    ```json
    {
        "history": [
            { 
                "type": "human", 
                "content": "Show me tables that can access" 
            },
            { 
                "type": "ai", 
                "content": "Here are the tables..." 
            }
        ]
    }
    ```

### 3. Chat Endpoint
The main endpoint to interact with the Agent.

- **URL:** `/api/v1/chat`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "session_id": "session-uuid",
        "prompt": "Find dataset related to finance in OpenMetadata"
    }
    ```
- **Response:**
    ```json
    {
        "history": [
            { 
                "type": "human", 
                "content": "Show me tables that can access" 
            },
            { 
                "type": "ai", 
                "content": "Here are the tables..." 
            },
            { 
                "type": "human", 
                "content": "Find dataset related to finance in OpenMetadata" 
            },
            { 
                "type": "ai", 
                "content": "I found 3 tables related to finance..." 
            }
        ]
    }
    ```