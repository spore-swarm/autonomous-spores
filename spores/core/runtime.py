import uuid
from swarms.structs.agent import Agent
from swarms_memory import ChromaDB

class AgentRuntime:
    agent: Agent
    character: None

    def __init__(self, character):
        self.character = character

    def initialize(self):
        memory = ChromaDB(
            metric="cosine",
            output_dir=self.character.get('name', 'agent'),
        )

        agent_id = str(
            uuid.uuid3(uuid.UUID("12345678-1234-5678-1234-567812345678"), self.character.get('name', 'agent')))
        agent = Agent(
            id=agent_id,
            agent_id=agent_id,
            agent_name=self.character.get('name', 'agent'),
            system_prompt=self.character['system'],
            model_name=self.character['model'],
            max_loops=1,
            dashboard=False,
            output_type="str",
            interactive=False,
            autosave=True,
            long_term_memory=memory,
            dynamic_temperature_enabled=True,
        )

        self.agent = agent

    def process_completion(self, prompt: str):
        response = self.agent.run(prompt)

        return response
