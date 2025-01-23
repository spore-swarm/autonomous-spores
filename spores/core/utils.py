import json
import uuid
import re

def is_valid_json(input_string):
    try:
        json.loads(input_string)
        return True
    except Exception:
        return False
    
def string_to_uuid(input_string):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, input_string))

def remove_json_block(text):
    pattern = r'```json[\s\S]*?```'
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return cleaned_text.strip()    
