from urllib.parse import urlparse
from Wrapper import read_config
from Core import logger

config = read_config()

array = config["VALUES_LIST"]
url = config["URL"]

def manipulator(func):
    value = func(array)
    print(f"{func.__name__} is {value}")

def url_extractor():
    path = urlparse(url)
    hostname = path.hostname
    port = path.port
    query = path.query
    return hostname, port, query

if __name__ == "__main__":
    manipulator(min)