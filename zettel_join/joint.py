# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
A joint is an import handler, which corresponds to a special file-format as well as a model.
"""

import emojis
import frontmatter
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

    def __init__(self):
        super().__init__()
        ...

    def join(self, zk: ZettelKasten = None, test_mode: bool = False):
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

    def load(self, file: str) -> frontmatter.Post:
        post = frontmatter.loads(self.read(file))
        logger.debug(f'File load: Done, frontmatter metadata of above file is {post.metadata}')
        return post


class ClozeJoint(MdJoint):
    zk: ZettelKasten = None
    model: Model = None
    model_name: str = 'ZK cloze'

    def __init__(self):
        super().__init__()
        self.new_notes_count = 0
        gui_hooks.profile_did_open.append(self.check_model)

    def check_model(self, model_name: str = None) -> bool:
        """
        verify if model exists, create model if not
        :return: False while error happens, otherwise True
        """
        model_name = model_name if model_name else self.model_name
        if model_name is None:
            logger.error('Create model: cancelled, model name is None.')
            return False
        m = mw.col.models.byName(self.model_name)
        if m:
            logger.info(f'Create model: model already exists, model name "{self.model_name}"')
            self.model = m
            return True
        else:
            self.create_model(model_name=model_name)
            return True

    def create_model(self, model_name: str = None):
        model_name = self.model_name if not model_name else model_name
        logger.info(f'Create model: begin, model name "{model_name}"')
        # create model if not exist
        mm: ModelManager = mw.col.models
        m: Model = mm.new(model_name)
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
        self.model = mm.by_name(model_name)
        logger.info(f'Create model: Done, model name "{model_name}"')

    def join(self, zk: ZettelKasten = None, test_mode: bool = False):
        self.zk = zk
        if test_mode:
            self.model_name += ' (test)'
            self.check_model(self.model_name)
        # Traverse the zk
        for root, dirs, files in os.walk(self.zk.path):
            # !Attention! dirs and files are just basename without path
            # Filter
            dirs[:] = self.filter_dirs(dirs)
            files = self.filter_files(files)
            # Get the relative path of the current directory
            rel_dir = os.path.relpath(root, self.zk.path)
            if not files:
                logger.debug(f'ZK join: Skip folder {rel_dir} since no MD files included.')
                continue
            # Traverse the files
            joinable_count: int = 0
            deck_name: str = 'Default'
            for file in files:
                abs_file = os.path.join(root, file)  # get the abs path
                post = self.load(file)
                # Skip to next file if not joinable
                if not self.check_joinable(post):
                    logger.debug(f'ZK join: Skip file "{rel_dir}/{file}" since not joinable.')
                    continue
                joinable_count += 1
                if joinable_count == 1:
                    # generate deck_name
                    deck_name = rel_dir.replace(os.sep, '::') if rel_dir != '.' else 'Default'
                    logger.debug(f'ZK join: Current dir "{rel_dir}", to the deck "{deck_name}"')
                    # Calculate depth, warning if depth > 3
                    depth = 0 if rel_dir == '.' else len(rel_dir.split(os.sep))  # os.sep is '\'
                    if depth > 3:
                        logger.warning(f'ZK join: bad practise, current working dir is "{depth}-level-deep" in zk.')
                # join md note
                post.content = self.standardize(post.content)
                ...

    @staticmethod
    def filter_dirs(dirs: list[str]) -> list[str]:
        # Filter out hidden directories
        return [d for d in dirs if not d.startswith('.')]

    @staticmethod
    def filter_files(files: list[str]) -> list[str]:
        # Filter out hidden and non-MD files
        files = [f for f in files if f.endswith('.md') and not f.startswith('.')]
        return files

    def check_joinable(self, post: frontmatter.Post) -> bool:
        """
        check file joinable by current Joint
        :param post: frontmatter.Post
        :return: True if joinable, otherwise False
        """
        # try to fetch 'note-type'
        try:
            note_type: str = str(post['note-type'])
            logger.debug(f'ZK join: "note-type" is "{note_type}" in the frontmatter.')
            # judge if match current joint
            if note_type == self.model_name or \
                    note_type in self.model_name:
                return True
            else:
                return False
        except KeyError:  # note-type key not exists
            logger.debug(f'ZK join: "note-type" metadata missing in the frontmatter.')
            return False

    def standardize(self, content: str) -> str:
        """
        standardize markdown content to avoid some render error.
        :param content: MD content
        :return: standardized MD content
        """
        # replace ':emoji-alia:' to emoji
        content = emojis.encode(content)
        return content
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
