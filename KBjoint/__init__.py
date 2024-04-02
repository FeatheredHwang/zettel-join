"""
Initialize the Add-on.
"""

# import importlib.util
import logging
import os
import subprocess
# import sys

# from aqt import gui_hooks
from aqt import mw
from aqt.qt import QAction, qconnect

# Logging set up
##################################################

# Set the working directory to the current Python script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(os.getcwd(), 'root.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')
# log the module's directory
logging.info(f'Initializing logging - log file path: {log_file_path}')

# Install modules
##################################################

# For modules that are not included by Anki:
# Register modules Here!
MODULE_MAP: dict[str, str] = {
    # 'module_name': 'package_name',
    'emojis': 'emojis',
    'pymdownx': 'pymdown-extensions',
}

# # import_module from a relative path with python importlib
# # todo import_module NOT WORKING, try to figure out why
# def import_module(module_name, file_path: str = '.' + TARGET_DIR):
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     sys.modules[module_name] = module
#     spec.loader.exec_module(module)

# pip options
# -i, --index-url <url>
#   Base URL of the Python Package Index (default https://pypi.org/simple)
INDEX_URL = 'https://mirrors.aliyun.com/pypi/simple'
# -t, --target <dir>
#   Install packages into <dir>. By default, this will not replace existing files/folders in <dir>.
#   Use --upgrade to replace existing packages in <dir> with new versions.
TARGET_DIR = 'lib'


def check_module(module_name: str):
    """
    check if modules exist, install module if not
    """
    if os.path.exists(os.path.join(TARGET_DIR, module_name)):
        logging.debug(f'Import module - modules already exist: "{module_name}".')
    else:
        logging.info(
            f'Import module - module not found, install package with pip: "{MODULE_MAP[module_name]}".')
        command = ['pip', 'install', '-i', INDEX_URL, '--target', TARGET_DIR, MODULE_MAP[module_name]]
        subprocess.check_call(command)


for name in MODULE_MAP.keys():
    check_module(name)

# import test modules if exist
##################################################

try:
    from .test import *

    logging.info("Importing test module: done.\n")
except ImportError:
    logging.info("Importing test module: test module doesn't exist.\n")

# Add 'KB Join' menu item
##################################################

# from kb import KB  # Anki cannot recognize it
from .kb import KnowledgeBase


def kb_join():
    """
    Join your knowledge base to Anki
    """
    KnowledgeBase(test_mode=test_mode).join()


# create a new menu item
action = QAction('KB Join', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, kb_join)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
