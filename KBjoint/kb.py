"""
Knowledge Base
"""

import logging
import os
import re
from typing import Union

from aqt import mw
from aqt.qt import QFileDialog
from aqt.utils import showInfo, askUser

from .joint import MdJoint, ClozeJoint, OnesideJoint


class KB:
    """
    Knowledge Base
    """
    top_dir: str = ''

    joints: dict[str, MdJoint]

    def __init__(self, top_dir: str = None):

        self.init_dir(top_dir)

        # TODO let user choose which joint works?
        self.joints = {
            ClozeJoint.FILE_SUFFIX: ClozeJoint(),
            OnesideJoint.FILE_SUFFIX: OnesideJoint()
        }

    def join(self):
        """
        Join your knowledge base to Anki
        """
        if not self.top_dir:
            logging.warning('Importing KB: dir is empty, without any notes imported.\n')
            return

        # TODO using GitPython to monitor changes and record each file's notetype

        self.traverse()

        # Calculate how many cards imported
        new_notes_count = sum(joint.new_notes_count for joint in self.joints.values())
        logging.info(f'Importing KB: {new_notes_count} notes imported.\n')
        showInfo(f'{new_notes_count} notes imported.')

        # With notes added, refresh the deck browser
        mw.deckBrowser.refresh()
        # todo open the notesBrowser window, show the last added notes

    def traverse(self):
        # Traverse the directory tree using os.walk()
        # todo: Popup a process bar to show the process
        #   and stop user doing anything else before importation done.
        # mw.progress.start(max=1, parent=mw)
        # # Processing...
        # mw.progress.update()
        # mw.progress.finish()
        for root, dirs, files in os.walk(self.top_dir):

            # Filter out hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

            # Calculate the relative path of the current directory
            relative_root = os.path.relpath(root, self.top_dir)

            # replace os.sep with '::' as deck's name
            deck_name: str = relative_root.replace(os.sep, '::')
            # TODO only take two levels of the dir path
            # todo 'part' for the third level of dir path
            logging.debug(f'Importing KB: under deck_name "{deck_name}"')

            for file in files:
                # judge if a file is a Markdown (.md) file
                if file.endswith('.md'):
                    suffix = self.get_suffix(file)
                    joint: MdJoint
                    try:
                        joint = self.joints[suffix]
                    except KeyError:
                        joint = next(iter(self.joints.values()))
                    # logging.debug(f'Inside the directory a md file found: `{file}`')
                    joint.join(str(os.path.join(root, file)), deck_name)

    @staticmethod
    def get_suffix(file: str) -> str:
        """
        Return suffix in filename that shows which joint the file uses
        :param file: filename str
        :return: suffix str
        """
        m = re.fullmatch(
            r'.+\((?P<suffix>\w+)\)\.\w+',
            file
        )
        return m.group('suffix') if m else ''

    def traverse_archive(self):
        pass

    def init_dir(self, top_dir: str = None):
        """
        Get KB directory
        """
        if not top_dir:
            # todo read config
            init_dir = os.path.expanduser("~")
            top_dir = QFileDialog.getExistingDirectory(
                mw,
                'Open Knowledge Base Directory',
                directory=init_dir
            )
            if not top_dir:
                logging.info('Initializing KB: open-kb-dir cancelled')
                return

        # check if the dir contains a 'ROOT' file, in case we open a sub of the top-directory
        if not os.path.exists(os.path.join(top_dir, 'ROOT')):
            logging.info('Initializing KB: dir not valid - "ROOT" file missing, ask user for choose-again.')
            if askUser('Knowledge Base directory does not contain "ROOT" file inside.\n'
                       'Choose again?'):
                self.init_dir()
                return
            else:
                logging.info('Initializing KB: open-kb-dir cancelled')
                return

        self.top_dir = top_dir
        # todo write config
        logging.info(f'Initializing KB done: top-dir is "{top_dir}"')

        # todo make the dir root
