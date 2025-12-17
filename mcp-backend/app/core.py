import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.sse import sse_client

from .state import STATE
from .agent import build_agent_app
from .routes import router as chat_router 

load_dotenv()

async def lifespan(app: FastAPI):
    SSE_ENDPOINT = os.getenv("SSE_ENDPOINT")
    async with sse_client(SSE_ENDPOINT) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            STATE["session"] = session
            
            try:
                STATE["app"] = await build_agent_app(session)
                yield
            except Exception as e:
                print(f"Error during lifespan: {e}")
                raise e
            
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, tags=["openmetadata chat"])