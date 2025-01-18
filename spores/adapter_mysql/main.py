from spores.core.database import DatabaseAdapter
from spores.adapter_mysql.tables import mysql_tables

class MysqlAdapter(DatabaseAdapter):
    def __init__(self, conn: any):
        self.conn = conn

    def init(self):
        cursor = self.conn.cursor()
        cursor.execute(mysql_tables)

    def add_memory(self, role: str, content: str, agent_id: str, user_id: str):
        pass

    def get_memories(self, params: dict):
        pass