import json

def is_valid_json(input_string):
    try:
        json.loads(input_string)
        return True
    except ValueError:
        return False