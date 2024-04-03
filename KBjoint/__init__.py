"""
Initialize the Add-on.
"""

import logging
import os

# from aqt import gui_hooks
from aqt import mw
from aqt.qt import QAction, qconnect


from . import log
from . import modules
from . import kb

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
