from datetime import datetime
from spores.core.database import DatabaseAdapter
from spores.adapter_mysql.tables import mysql_tables
from spores.core.utils import string_to_uuid

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

    def create_memory(self, user_id:str, content: str, agent_id: str, room_id: str):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            id = string_to_uuid(datetime.now().isoformat())
            cursor.execute("insert into memories (id,user_id, content, agent_id, room_id) values (%s, %s, %s, %s, %s)", (id, user_id, content, agent_id, room_id))
            conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_memories(self, params: dict):
        pass