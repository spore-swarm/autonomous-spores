from abc import ABC, abstractmethod
import json
import time

class CacheAdapter(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str):
        pass

    @abstractmethod
    def delete(slef, key: str):
        pass


class DbCacheAdapter(CacheAdapter):
    def __init__(self, db_adapter, agent_id: str):
        self.db_adapter = db_adapter
        self.agent_id = agent_id

    def get(self, key: str):
        try:
            conn = self.db_adapter.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("select `value` from cache where `key`=%s and agent_id=%s limit 1", (key, self.agent_id))
            result = cursor.fetchone()
            if result:
                return result[0]

        except Exception as e:
            print(f"Error get cache from database: {e}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()        
    
    def set(self, key: str, value: str):
        self.delete(key)

        try:
            conn = self.db_adapter.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("insert into cache(agent_id,`key`,`value`) values(%s,%s,%s)", (self.agent_id,key, value))
            conn.commit()
        except Exception as e:
            print(f"Error set cache from database: {e}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()              
    
    def delete(self, key: str):
        try:
            conn = self.db_adapter.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("delete from `cache` where `key`=%s and agent_id=%s", (key, self.agent_id))
            conn.commit()
        except Exception as e:
            print(f"Error delete cache from database: {e}")
            raise
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()          

class CacheManager():
    def __init__(self, adapter: CacheAdapter):
        self.adapter = adapter

    def get(self, key: str):
        data = self.adapter.get(key)

        if data:
            parsed_data = json.loads(data)
            value = parsed_data.get("value")
            expires = parsed_data.get("expires")

            if expires == 0 or expires > int(time.time() * 1000):
                return value
            
            self.adapter.delete(key)

        return None

    def set(self, key: str, value: str, expires: int = 0):
        data = json.dumps({"value": value, "expires": expires})
        self.adapter.set(key, data)

    def delete(self, key: str):
        self.adapter.delete(key)

    