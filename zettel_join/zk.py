# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
ZettelKästen
A ZK contains a '.root' directory
"""

import logging
import os

from aqt import mw, gui_hooks
from aqt.qt import QFileDialog
from aqt.utils import showInfo, askUser

from anki.models import ModelManager, MODEL_CLOZE
from anki.models import NotetypeDict as Model
from anki.models import TemplateDict as Template

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


"""

A joint is an import handler, which corresponds to a special file-format as well as a model.

"""


class MdJoint:
    test_mode: bool = False
    model: Model = None
    model_name: str = None

    def __init__(self):
        self.new_notes_count = 0
        gui_hooks.profile_did_open.append(self.create_model)
        ...

    def check_model(self) -> bool:
        """
        verify if model exists
        :return: True if it does, otherwise False
        """
        if self.model_name is None:
            logger.error('Create model: model name is None.')
            return True
        m = mw.col.models.byName(self.model_name)
        if m:
            logger.info(f'Create model: model already exists, model name"{self.model_name}"')
            return True
        else:
            return False

    def create_model(self):
        ...

    def join(self, zk: ZettelKasten):
        ...

    def get_files(self):
        ...

    def check_file(self):
        ...

    @staticmethod
    def read(file: str) -> str:
        """
        Open the file and read the file content.
        :param file: The path of the file to read from.
        :return: The content of the file.
        """
        try:
            with open(file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                logger.debug(f'File read: done, filepath "{file}"')
                return file_content
        except FileNotFoundError:
            logger.error(f'File read: error, file not found, filepath "{file}"')
        except IOError as e:
            logger.error(f'File read: error, {e}, filepath "{file}"')
        return ''


class ClozeJoint(MdJoint):
    model_name: str = 'ZK cloze'

    def __init__(self):
        super().__init__()

    def create_model(self):
        if self.check_model():
            return
        logger.info(f'Create model: begin, model name "{self.model_name}"')
        # create model if not exist
        mm: ModelManager = mw.col.models
        m: Model = mm.new(self.model_name)
        fields: list[str] = [
            'file',
            'header',  # used to traceback to sections in the book
            'Text',
            'Extra',
        ]
        m["type"] = MODEL_CLOZE  # as cloze type
        # Add fields
        for fld_name in fields:
            fld = mm.newField(fld_name)
            fld['size'] = 15
            fld['plainText'] = True
            mm.addField(m, fld)
        mm.set_sort_index(m, fields.index('header'))
        # Add card template and css using relative path
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        t: Template = mm.newTemplate('Cloze')
        t['qfmt'] = self.read('tpl/cloze_front.html')
        t['afmt'] = self.read('tpl/cloze_back.html')
        mm.addTemplate(m, t)
        m['css'] = self.read('tpl/cloze.css')
        # Add the Model (NoteTypeDict) to Anki
        mm.add_dict(notetype=m)
        self.model = mm.by_name(self.model_name)
        logger.info(f'Create model: done, model name "{self.model_name}"')


# Add joints in this function, manually
JOINTS: dict[str: MdJoint] = {
    ClozeJoint.model_name: ClozeJoint(),
}
