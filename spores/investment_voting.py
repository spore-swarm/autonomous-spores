from spores.core.runtime import AgentRuntime
from dotenv import load_dotenv
from swarms.structs.majority_voting import MajorityVoting
from swarms import Agent as SwarmsAgent
import os
import json
import requests

load_dotenv()

class APIAgent(SwarmsAgent):
    def run(self, task: str) -> str:
        response = requests.get(os.getenv("REMOTE_SAYA_API"), params={"q": task})
        return response.text


def load_character(character_name):
    filepath = os.path.join("../characters", f"{character_name}.character.json")
    with open(filepath, "r", encoding="utf-8") as f:
        character = json.load(f)

    return character

def create_agent(character):
   runtime = AgentRuntime(character)
   runtime.initialize()
   return runtime.agent

def start():
    saya = create_agent(load_character("saya"))
    curious_saya = create_agent(load_character("curious_saya"))
    remote_saya = APIAgent(agent_name="remote_saya")

    majority_voting = MajorityVoting(agents=[saya, curious_saya, remote_saya])
    result = majority_voting.run("Which token is for the next round of investment?")
    print(result)

if __name__ == "__main__":
    start()

