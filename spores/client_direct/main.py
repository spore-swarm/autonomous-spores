import asyncio
import sys
import threading

from spores.core.client import Client
from fastapi import FastAPI
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from fastapi import (APIRouter, Depends, Request)
from loguru import logger
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional


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
        def hello():
            return "Spores"

        @router.get("/agents")
        def list_agents():
            print(self.agents)

        @router.post("/agent/completions")
        def create_completion(request: CompletionRequest):
            runtime = self.agents[request.agent_id]
            response = runtime.process_completion(request.prompt)
            print(response)

        return router

    def start(self):
        port = os.getenv("SEVER_PORT", 8000)
        logger.info(f"Server running at http://localhost:{port}")
        uvicorn.run(self.app, port=port, log_level="error")

    def stop(self):
        logger.warning("Direct client does not support stopping")


class CompletionRequest(BaseModel):
    """Model for completion requests."""

    prompt: str = Field(..., description="The prompt to process")
    agent_id: str = Field(..., description="ID of the agent to use")
    max_tokens: Optional[int] = Field(
        None, description="Maximum tokens to generate"
    )
    temperature_override: Optional[float] = 0.5
    stream: bool = Field(
        default=False, description="Enable streaming response"
    )