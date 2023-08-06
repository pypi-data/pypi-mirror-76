import json
from pathlib import Path

configuration_file = Path(__path__).parent / 'configuration.json'

def read_config():
    with open(configuration_file, "r") as db_config:
        credentials = json.load(db_config)
    return credentials