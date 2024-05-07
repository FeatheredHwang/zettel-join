# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

A joint is an import handler, which corresponds to a special file-format as well as a model.

"""

import os
import logging


from aqt import mw, gui_hooks
from aqt.utils import showInfo
from anki.models import ModelManager, MODEL_CLOZE
from anki.models import NotetypeDict as Model
from anki.models import TemplateDict as Template

from .zk import ZettelKasten


logger = logging.getLogger(__name__)


class Joint:
    def __init__(self):
        ...

    def join(self, zk: ZettelKasten = None, test_mode: bool = False):
        ...


class MdJoint(Joint):
    zk: ZettelKasten = None
    test_mode: bool = False
    model: Model = None
    model_name: str = None

    def __init__(self):
        super().__init__()
        self.new_notes_count = 0
        gui_hooks.profile_did_open.append(self.create_model)
        ...

    def check_model(self) -> bool:
        ...

    def create_model(self):
        ...

    def join(self, zk: ZettelKasten = None, test_mode: bool = False):
        self.zk = zk

    def get_file(self):
        ...

    traverse = get_file

    def check_file(self, path: str):
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

    def get_file(self):
        """
        Traverse the directory
        """
        for root, dirs, files in os.walk(self.zk.path):
            # !Attention! dirs and files are just basename without path
            # Filter out hidden directories and hidden files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            # Get the relative path of the current directory, and its depth from top dir
            rel_path = os.path.relpath(root, self.zk.path)
            depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))  # os.sep is '\'
            # Find out files which is able to join
            joinable: list[str] = []
            for file in files:
                file = os.path.join(root, file)  # get the complete path
                if self.check_file(file):
                    joinable.append(file)
            # Skip to next folder if no join-task exists
            if not joinable:
                logger.debug(f'ZK join: Skip dir "{rel_path}" since no files to import here.')
                continue
            elif depth > 3:
                logger.warning(f'ZK join: current working dir is "{depth}-level-deep" in zk, which is not recommended.')
            # join file to deck
            deck_name: str = rel_path.replace(os.sep, '::') if rel_path != '.' else 'Default'
            logger.debug(f'ZK join: to deck "{deck_name}"')
            for file in joinable:
                ...

    def check_file(self, path: str):
        # todo check file suitable to current Joint
        ...


# Add joints in this function, manually
JOINTS: dict[str: Joint] = {
    ClozeJoint.model_name: ClozeJoint(),
}


def join(path: str = None, test_mode: bool = False):
    """
    Join your ZettelKästen to Anki
    """
    zk: ZettelKasten = ZettelKasten(path)
    if not path:
        return
    new_notes_count: int = 0
    for joint in JOINTS.values():
        joint.join(zk, test_mode=test_mode)
        # calculate how many cards imported
        new_notes_count += joint.new_notes_count
    logger.info(f'ZK join: Done, {new_notes_count} notes imported.\n')
    showInfo(f'ZK-join finished, with {new_notes_count} notes imported.')
    # refresh the deck browser
    mw.deckBrowser.refresh()
