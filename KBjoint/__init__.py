import logging
import os

# from aqt import gui_hooks
from aqt import mw
from aqt.qt import QAction, qconnect

# from kb import KB  # Anki cannot recognize it
from .kb import KB

# Logging set up
##################################################

# Set the working directory to the current Python script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(os.getcwd(), 'default.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')
# log the module's directory
logging.info(f'Initializing logging - log file path: {log_file_path}')


# Add 'KB Join' menu item
##################################################

def kb_join():
    """
    Join your knowledge base to Anki
    """
    KB().join()


# create a new menu item
action = QAction('KB Join', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, kb_join)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


# import test modules if exist
##################################################
try:
    from .test.quick import *
    logging.info("Importing test module: done.\n")
except ImportError:
    logging.info("Importing test module: test module doesn't exist.\n")
