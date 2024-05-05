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
from . import zk

logger = logging.getLogger(__name__)

# Version Check
logger.info(f"Current Anki version is: {version_with_build()}")
if int_version() >= 231000:
    ...

# Import test modules if exist
##################################################
try:
    from . import test
except ImportError as e:
    logger.info(f"Importing test module: {e}.\n")
else:
    logger.info("Importing test module: done.\n")


# Add 'ZK Join' menu item
##################################################
def zk_join():
    """
    Join your knowledge base to Anki
    """
    zk.ZettelKasten().join()


# create a new menu item
action = QAction('ZK Join', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, zk_join)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
