import json
from pathlib import Path
config_credentials = Path(__path__).parent / 'config.json'

def read_config():
    with open(config_credentials, "r") as db_config:
        credentials = json.load(db_config)
    return credentials