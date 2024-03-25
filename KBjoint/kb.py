"""
Knowledge Base
"""

import logging
import os
import re

from aqt import mw
from aqt.qt import QFileDialog
from aqt.utils import showInfo, askUser

from .joint import MdJoint, ClozeJoint, OnesideJoint


class KB:
    """
    Knowledge Base
    """
    top_dir: str = ''
    joints: dict[str, MdJoint] = {}

    def __init__(self, top_dir: str = None):
        self.init_dir(top_dir)
        self.register_joints()

    def init_dir(self, top_dir: str = None):
        """
        Get KB directory
        """
        if not top_dir:
            # todo read config
            init_dir = os.path.expanduser("~")
            # noinspection PyTypeChecker
            top_dir = QFileDialog.getExistingDirectory(
                mw,
                'Open Knowledge Base Directory',
                directory=init_dir
            )
            if not top_dir:
                logging.info('Initializing KB: open-kb-dir cancelled\n')
                return

        # check if the dir contains a 'ROOT' file, in case we open a sub of the top-directory
        if not os.path.exists(os.path.join(top_dir, '.root')):
            logging.info('Initializing KB: dir not valid - ".root" folder missing, ask user to choose-again.')
            if askUser('Knowledge Base directory does not contain "ROOT" file inside.\n'
                       'Choose again?'):
                # self.init_dir()
                self.init_dir()
                return
            else:
                logging.info('Initializing KB: open-kb-dir cancelled\n')
                return

        logging.info(f'Initializing KB done: top-dir is "{top_dir}"')
        self.top_dir = top_dir
        # todo write config
        # todo make the dir root

    def register_joints(self):
        if not self.top_dir:
            return
        # todo let user choose which joint works?
        self.joints = {
            ClozeJoint.FILE_SUFFIX: ClozeJoint(),
            OnesideJoint.FILE_SUFFIX: OnesideJoint()
        }

    def join(self):
        """
        Join your knowledge base to Anki
        """
        if not self.top_dir:
            return
        self.traverse()
        # Calculate how many cards imported
        new_notes_count = sum(joint.new_notes_count for joint in self.joints.values())
        logging.info(f'Importing KB: {new_notes_count} notes imported.\n')
        showInfo(f'{new_notes_count} notes imported.')
        # With notes added, refresh the deck browser
        mw.deckBrowser.refresh()
        # todo open the notesBrowser window, show the last added notes

    def traverse(self):
        """
        Traverse the directory tree using os.walk()
        """
        # todo: Popup a process bar to show the process
        #   and stop user doing anything else before importation done.
        # mw.progress.start(max=1, parent=mw)
        # # Processing...
        # mw.progress.update()
        # mw.progress.finish()
        # TODO using GitPython to monitor changes and record each file's notetype
        for root, dirs, files in os.walk(self.top_dir):
            # Attention, dirs and files are just basename without path
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            # Get the relative path of the current directory, and its depth from top dir
            rel_path = os.path.relpath(root, self.top_dir)
            depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))
            # Skip if its top two levels
            if depth < 2:
                if files:
                    logging.debug(f'Importing KB - Skip files under "{rel_path}" since not reach chapter-depth yet.')
                continue
            # Replace os.sep('\') with '::' as deck's name
            deck_name: str = rel_path.replace(os.sep, '::')
            logging.debug(f'Importing KB: under deck_name "{deck_name}"')
            # Filter out hidden files
            files = [f for f in files if not f.startswith('.')]
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
                    joint.join(os.path.join(root, file), deck_name)

    def traverse_archive(self):
        # todo traverse archive
        pass

    def archive(self, dir_path):
        # todo archive a folder
        pass

    @staticmethod
    def get_suffix(file: str) -> str:
        """
        Return suffix in filename that shows which joint the file uses
        :param file: filepath
        :return: suffix str
        """
        m = re.fullmatch(
            r'.+\[(?P<suffix>\w+)]\.\w+',
            file
        )
        return m.group('suffix') if m else ''

    @staticmethod
    def remove_suffix(file: str) -> str:
        """
        Remove joint suffix in filename, and rename the file.
        :param file: filepath
        :return: filename with suffix removed
        """
        new_file = re.sub(r'\[\w+]', '', file)
        os.rename(file, new_file)
        return new_file

    @staticmethod
    def add_suffix(file: str, suffix: str) -> str:
        """
        Add/Replace joint suffix to filename, and rename the file.
        :param file: filepath
        :param suffix: joint suffix text
        :return: filename with suffix added/replaced
        """
        name, ext = os.path.splitext(re.sub(r'\[\w+]', '', file))
        new_file = f'{name}[{suffix}]{ext}'
        os.rename(file, new_file)
        return new_file
