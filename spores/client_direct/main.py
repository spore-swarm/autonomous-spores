import uvicorn
import os
import json
from spores.client_direct.template import MESSAGE_HANDLER_TEMPLATE
from spores.core.client import Client
from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
from typing import Optional
from spores.core.context import compose_context
from spores.core.parsing import MESSAGE_COMPLETION_FOOTER


class DirectClient(Client):
    def __init__(self):
        self.agents = {}
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "*"
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.include_router(self.create_api_router())

    def get_agents(self):
        return self.agents

    def register_agent(self, runtime):
        self.agents[runtime.agent.id] = runtime

    def create_api_router(self):
        router = APIRouter()

        @router.get("/")
        async def hello():
            return "Spores"

        @router.get("/agents")
        async def list_agents():
            agents = []
            for runtime in self.agents.values():
                agents.append({
                    "id": runtime.agent.agent_id,
                    "name": runtime.agent.name
                })

            return {"agents": agents}

        @router.get("/agents/{agent_id}")
        async def get_agent(agent_id):
            item = self.agents.get(agent_id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Agent {agent_id} not found",
                )

            return {
                "id": agent_id,
                "character": item.character
            }

        @router.post("/agents/{agent_id}/message")
        async def create_message(agent_id, request: CompletionRequest):
            runtime = self.agents.get(agent_id)
            if not runtime:
                raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail=f"Agent {agent_id} not found",
                )

            state = runtime.compose_state()
            context = compose_context(state, MESSAGE_HANDLER_TEMPLATE)
            runtime.agent.short_memory.update(0, "system", context)
            response = runtime.process_message(request.message)

            return json.loads(response)

        return router

    def start(self):
        port = os.getenv("SERVER_PORT", 8000)
        logger.info(f"Server running at http://localhost:{port}")
        uvicorn.run(self.app, port=port, log_level="error")

    def stop(self):
        logger.warning("Direct client does not support stopping")


class CompletionRequest(BaseModel):
    """Model for completion requests."""

    message: str = Field(..., description="The prompt to process")
    max_tokens: Optional[int] = Field(
        None, description="Maximum tokens to generate"
    )
    temperature_override: Optional[float] = 0.5
    stream: bool = Field(
        default=False, description="Enable streaming response"
    )
