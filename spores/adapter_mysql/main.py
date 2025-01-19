from spores.core.database import DatabaseAdapter
from spores.adapter_mysql.tables import mysql_tables

class MysqlAdapter(DatabaseAdapter):
    def __init__(self, db: any):
        self.db = db

    def init(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(mysql_tables)
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def add_memory(self, role: str, content: str, agent_id: str, user_id: str):
        pass

    def get_memories(self, params: dict):
        pass