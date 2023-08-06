import psycopg2
from Kingfish.DBs.mongodb_wizard import find_documents
from Kingfish.DBs import read_config

def convert_json_to_table(value = None):
    sql_commands = []
    for document in find_documents(value):
        columns = ', '.join("`" + str(val).replace('/', '_') + "`" for val in document.keys())
        values = ', '.join("'" + str(val).replace('/', '_') + "'" for val in document.values())
        sql_command = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values});"
        sql_commands.append(sql_command)
    return sql_commands

sql_section = read_config()["SQL"]
DEFAULT_SQL_HOST = sql_section["SQL_HOST"]
SQL_DB = sql_section["SQL_DB_NAME"]
USERNAME = sql_section["USERNAME"]
PASSWORD = sql_section["PASSWORD"]
PORT = sql_section["PORT"]
IS_CONNECTED = False

connection = psycopg2.connect(user=USERNAME, password=PASSWORD, host=DEFAULT_SQL_HOST, port=PORT, database=SQL_DB)

def connect_to_db():        
    cursor = connection.cursor()
    IS_CONNECTED = True
    return cursor

CURSOR = connect_to_db()

def run_query(command):
    CURSOR.execute(command)

def insert_row(insert_command):
    CURSOR.execute(insert_command)
    connection.commit()
