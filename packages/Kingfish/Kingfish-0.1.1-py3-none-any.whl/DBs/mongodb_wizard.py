import pymongo
from Kingfish.DBs import read_config
import Core.logger as logger

mongo_section = read_config()["MONGODB"]

DEFAULT_MONGODB_HOST = mongo_section["MONGODB_HOST"]
DEFAULT_MONGODB_DB_NAME = mongo_section["MONGODB_DB_NAME"]

data_base = None
IS_CONNECTED = False
collections = []

def connect_to_mongodb(mongodb_host = DEFAULT_MONGODB_HOST, mongodb_db_name = DEFAULT_MONGODB_DB_NAME):
    global data_base, IS_CONNECTED
    print(f"hostname is {mongodb_host} and the DB name is {mongodb_db_name}")
    client = pymongo.MongoClient(mongodb_host, 27017)
    data_base = client[mongodb_db_name]
    IS_CONNECTED = True
    return IS_CONNECTED

def get_collection():
    global collections
    if not IS_CONNECTED:
        connect_to_mongodb()
    for collection in mongo_section["COLLECTIONS"]:
        collections.append(data_base[collection]) #cursor
    return IS_CONNECTED

def find_documents(value = None, key = None):
    relevant_docs = []
    for col in collections:
        for document in col.find():
            if value in document.values():
                print(document)
                relevant_docs.append(document)
            elif key in document.keys():
                print(document)
                relevant_docs.append(document)
    return relevant_docs

def create_document(**data):
    document = {}
    for key in data.keys():
        document[str(key)] = data.get(key)
    return document

def insert_to_mongodb(collection_name, doc = None, **data):
    if not IS_CONNECTED:
        connect_to_mongodb()
    collection = data_base[collection_name]
    if doc:
        collection.insert_one(doc)
        logger.info("Inserted successfully the document")
    else:
        document = {}
        for key in data.keys():
            document[str(key)] = data.get(key)
        collection.insert_one(document)
        logger.info("Inserted successfully the dictionary")
        
if __name__ == '__main__':
    get_collection()
    insert_to_mongodb("users", data = "dfsdfsdds", dsdsd = "dsds")
    find_documents(key="name")