import json

def parse_json_field(value):
    if not value:
        return []

    try:
        return json.loads(value)
    except Exception:
        return []