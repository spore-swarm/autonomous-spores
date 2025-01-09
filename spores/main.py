import asyncio

from dotenv import load_dotenv
from spores.client_direct.main import DirectClient
import sys
import os
import json
from loguru import logger

from spores.core.runtime import AgentRuntime

load_dotenv()

def start_agents():
    direct_client = DirectClient()

    characters = load_characters()
    for character in characters:
        start_agent(character, direct_client)

    direct_client.start()

def load_characters():
    characters = []

    directory = "../characters"
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                characters.append(data)

    return characters

def start_agent(character, direct_client):
    runtime = create_agent(character)
    direct_client.register_agent(runtime)

def create_agent(character):
    logger.info(f"Creating runtime for character {character['name']}")
    runtime = AgentRuntime(character)
    runtime.initialize()

    return runtime

if __name__ == "__main__":
    start_agents()

