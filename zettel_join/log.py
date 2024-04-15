"""
Logging set up
"""

import logging
import os

logger = logging.getLogger(__name__)


# Set the working directory to the current Python script
#   while copy addon files to Anki using batch, cwd is the Project's root dir like "D:\PycharmProjects\KBjoint"
#   while open Anki directly, cwd is Anki's installation dir like "D:\Program Files\Anki"
pwd = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(os.getcwd(), 'DEBUG.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')

# log the module's CWD
logger.debug(f'CWD: {pwd}\n')
logger.debug(f'Initializing logging - CWD: {os.getcwd()}')
logger.info(f'Initializing logging - log file path: {log_file_path}\n')
