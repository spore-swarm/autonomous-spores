from spores.core.runtime import AgentRuntime
from spores.client_twitter.data_source import DataSource
from spores.client_twitter.client import TwitterClient
from spores.client_twitter.interactions import InteractionClient

class TwitterManager:
    def __init__(self, runtime: AgentRuntime, data_source: DataSource):
        self.client = TwitterClient(runtime, data_source)    
        self.interaction = InteractionClient(self.client, runtime)

    async def start(self):          
        await self.client.init()
        await self.interaction.start()
        
    def stop(self):
        pass