# Open Metadata with Azure OpenAI (MCP Implementation)

This project implements a **Model Context Protocol (MCP)** connection between **OpenMetadata** and **Azure OpenAI**. It enables an AI agent to interact with metadata catalog using the MCP standard over SSE (Server-Sent Events) transport.

## Overview

The system consists of two main services running via Docker Compose:

1.  **MCP Server (`mcp-server-openmetadata`)**:
    - Based on [yangkyeongmo/mcp-server-openmetadata](https://github.com/yangkyeongmo/mcp-server-openmetadata.git).
    - Acts as the bridge to the OpenMetadata Rest API.
    - Exposes an SSE endpoint for clients to connect.

2.  **Backend Client (`mcp-backend`)**:
    - Acts as the **MCP Client**.
    - Connects to Azure OpenAI services.
    - Consumes the MCP Server's SSE stream to fetch metadata context for the AI.

## Project Structure

Ensure your directories are organized as follows so Docker can build the images correctly

```text
.
├── docker-compose.yml
├── .gitignore
├── README.md
├── mcp-server-openmetadata/    # Code for MCP Server
│   └── Dockerfile
└── mcp-backend/                # Code for Backend API
    └── Dockerfile
```

---

## Configuration

Before running, need to configure environment variables. You can set them in a `.env` file.

**Required Environment Variables**

**For MCP Server**
 - `OPENMETADATA_SERVER_URL`: URL of OpenMetadata instance.
 - `OPENMETADATA_JWT_TOKEN`: Bot token for authentication.

**For Backend Client**
 - `AZURE_OPENAI_API_KEY`: Azure OpenAI Key.
 - `AZURE_OPENAI_ENDPOINT`: Azure OpenAI Endpoint.
 - `AZURE_DEPLOYMENT_NAME`: The model deployment name.

**Database** Microsoft SQL Server
 - `DATABASE_HOST`: Database host
 - `DATABASE_NAME`: Database name
 - `DATABASE_USER`: username
 - `DATABASE_PASSWORD`: password
 - `DATABASE_HISTORY_TABLE`: Database table
---

## Installation & Running

1. **Build and Run with Docker Compose:** Use the following command to build the images locally and start the services.

    ```bash
        docker compose up
    ```

2. **Verify Status**
    - **MCP Server:** Should be running on port 8000 (internal).
    - **Backend Client:** Should be accessible at http://localhost:8010