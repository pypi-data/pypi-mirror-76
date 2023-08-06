"""
Usage: from Kingfish.Core import logger
       logger.info("message")
"""
import logging
from platform import platform
from pathlib import Path
import os

if "linux" in platform().lower():
    create_path_to_logs_file = Path('/opt/logs').mkdir(parents=True, exist_ok=True)
    path_to_logs_file = '/opt/logs'
elif "windows" in platform().lower():
    create_path_to_logs_file = Path('C:/Kingfish/logs').mkdir(parents=True, exist_ok=True)
    path_to_logs_file = 'C:/Kingfish/logs'
logs_filename = os.path.join(path_to_logs_file, 'logs_file.log')

logging.basicConfig(filename=logs_filename, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s') #DEBUG level is 10

def debug(msg: str):
    logging.debug(msg)
    print(f"-d- {msg} -d-")

def info(msg: str):
    logging.info(msg)
    print(f"-i- {msg} -i-")

def warn(msg: str):
    logging.warn(msg)
    print(f"-!- {msg} -!-")

def fatal(msg: str):
    logging.fatal(msg)
    print(f"-!!- {msg} -!!-")
    
def clear_logs_file():
    logs_file = open(logs_filename, 'w')
    logs_file.close()
    print("Logs file has been cleared!")

def display_logs_file():
    with open(logs_filename, 'r', encoding='utf-8') as logs_file:
        data = logs_file.read()
    print(data)