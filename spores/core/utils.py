import json
import uuid

def is_valid_json(input_string):
    try:
        json.loads(input_string)
        return True
    except Exception:
        return False
    
def string_to_uuid(input_string):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, input_string))
