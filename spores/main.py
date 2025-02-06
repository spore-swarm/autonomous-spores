from dotenv import load_dotenv
from spores.client_direct.main import DirectClient
from spores.adapter_mysql.main import MysqlAdapter
import os
import json
from loguru import logger
from mysql.connector import pooling
from spores.client_twitter.manager import TwitterManager
from spores.core.runtime import AgentRuntime
import asyncio
from spores.client_twitter.data_source_mock import MockDataSource
from spores.core.utils import string_to_uuid
from spores.core.cache import DbCacheAdapter
from spores.core.cache import CacheManager


load_dotenv(override=True)

async def start_agents():
    direct_client = DirectClient()

    db_adapter = initialize_database()
    db_adapter.init()

    characters = load_characters()
    for character in characters:
        start_agent(character, direct_client, db_adapter)

    await direct_client.start()

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

def start_agent(character, direct_client, db_adapter):
    runtime = create_agent(character, db_adapter)

    initialize_clients(runtime)

    direct_client.register_agent(runtime)

def create_agent(character, db_adapter):
    logger.info(f"Creating runtime for character {character['name']}")
    
    cache_adapter = intialize_db_cache(character, db_adapter)

    runtime = AgentRuntime(character, db_adapter, CacheManager(cache_adapter))
    runtime.initialize()

    return runtime

def initialize_database():
    db_adapter = None

    db_adapter_str = os.getenv("DB_ADAPTER")
    match db_adapter_str:
        case "mysql":
            db_config = {
                "host": os.getenv("DB_HOST"),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
            }    

            pool_config = {
                "pool_name": "mysql_pool",
                "pool_size": 5,
                "pool_reset_session": True,
                **db_config
            }        

            connection_pool = pooling.MySQLConnectionPool(**pool_config)
            
            db_adapter = MysqlAdapter(connection_pool)
        case _:
            raise ValueError(f"Invalid database adapter: {db_adapter}")
        
    return db_adapter

def initialize_clients(runtime: AgentRuntime):
    clients = []

    if len(runtime.character.get('clients', [])) == 0:
        return clients
    
    if  "twitter" in runtime.character['clients']:
        twitter_client = TwitterManager(runtime, MockDataSource())
        asyncio.create_task(twitter_client.start())
        clients.append(twitter_client)

    return clients

def intialize_db_cache(character, db_adapter):
    agent_id = string_to_uuid(character.get('name', 'agent'))

    db_cache_adapter = DbCacheAdapter(db_adapter, agent_id)

    return db_cache_adapter


if __name__ == "__main__":
    asyncio.run(start_agents())
