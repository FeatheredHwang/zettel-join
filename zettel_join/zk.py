"""
ZettelKästen
A ZK contains a '.root' directory
"""

import logging
import os

from aqt import mw
from aqt.qt import QFileDialog
from aqt.utils import showInfo, askUser

from .joint import JOINTS

logger = logging.getLogger(__name__)


class ZettelKasten:
    """
    ZettelKästen
    """
    path: str = None
    test_mode: bool = False

    def __init__(self, path: str = None, test_mode: bool = False):
        logger.debug(f'CWD - current working directory: {os.getcwd()}')
        self.test_mode = test_mode
        self.get_zk(path)

    def get_zk(self, path: str = None):
        """
        Get ZK directory path
        """
        if not path:
            df = os.path.expanduser("~")  # default path
            # noinspection PyTypeChecker
            path = QFileDialog.getExistingDirectory(
                mw,
                'Open ZettelKästen Directory',
                directory=df
            )
        if self.check_zk(path):
            self.path = path
            logger.info(f'Open ZK: Done, directory path is "{path}".\n')

    def check_zk(self, path: str = None) -> bool:
        if not path:
            logger.info('Open ZK: cancelled, directory path is empty.\n')
            return False
        # check if contains a '.root' directory, in case we open a sub-folder of ZK
        if os.path.exists(os.path.join(path, '.root')):
            return True
        else:
            logger.info('Open ZK: ".root" folder missing, ask user to choose-again.')
            if askUser('ZettelKästen directory does not contain ".root" folder.\n'
                       'Choose again?'):
                self.get_zk()
                return False  # which will do nothing, to avoid repeat job
            else:
                logger.info('Open ZK: cancelled, as user have choose.\n')
                return False

    def join(self):
        """
        Join your ZettelKästen to Anki
        """
        if not self.path:
            return
        new_notes_count: int = 0
        for joint in JOINTS.values():
            joint.join(self)
            # Calculate how many cards imported
            new_notes_count += joint.new_notes_count
        logger.info(f'ZK join: {new_notes_count} notes imported.\n')
        showInfo(f'{new_notes_count} notes imported.')
        # With notes added, refresh the deck browser
        mw.deckBrowser.refresh()
