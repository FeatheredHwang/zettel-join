"""
Initialize the Add-on.
"""

import logging

# from aqt import gui_hooks
from aqt import mw
from aqt.qt import QAction, qconnect
from anki.utils import version_with_build, int_version

# logging setup
from . import log
# download package to local library
from . import modules
from . import kb

# Version Check
logging.info(f"Current Anki version is: {version_with_build()}")
if int_version() >= 231000:
    ...

# Import test modules if exist
##################################################
try:
    from . import test
except ImportError:
    logging.info("Importing test module: test module doesn't exist.\n")
else:
    logging.info("Importing test module: done.\n")


# Add 'KB Join' menu item
##################################################
def kb_join():
    """
    Join your knowledge base to Anki
    """
    kb.KnowledgeBase().join()


# create a new menu item
action = QAction('KB Join', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, kb_join)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
