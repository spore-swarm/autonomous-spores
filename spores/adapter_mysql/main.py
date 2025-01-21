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

    def create_memory(self, role:str, user_id:str, content: str, agent_id: str, room_id: str):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            id = string_to_uuid(datetime.now().isoformat())
            cursor.execute("insert into memories (id, role, user_id, content, agent_id, room_id) values (%s, %s, %s, %s, %s, %s)", (id, role, user_id, content, agent_id, room_id))
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
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM memories WHERE 1=1"
            query_params = []
            
            if 'room_id' in params:
                query += " AND room_id = %s"
                query_params.append(params['room_id'])
                
            if 'user_id' in params:
                query += " AND user_id = %s"
                query_params.append(params['user_id'])
            
            query += " ORDER BY create_time ASC"
            
            if 'count' in params:
                query += " LIMIT %s"
                query_params.append(int(params['count']))
            
            cursor.execute(query, tuple(query_params))
            memories = cursor.fetchall()
            return memories
            
        except Exception as e:
            print(f"Error getting memories: {e}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
        