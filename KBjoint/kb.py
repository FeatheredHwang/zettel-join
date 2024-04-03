"""
Knowledge Base

# TODO using GitPython to monitor changes and record each file's notetype
# todo: Popup a process bar to show the process
#   and stop user doing anything else before importation done.
# mw.progress.start(max=1, parent=mw)
# # Processing...
# mw.progress.update()
# mw.progress.finish()
"""

import logging
import os

from aqt import mw
from aqt.qt import QFileDialog
from aqt.utils import showInfo, askUser

from .joint import MdJoint, ClozeJoint, OnesideJoint


class KnowledgeBase:
    """
    Knowledge Base
    """
    top_dir: str = ''
    test_mode: bool = False
    joints: dict[str, MdJoint] = {}

    def __init__(self, top_dir: str = None, test_mode: bool = False):
        logging.debug(f'CWD - current working directory: {os.getcwd()}')
        self.init_dir(top_dir)
        self.test_mode = test_mode
        # Add joints in this function, manually
        self.register_joints()

    def register_joints(self):
        """
        Add joints in this function, manually
        # todo let user choose which joint works?
        """
        if not self.top_dir:
            return
        if not self.test_mode:
            self.joints = {
                ClozeJoint.FILE_SUFFIX: ClozeJoint(),
                OnesideJoint.FILE_SUFFIX: OnesideJoint()
            }
        else:
            self.joints = {
                ClozeJoint.FILE_SUFFIX: ClozeJoint('Cloze (traceable) (test)'),
                OnesideJoint.FILE_SUFFIX: OnesideJoint('Oneside (test)')
            }

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
                self.init_dir()
                return
            else:
                logging.info('Initializing KB: open-kb-dir cancelled\n')
                return

        logging.info(f'Initializing KB done: top-dir is "{top_dir}"')
        self.top_dir = top_dir
        # todo write config
        # todo make the dir root

    def join(self):
        """
        Join your knowledge base to Anki
        """
        if not self.top_dir:
            return
        self.traverse()
        # Calculate how many cards imported
        new_notes_count: int = sum(joint.new_notes_count for joint in self.joints.values())
        logging.info(f'KB join: {new_notes_count} notes imported.\n')
        showInfo(f'{new_notes_count} notes imported.')
        # With notes added, refresh the deck browser
        mw.deckBrowser.refresh()
        # todo open the notesBrowser window, show the last added notes after kb-join

    def traverse(self):
        """
        Traverse the directory tree using os.walk()
        """
        for root, dirs, files in os.walk(self.top_dir):
            # !Attention! dirs and files are just basename without path
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            # Get the relative path of the current directory, and its depth from top dir
            rel_path = os.path.relpath(root, self.top_dir)
            depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))  # os.sep is '\'
            # Skip to next folder if not reach chapter depth yet
            if depth < 2:
                if files:
                    logging.debug(f'KB join - Skip files under "{rel_path}" since not reach chapter-depth yet.')
                continue

            # Filter out hidden files
            files = [f for f in files if not f.startswith('.')]
            # Find out files which is able to join
            join_tasks: list[(str, str)] = []
            for file in files:
                for suffix, joint in self.joints.items():
                    if joint.check_filename(file):
                        join_tasks.append((joint.FILE_SUFFIX, file))
            # Skip to next folder if no join-task exists
            if not join_tasks:
                logging.debug(f'KB join - Skip dir "{rel_path}" since no files to import here.')
                continue

            # join file to deck
            deck_name: str = rel_path.replace(os.sep, '::')
            logging.debug(f'KB join to the deck "{deck_name}"')
            for suffix, file in join_tasks:
                try:
                    self.joints[suffix].join(os.path.join(root, file), deck_name)
                except KeyError:
                    logging.warning(f'KB join - unexpected joint-suffix "{suffix}" from file "{file}"')

    def traverse_archive(self):
        """
        # todo traverse archive
        :return:
        :rtype:
        """
        pass

    def archive(self, dir_path):
        """
        # todo archive a folder

        :param dir_path:
        :type dir_path:
        """
        pass
