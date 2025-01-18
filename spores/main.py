from dotenv import load_dotenv
import mysql.connector
from spores.client_direct.main import DirectClient
from spores.adapter_mysql.main import MysqlAdapter
import os
import json
from loguru import logger

from spores.core.runtime import AgentRuntime

load_dotenv(override=True)

def start_agents():
    direct_client = DirectClient()

    db = initialize_database()
    db.init()

    characters = load_characters()
    for character in characters:
        start_agent(character, direct_client, db)

    direct_client.start()

def load_characters():
    characters = []
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, "characters")
    
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                characters.append(data)

    return characters

def start_agent(character, direct_client, db):
    runtime = create_agent(character, db)
    direct_client.register_agent(runtime)

def create_agent(character, db):
    logger.info(f"Creating runtime for character {character['name']}")
    runtime = AgentRuntime(character, db)
    runtime.initialize()

    return runtime

def initialize_database():
    db = None

    db_adapter = os.getenv("DB_ADAPTER")
    match db_adapter:
        case "mysql":
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_name = os.getenv("DB_NAME")

            connection = mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name
            )
            db = MysqlAdapter(connection)
        case _:
            raise ValueError(f"Invalid database adapter: {db_adapter}")
        
    return db

if __name__ == "__main__":
    start_agents()

