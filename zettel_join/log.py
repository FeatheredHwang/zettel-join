"""
Logging set up
"""

import logging
import os

# Set the working directory to the current Python script
#   while copy addon files to Anki using batch, cwd is the Project's root dir like "D:\PycharmProjects\KBjoint"
#   while open Anki directly, cwd is Anki's installation dir like "D:\Program Files\Anki"
pwd = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(os.getcwd(), 'root.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')
# log the module's directory
logging.debug(f'CWD - previous working directory: {pwd}')
logging.debug(f'CWD - current working directory: {os.getcwd()}')
logging.info(f'Initializing logging - log file path: {log_file_path}\n')
