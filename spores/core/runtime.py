import uuid
import random
from importlib import import_module
from unique_names_generator.data import NAMES
from spores.core.context import add_header
from spores.core.prompt import tool_prompt
from spores.core.agent import Agent
from swarms_memory import ChromaDB
from unique_names_generator import get_random_name
from loguru import logger
from spores.core.database import DatabaseAdapter
from spores.core.utils import string_to_uuid

class AgentRuntime:
    agent: Agent
    character: None
    db_adapter: DatabaseAdapter

    def __init__(self, character, db_adapter, cache_manager):
        self.character = character
        self.db_adapter = db_adapter
        self.cache_manager = cache_manager

    def initialize(self):
        memory = ChromaDB(
            metric="cosine",
            output_dir=self.character.get('name', 'agent'),
        )

        tools = []
        if len(self.character.get('plugins', [])) > 0:
            for plugin in self.character['plugins']:
                try:
                    module = import_module(f"spores.{plugin}.main")
                except ImportError:
                    logger.error(f"Plugin {plugin} not found")
                    continue
                plugin_class = getattr(module, plugin)
                tools += plugin_class.get("actions")

        agent_id = string_to_uuid(self.character.get('name', 'agent'))
        agent = Agent(
            id=agent_id,
            agent_id=agent_id,
            agent_name=self.character.get('name', 'agent'),
            system_prompt=self.character.get('system', ''),
            model_name=self.character.get('model', 'gpt-4o'),
            max_loops=1,
            dashboard=False,
            tools=tools,
            output_type="str",
            interactive=False,
            long_term_memory=memory,
            auto_generate_prompt=False,
            dynamic_temperature_enabled=True,
            tool_system_prompt=tool_prompt(),
            db = self.db_adapter
        )

        self.agent = agent

    def process_message(self, user_id:str, room_id:str, message: str):        
        response = self.agent.run(message, user_id=user_id, room_id=room_id)
        return response

    def compose_state(self, additional_keys: dict[str, str] = {}):
        state = {
            'agent_name': self.character['name'],
            'lore': self.process_lore(),
            'bio': self.process_bio(),
            'topic': self.process_topic(),
            'topics': self.process_topics(),
            'message_directions': self.process_message_directions(),
            'post_directions': self.process_post_directions()
        }
        state.update(additional_keys)
        return state

    def process_lore(self):
        lore = ""

        if self.character['lore'] and len(self.character['lore']) > 0:
            shuffled_lore = self.character['lore'][:]
            random.shuffle(shuffled_lore)
            selected_lore = shuffled_lore[:10]
            lore = "\n".join(selected_lore)

        return lore

    def process_posts(self):
        shuffled_posts = self.character['postExamples'][:]
        random.shuffle(shuffled_posts)
        selected_posts = shuffled_posts[:50]
        formatter_posts = "\n".join(str(post) for post in selected_posts)

        return formatter_posts

    def process_messages_examples(self):
        shuffled_message_examples = self.character['messageExamples'][:]
        random.shuffle(shuffled_message_examples)
        selected_message_examples = shuffled_message_examples[:5]

        formatted_examples = []
        for message_example in selected_message_examples:
            example_names = [get_random_name(combo=[NAMES]) for _ in range(5)]
            formatted_messages = []
            for message in message_example:
                message_string = f"{message['user']}: {message['content']['text']}"
                for index, name in enumerate(example_names):
                    placeholder = f"{{{{user{index + 1}}}}}"
                    message_string = message_string.replace(placeholder, name)
                formatted_messages.append(message_string)
            formatted_examples.append("\n".join(formatted_messages))

        formatted_message_examples = "\n\n".join(formatted_examples)
        return formatted_message_examples

    def process_bio(self):
        bio = ''
        if self.character['bio'] and len(self.character['bio']) > 0:
            shuffled_bio = self.character['bio'][:]
            random.shuffle(shuffled_bio)
            selected_bio = shuffled_bio[:3]
            bio = "\n".join(selected_bio)

        return bio

    def process_adjective(self):
        if self.character['adjectives'] and len(self.character['adjectives']) > 0:
            return random.choice(self.character['adjectives'])

        return ""

    def process_topic(self):
        if self.character['topics'] and len(self.character['topics']) > 0:
            return random.choice(self.character['topics'])
        return None

    def process_topics(self):
        if self.character['topics'] and len(self.character['topics']) > 0:
            shuffled_topics = random.sample(self.character['topics'], len(self.character['topics']))
            selected_topics = shuffled_topics[:5]

            formatted_topics = []
            for index, topic in enumerate(selected_topics):
                if index == len(selected_topics) - 2:
                    formatted_topics.append(f"{topic} and ")
                elif index == len(selected_topics) - 1:
                    formatted_topics.append(topic)
                else:
                    formatted_topics.append(f"{topic}, ")

            return f"{self.character['name']} is interested in " + "".join(formatted_topics)

        return ""

    def process_message_directions(self):
        all_styles = self.character['style'].get("all", [])
        chat_styles = self.character['style'].get("chat", [])
        if len(all_styles) > 0 or len(chat_styles) > 0:
            combined_styles = "\n".join(all_styles + chat_styles)
            return add_header(f"# Message Directions for {self.character['name']}", combined_styles)

        return ""

    def process_post_directions(self):
        all_styles = self.character['style'].get("all", [])
        post_styles = self.character['style'].get("post", [])
        if len(all_styles) > 0 or len(post_styles) > 0:
            combined_styles = "\n".join(all_styles + post_styles)
            return add_header(f"# Post Directions for {self.character['name']}", combined_styles)

        return ""