# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
A joint is an import handler, which corresponds to a special file-format as well as a model.
"""

import copy
import emojis
import frontmatter
import logging
import markdown
import os
import shutil

from bs4 import BeautifulSoup, Tag, NavigableString, Comment, ResultSet
from markdown.extensions import tables
from pymdownx import arithmatex, superfences

from aqt import mw, gui_hooks
from aqt.utils import showInfo
from anki.decks import DeckId
from anki.models import ModelManager, MODEL_CLOZE
from anki.models import NotetypeDict as Model
from anki.models import TemplateDict as Template
from anki.notes import Note, NoteId

from .zk import ZettelKasten


logger = logging.getLogger(__name__)


class Joint:
    def __init__(self):
        ...

    def join_zk(self, zk: ZettelKasten = None, test_mode: bool = False):
        ...


class MdJoint(Joint):

    def __init__(self):
        super().__init__()
        ...

    def join_zk(self, zk: ZettelKasten = None, test_mode: bool = False):
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

    """
    Initialize
    """

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
            'root',  # the header path inside MD file
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

    """ ========== ========== ========== ========== ========== ========== ========== ========== ========== ========== 
    ZK-level
    """

    def join_zk(self, zk: ZettelKasten = None, test_mode: bool = False) -> int:
        self.zk = zk
        if test_mode:
            self.model_name += ' (test)'
            self.check_model(self.model_name)
        logger.info(f'ZK-join: start using {self.__class__}, map to model "{self.model_name}"')
        # Traverse the ZK
        new_notes_count: int = 0
        for root, dirs, files in os.walk(self.zk.path):
            # Get the relative path of the current directory
            rel_dir = os.path.relpath(root, self.zk.path)
            # !Attention! dirs and files are just basename without path
            # Filter out hidden directories, hidden or non-MD files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if f.endswith(self.FILE_TYPE) and not f.startswith('.')]
            if not files:
                logger.debug(f'ZK-join: Skip folder {rel_dir} since no MD files included.')
                continue
            logger.debug(f'ZK-join: Current dir "{rel_dir}".')
            # Generate deck_name and get deck_id
            deck_name: str = rel_dir.replace(os.sep, '::') if rel_dir != '.' else 'Default'
            deck_id: DeckId = mw.col.decks.id(deck_name)  # find deck or create if not exist
            # Calculate depth, warning if depth > 3
            depth = 0 if rel_dir == '.' else len(rel_dir.split(os.sep))  # os.sep is '\'
            if depth > 3:
                logger.warning(f'ZK-join: bad practise, current working dir is "{depth}-level-deep" in zk.')
            # Traverse the files
            for file in files:
                abs_file = os.path.join(root, file)  # get the abs path
                new_notes_count += self.join_file(abs_file, deck_id)
        logger.info(f'ZK-join: finish using {self.__class__}, with {new_notes_count} joined.\n')
        return new_notes_count

    """ ========== ========== ========== ========== ========== ========== ========== ========== ========== ========== 
    file-level
    """

    FILE_TYPE = '.md'

    def join_file(self, abs_file: str, deck_id: DeckId) -> int:
        """
        Join MD file.
        :param abs_file: The absolute path of the file to join
        :param deck_id: The ID of the deck where the MD file is joined to
        """
        logger.debug(f'File-join: Handling with "{os.path.basename(abs_file)}"')
        post = self.load(abs_file)
        # Skip to next file if not joinable
        if not self.check_joinable(post):
            logger.info(f'File-join: Skip file since it is not joinable.')
            return 0
        # join MD note
        post.content = self.standardize(post.content)
        soup: BeautifulSoup = self.make_soup(post.content)
        new_notes_count: int = 0
        # Traverse headings
        for heading in soup.find_all(self.HEADING_TAG_NAMES):
            if self.join_note(heading, deck_id):
                new_notes_count += 1
        logger.info(f'File-join: Done, with {new_notes_count} notes joined.')
        return new_notes_count

    def check_joinable(self, post: frontmatter.Post) -> bool:
        """
        Check the frontmatter metadata, see if joinable with current Joint
        :param post: frontmatter.Post
        :return: True if joinable, otherwise False
        """
        # try to fetch 'note-type'
        try:
            note_type: str = str(post['note-type'])
            logger.debug(f'File-join: "note-type" is "{note_type}" in the frontmatter.')
            # judge if match current joint
            if note_type == self.model_name or \
                    note_type in self.model_name:
                return True
            else:
                return False
        except KeyError:  # note-type key not exists
            logger.debug(f'File-join: "note-type" metadata missing in the frontmatter.')
            return False

    @staticmethod
    def standardize(content: str) -> str:
        """
        standardize markdown content to avoid some render error.
        :param content: MD content
        :return: standardized MD content
        """
        # replace ':emoji-alia:' to emoji
        content = emojis.encode(content)
        return content

    @staticmethod
    def make_soup(content: str) -> BeautifulSoup:
        """
        Transfer md file to html, then using bs4 to parse
        :param content: md file content
        :return: beautifulsoup (parse tree) of the file
        """
        extensions: list[markdown.Extension] = []
        # add table extension
        table_ext = tables.TableExtension()
        table_ext.setConfig('use_align_attribute', True)
        extensions.append(table_ext)
        # add math extension
        math_ext = arithmatex.ArithmatexExtension()
        math_ext.setConfig('preview', False)
        math_ext.setConfig('generic', True)
        # not wrap while parse md, add manually after cloze deletion
        math_ext.setConfig('tex_block_wrap', ['', ''])
        extensions.append(math_ext)
        # add fenced-code extension
        fenced_code_ext = superfences.SuperFencesCodeExtension()
        extensions.append(fenced_code_ext)
        # parse markdown with extensions
        html = markdown.markdown(content, extensions=extensions)
        return BeautifulSoup(html, 'html.parser')

    """ ========== ========== ========== ========== ========== ========== ========== ========== ========== ========== 
    note-level
    """

    HEADING_TAG_NAMES: list[str] = [f'h{n}' for n in range(1, 7)]

    def join_note(self, note_heading: Tag, deck_id: DeckId) -> int:
        """
        Join MD file sections to Anki notes
        :param note_heading: bs4-tag of heading from the parse tree, which corresponds to an Anki-note
        :param deck_id: The ID of the deck where the MD file is joined to
        :return: How many cloze-deletions made
        """
        # get heading root (heading path)
        root_field = self.parse_root_field(note_heading)
        logger.info(f'Note-join: Handling with note-heading: "{root_field}"')
        # Check if the note has been imported (commented with note_id)
        noteid = self.get_commented_noteid(note_heading)
        if noteid:
            logger.debug(f'Note-join: note already imported: "{root_field}"')
            return 0
        # parse note scope
        note_scope: BeautifulSoup = self.get_note_scope(note_heading)
        extra_field_scope = self.parse_extra_field_scope(note_scope)
        text_field_scope = self.parse_text_field_scope(note_scope)
        # cloze deletion
        new_cloze_count: int = 0
        for cloze_tag in self.do_cloze_selection(cloze_scope=text_field_scope):
            if self.do_cloze_deletion(cloze_tag, new_cloze_count + 1):
                new_cloze_count += 1
        # check if the note has cloze-deletion
        if not new_cloze_count:
            logger.debug(f'Note-join: no cloze-deletion found, skip.')
            return 0
        # Import media files
        self.do_media_import(extra_field_scope)
        self.do_media_import(text_field_scope)
        # Create a note
        note = Note(mw.col, self.model)
        note['root'] = root_field
        note['Text'] = str(text_field_scope)
        note['Extra'] = str(extra_field_scope)
        if '⭐' in root_field:
            note.tags.append('marked')
        # add note to deck, and the note object will get assigned with id
        mw.col.add_note(note, deck_id)
        self.comment_noteid(note_heading, note.id)
        logger.info(f'Note-Join: Done, {new_cloze_count} cloze-deletions made, note.id: {note.id}')
        return new_cloze_count

    def get_note_scope(self, note_heading: Tag, recursive: bool = False) -> BeautifulSoup:
        """
        get the note scope of soup from the parse tree (a header corresponds to a note)
        :param note_heading: heading bs4-tag from the parse tree, which corresponds to Anki-note
        :param recursive: if True, include subheadings with their content
        :return: BeautifulSoup instance of the note scope, note-heading excluded
        """
        # check tag name
        if note_heading.name not in self.HEADING_TAG_NAMES:
            raise ValueError(f'heading tag supposed, but <{note_heading.name}> tag get')
        # setup stop condition (while encounter the specific tag, stop parsing)
        if recursive:
            stop = self.HEADING_TAG_NAMES[:self.HEADING_TAG_NAMES.index(note_heading.name) + 1]
        else:
            stop = self.HEADING_TAG_NAMES
        stop.append('hr')  # <hr> tag is also one of stop tag
        # generate heading/note scope
        note_scope: BeautifulSoup = BeautifulSoup('', 'html.parser')
        sibling = note_heading.next_sibling  # !Attention! .next_sibling might return NavigableString
        while sibling and sibling.name not in stop:
            if sibling.name in stop:
                break
            note_scope.append(copy.copy(sibling))
            sibling = sibling.next_sibling
        return note_scope

    def parse_root_field(self, note_heading: Tag) -> str:
        index = self.HEADING_TAG_NAMES.index(note_heading.name)
        heading_strs: list[str] = []
        for n in range(index):
            heading_strs.append(note_heading.find_previous_sibling(self.HEADING_TAG_NAMES[n]).text)
        return '.'.join(heading_strs)

    @staticmethod
    def parse_extra_field_scope(note_scope: BeautifulSoup) -> BeautifulSoup:
        """
        Extract the blockquote tags to extra field
        :param note_scope: BeautifulSoup instance of the note scope
        :return: BeautifulSoup instance of extra field scope
        """
        extra_field_scope: BeautifulSoup = BeautifulSoup()
        # Find all the blockquote tags, join them as the extra field
        for tag in note_scope.find_all('blockquote', recursive=False):
            extra_field_scope.append(tag)
        return extra_field_scope

    @staticmethod
    def parse_text_field_scope(note_scope: BeautifulSoup) -> BeautifulSoup:
        """
        Parse the text field scope
        :param note_scope: BeautifulSoup instance of the note scope
        :return: BeautifulSoup instance of text field scope
        """
        # check if blockquote tags has been extracted
        bq_tags = note_scope.find_all('blockquote', recursive=False)
        if bq_tags:
            for tag in bq_tags:
                tag.decompose()
            logger.warning(f'Note-join: blockquote tags decomposed (without included in "Extra" field)')
        return note_scope

    def comment_noteid(self, note_heading: Tag, note_id: NoteId) -> str:
        ...

    def get_commented_noteid(self, note_heading: Tag) -> NoteId:
        ...

    def do_media_import(self, soup: BeautifulSoup) -> int:
        """
        Import media file to Anki collection (media folder).
        :param soup: BeautifulSoup object of note scope
        :return: How many media files imported
        """
        ...

    """ ========== ========== ========== ========== ========== ========== ========== ========== ========== ========== 
    cloze-level
    """

    @staticmethod
    def do_cloze_selection(cloze_scope: BeautifulSoup) -> ResultSet:
        """
        Select cloze on the text field
        :param cloze_scope: BeautifulSoup instance of the note scope
        :return: ResultSet of cloze tags
        """
        # replace blockquote tags with placeholder, to avoid select cloze-deletion in blockquote tags
        blockquote_tags = cloze_scope.find_all('blockquote')
        ph_count: int = 0
        for bq_tag in blockquote_tags:
            ph_count += 1
            ph_tag = cloze_scope.new_tag('blockquote')
            ph_tag['id'] = f'ph-{ph_count}'
            bq_tag.replace_with(ph_tag)
        # find all cloze-deletion, avoid including child tag, skip if empty
        cloze_tags: ResultSet = cloze_scope.find_all(['strong', 'em', 'td', 'li'])
        cloze_tags += cloze_scope.select('div.arithmatex')
        # replace the blockquote placeholders with the original
        ph_count = 0
        for bq_tag in blockquote_tags:
            ph_count += 1
            ph_tag = cloze_scope.select_one(f'blockquote#ph-{ph_count}')
            ph_tag.replace_with(bq_tag)
        return cloze_tags

    @staticmethod
    def do_cloze_deletion(cloze_tag: Tag, cloze_no: int) -> bool:
        """
        Do cloze-deletion on the text field
        :param cloze_tag: Tag waiting for cloze-deletion
        :param cloze_no: cloze number which is unique in the note
        :return: True if cloze deletion was successful, False otherwise
        """
        if cloze_tag.string.strip() == '':  # skip empty tag
            return False
        if len(cloze_tag.contents) > 1:  # skip if including child tag(s)
            return False
        cloze_tag.string = '{{c' + str(cloze_no) + ':: ' + cloze_tag.string + '}}'
        # add math wrap manually
        if cloze_tag.has_attr('class') and cloze_tag.attrs['class'] == 'arithmatex':
            cloze_tag.contents[0].insert_before('\\[')
            cloze_tag.contents[-1].insert_after('\\]')
        return True


""" ========== ========== ========== ========== ========== ========== ========== ========== ========== ========== 
module-level functions
"""

# Add joints in this function, manually
JOINTS: dict[str: Joint] = {
    ClozeJoint.model_name: ClozeJoint(),
}


def join(path: str, test_mode: bool = False):
    """
    Join your ZettelKästen to Anki
    """
    if not path:
        return
    zk: ZettelKasten = ZettelKasten(path)
    logger.info(f'ZK-join: Handling with ZK "{zk.path}".\n')
    new_notes_count: int = 0
    for joint in JOINTS.values():
        joint.join_zk(zk, test_mode=test_mode)
        # calculate how many cards imported
        new_notes_count += joint.new_notes_count
    logger.info(f'ZK-join: Done, {new_notes_count} notes imported.\n\n')
    showInfo(f'ZK-join finished, with {new_notes_count} notes imported.')
    # refresh the deck browser
    mw.deckBrowser.refresh()
