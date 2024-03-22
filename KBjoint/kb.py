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
    top_dir: str

    joints: dict[str, MdJoint]

    def __init__(self, top_dir: str = None):
        if top_dir:
            self.top_dir = top_dir
        else:
            self.top_dir = self.open_kb_dir()
        self.joints = {
            ClozeJoint.FILE_SUFFIX: ClozeJoint(),
            # OnesideJoint.FILE_SUFFIX: OnesideJoint()
        }

    def join(self):
        """
        Join your knowledge base to Anki
        """
        if not self.top_dir:
            logging.warning('Opening KB dir: empty dir path, no cards imported.\n')
            return
        else:
            logging.info(f'\nThe KB located at {self.top_dir}')

        # TODO using GitPython to monitor changes and record each file's notetype

        self.traverse()

        # Calculate how many cards imported
        new_notes_count = sum(joint.new_notes_count for joint in self.joints.values())
        logging.info(f'{new_notes_count} notes imported.\n'
                     '================================================================')
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
            logging.debug(f'Create deck name using relative directory path: `{deck_name}`')

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
        return m.group('suffix') if m else 'SUFFIX_MISSING'

    def traverse_archive(self):
        pass

    # The | symbol for type hinting is introduced in Python 3.10 and later versions.
    # For now, Anki uses Python 3.9
    # def open_kb_dir(self) -> str | None:
    def open_kb_dir(self) -> Union[str, None]:
        """
        Get KB directory to traverse
        :return: The directory path of chosen
        """
        # todo using config
        # try:
        #     init_dir = config['last_top_dir']
        # except KeyError:
        init_dir = os.path.expanduser("~")
        # noinspection PyTypeChecker
        top_directory = QFileDialog.getExistingDirectory(
            mw,
            'Open the Knowledge Base Directory',
            directory=init_dir
        )

        # check if user cancelled selection
        if not top_directory:
            logging.info('Opening KB dir: cancelled')
            return

        # save config
        # config['last_top_dir'] = top_directory

        # check if KB-folder or not, in case we open a sub of the top-directory
        if not os.path.exists(os.path.join(top_directory, 'ROOT')):
            logging.info("Opening KB dir: dir not valid - 'ROOT' file missing, ask user for choose-again")
            if askUser("The directory you choose does not contain KB 'ROOT' file inside.\n"
                       "Choose again? "):
                return self.open_kb_dir()
            else:
                logging.info("Opening KB dir: choose-again cancelled.")
                return

        logging.info(f"Opening KB dir: dir valid, shown below \n  {top_directory}")
        return top_directory
