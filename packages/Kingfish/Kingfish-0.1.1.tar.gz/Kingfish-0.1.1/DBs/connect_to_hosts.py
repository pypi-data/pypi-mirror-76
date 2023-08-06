from DBs import read_config
from Overlord.ssh import Host

mongodb_credentials = read_config()["MONGODB"]
sql_credentials = read_config()["SQL"]

mongodb_connect = Host(mongodb_credentials["MONGODB_HOST"], "username", "password")
sql_connect = Host(sql_credentials["SQL_HOST"], "username", "password")

def mongo_connection(command):
    mongodb_connect.connect()
    output = mongodb_connect.execute(command)

def sql_connection(command):
    sql_connect.connect()
    output = sql_connect.execute(commands)
