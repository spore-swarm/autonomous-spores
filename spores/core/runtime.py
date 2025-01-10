import uuid
import random

from unique_names_generator.data import NAMES

from spores.core.context import add_header
from swarms.structs.agent import Agent
from swarms_memory import ChromaDB
from unique_names_generator import get_random_name


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
            system_prompt=self.character.get('system', ''),
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

    def compose_state(self):
        return {
            'agent_name': self.character['name'],
            'lore': self.process_lore(),
            'bio': self.process_bio(),
            'topic': self.process_topic(),
            'topics': self.process_topics(),
            'message_directions': self.process_message_directions()
        }

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
            return add_header(f"# Post Directions for {self.character.name}", combined_styles)

        return ""
