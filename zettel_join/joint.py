# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

# TODO How to update the model? Using version to keep user's custom changes

"""

import logging
import os
import re
import shutil

import markdown

from anki.decks import DeckId
from anki.models import ModelManager, NotetypeDict, TemplateDict, MODEL_CLOZE
from anki.notes import Note, NoteId
from aqt import mw
from bs4 import BeautifulSoup, Tag, NavigableString, Comment, ResultSet

from .lib.pymdownx import arithmatex, superfences
from .lib import emojis

# legacy types
HeadingRoot = dict[str, str]


class MdJoint:
    """
    MdJoint is a model with join() function which import notes from markdown files.
    """

    DEFAULT_NAME: str = 'Basic'
    FILE_SUFFIX: str = 'basic'

    model_name: str
    handling_file: str
    # TODO !!! let's cancel 'handling_content'
    handling_content: str
    aimed_deck: str
    new_notes_count: int

    config = {
        # MD syntax config
        'fenced-code': False,
        'math': False,
        # MD standardize config
        'md-standardize': True,
        'emojis-encode': True,
    }

    HEADINGS: list[str] = [f'h{n}' for n in range(1, 7)]

    def __init__(self, model_name=DEFAULT_NAME):
        logging.debug(f'CWD - current working directory: {os.getcwd()}')
        # Using model manager is the only way to add new model
        self.model_name = model_name
        self.new_notes_count = 0

        # verify if model exists
        m = mw.col.models.byName(model_name)
        if m:
            logging.info(f'Initializing model - model already exists: "{model_name}"')
        else:
            # build model if not exists
            logging.info(f'Initializing model - model not exists, build() started: "{model_name}"')
            # Set the working directory to the path of current Python script
            #   used to find template files by relative path
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            logging.debug(f'Initializing model - current working directory is: {os.getcwd()}')
            self.build()
            logging.info(f'Initializing model - model not exists, build() done: "{model_name}"')

    def build(self):
        """
        Build up the model and add it to Anki yet
        """
        mm: ModelManager = mw.col.models
        m: NotetypeDict = mm.new(self.model_name)

        # Add fields
        for fld_name in ['Front', 'Back']:
            fld = mm.newField(fld_name)
            fld['size'] = 15
            fld['plainText'] = True
            mm.addField(m, fld)
        # Add card template
        t: TemplateDict = mm.newTemplate('Card 1')
        t['qfmt'] = "{{Front}}"
        t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
        mm.addTemplate(m, t)
        # Add css
        m['css'] = self.read('tpl/basic.css')

        # Add the Model (NoteTypeDict) to Anki
        mm.add_dict(notetype=m)

    def check_filename(self, file: str) -> bool:
        """
        check the file extension,
        and then check model [suffix] if the same as current model
        :param file: filepath
        :return: feasible or not
        """
        if re.match(r'.*\.md$', file, flags=re.IGNORECASE) \
                and self.get_suffix(file) == self.FILE_SUFFIX:
            return True
        else:
            return False

    def join(self, file: str, deck_name: str = None):
        """
        Parse the file content, map them on the model,
        then add/join them to collection.
        :param file: filepath of the kb md-format file
        :param deck_name: deck name where to import notes to
        """
        self.start_join(file, deck_name)
        pass

    def start_join(self, file: str, deck_name: str = None):
        if not deck_name:
            self.aimed_deck = 'Default'
        else:
            self.aimed_deck = deck_name
        self.handling_file = file

    def finish_join(self):
        """
        While finished join(), clear attrs so that it won't influence next join() job.
        """
        self.aimed_deck = ''
        self.handling_file = ''
        self.handling_content = ''

    def join_img(self, soup: BeautifulSoup):
        """
        Since folders inside the media folder are not supported,
        import img file directly to media folder with standard name,
        and modify 'src' attribute of <img> tag to filename
        :param soup: the BeautifulSoup that contains img tags
        """
        # todo Anki supports jpg better than png
        # todo resize picture
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            src = img_tag.get('src', None)
            # continue if src attribute missing
            if not src:
                logging.debug(f'Importing MD - add img failed, src attr missing "{src}"')
                continue
            # todo what if src is weblink
            if not os.path.isabs(src):
                os.chdir(os.path.dirname(self.handling_file))
                img = os.path.abspath(src)  # img path
            else:
                img = src
            # continue if file not exist
            if not os.path.exists(img):
                logging.debug(f'Importing MD - add img failed, file not exist "{img}"')
                continue
            img_name = os.path.basename(img)
            # create a copy with standardized name
            std_name = '.'.join(self.aimed_deck.split(sep='::') + [img_name])
            std_img = os.path.join(os.path.dirname(img), std_name)
            shutil.copyfile(img, std_img)
            # modify 'src' attribute of <img> tag
            img_tag['src'] = std_name
            # Anki will add basename of path to the media folder, renaming if not unique
            # which could be found under `%APPDATA%\Anki2`
            if not mw.col.media.have(std_name): mw.col.media.addFile(std_img)
            logging.debug(f'Importing MD - add img success, img path "{std_name}"')
            # delete copied file
            os.remove(std_img)

    # noinspection PyArgumentEqualDefault
    @staticmethod
    def read(file: str) -> str:
        """
        Open the file and read the file content.
        :param file: The path of the file to read from.
        :return: The content of the file.
        """
        try:
            # Attempt to open the file
            with open(file, 'r', encoding='utf-8') as f:
                # Read the entire content of the file
                file_content = f.read()
                logging.debug(f'File-read done: "{file}"')
                return file_content
        except FileNotFoundError:
            logging.error(f'File-read error - File not found: "{file}"')
        except IOError as e:
            logging.error(f'File-read error: "{file}" {e}')
        return ''

    @staticmethod
    def write(file: str, content: str):
        """
        Write content to a file.
        :param content: The content to write to the file.
        :param file: The path of the file to write to.
        """
        try:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.debug(f'File-write done: "{file}"')
        except Exception as e:
            logging.error(f'File-write error: "{file}" {e}')

    def make_soup(self, file: str) -> BeautifulSoup:
        """
        Transfer md file to html, then using bs4 to parse
        :param file: md file path
        :return: beautifulsoup (parse tree) of the file
        """
        content = self.standardize_md(file)
        self.handling_content = content

        extensions: list[markdown.Extension] = []
        # add math extension
        self.config['math'] = True if '$' in content else False
        if self.config['math']:
            # todo create extension with config dictionary?
            math_ext = arithmatex.ArithmatexExtension()
            math_ext.config['preview'] = [False, ""]
            math_ext.config['generic'] = [True, ""]
            extensions.append(math_ext)
        # add fenced-code extension
        self.config['fenced-code'] = True if '```' in content else False
        if self.config['fenced-code']:
            # add fenced_code extension
            fenced_code_ext = superfences.SuperFencesCodeExtension()
            fenced_code_ext.config['css_class'] = ['BlahBlah', '']
            extensions.append(fenced_code_ext)

        html = markdown.markdown(content, extensions=extensions)
        return BeautifulSoup(html, 'html.parser')

    def standardize_md(self, file: str = None, content: str = None) -> str:

        if file: content = self.read(file)
        if not content: return ''
        if self.config['emojis-encode']:
            # replace ':emoji-alia:' to emoji
            content = emojis.encode(content)
        # TODO !!! other standardize jobs like:
        #   todo what if no blank line before and after math blocks $$ signal? the render will return false result
        #   todo standard md file: no blank line inside list, even between p and blockquote tags inside li
        #   todo not allow blockquote inside another blockquote

        if self.config['md-standardize']: self.write(file, content)
        return content

    def standardize_field(self, field: str) -> str:

        if self.config['emojis-encode']:
            # replace ':emoji-alia:' to emoji
            field = emojis.encode(field)
        return field

    def comment_noteid(self, heading: Tag, note_id: NoteId):
        """
        add comment of NoteId for new notes
        :param heading:
        :param note_id:
        """
        # TODO !!! NOW could it be possible that insert in html tree and at the end transfer html page back to md?
        self.handling_content = re.sub(
            r'(\n*#+\s*{}\s*\n\n)'.format(heading.text),
            r'\1' + f'<!-- NoteId: {note_id} -->\n\n',
            self.handling_content)
        # there must be two '\n' at the end of the pattern,
        #  or the comment will be parsed as part of next element in markdown2
        logging.debug(f'Importing MD - NoteId commented after heading "{heading.text}".')

    @staticmethod
    def get_commented_noteid(heading: Tag) -> NoteId:
        """
        Get the noteid from comment right after the heading tag
        :param heading:
        :return:
        """
        comm = heading.next_sibling
        while comm and isinstance(comm, NavigableString):
            if isinstance(comm, Comment):
                break
            else:
                comm = comm.next_sibling
        else:
            return NoteId(0)
        m = re.fullmatch(
            r'\s*NoteId:\s*(?P<note_id>[0-9]{13})\s*',
            comm,
            flags=re.IGNORECASE
        )
        note_id = NoteId(m.group('note_id')) if m else None
        return note_id

    def get_heading_soup(self, heading: Tag, recursive: bool = False) -> BeautifulSoup:
        """
        find the content of heading
        :param heading:
        :param recursive: if True, include subheadings with their content
        :return:
        """
        if heading.name not in self.HEADINGS:
            raise ValueError(f'heading tag supposed, but <{heading.name}> tag get')
        if recursive:
            stop = self.HEADINGS[:self.HEADINGS.index(heading.name) + 1]
        else:
            stop = self.HEADINGS
        # add <hr> tag as its stop tag
        stop.append('hr')

        text: str = ''
        sibling = heading.find_next_sibling()  # Attention: .next_sibling might return NavigableString
        while sibling and sibling.name not in stop:
            text += str(sibling)
            sibling = sibling.find_next_sibling()
        return BeautifulSoup(text, 'html.parser')

    def get_heading_root(self, heading: Tag) -> HeadingRoot:
        index = self.HEADINGS.index(heading.name)
        heading_root: HeadingRoot = {}
        # start from h1, h2...
        for n in range(index):
            heading_root[self.HEADINGS[n]] = heading.find_previous_sibling(self.HEADINGS[n]).text
        # and end with current heading
        heading_root[heading.name] = heading.text

        return heading_root

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


class ClozeJoint(MdJoint):
    """
    This joint will create a cloze note for each heading.
    Markdown Reference:
    - To create cloze-deletion, enclose the contents as **strong** or list them all (without strong)
    - To mark a note, add '⭐' or ':star:' at the start of heading text;
    ...
    """
    DEFAULT_NAME: str = 'Cloze (traceable)'
    FILE_SUFFIX: str = 'cloze'

    NORMAL_FIELDS: list[str] = [
        'root',  # used to traceback to sections in the book
        'Text',
        'Extra',
    ]
    TRACEBACK_FIELDS_MAP: HeadingRoot = {
        'h1': 'Chapter',
        'h2': 'Section',
        'h3': 'Subsection',
    }

    def __init__(self, model_name=DEFAULT_NAME):
        super().__init__(model_name=model_name)

    def build(self):

        mm: ModelManager = mw.col.models
        m: NotetypeDict = mm.new(self.model_name)
        # as cloze type
        m["type"] = MODEL_CLOZE

        # Add fields
        for fld_name in self.NORMAL_FIELDS:
            fld = mm.newField(fld_name)
            fld['size'] = 15
            fld['plainText'] = True
            mm.addField(m, fld)
        mm.set_sort_index(m, self.NORMAL_FIELDS.index('root'))

        for fld_name in self.TRACEBACK_FIELDS_MAP.values():
            fld = mm.newField(fld_name)
            fld['plainText'] = True
            fld['collapsed'] = True
            fld['excludeFromSearch'] = True
            mm.addField(m, fld)

        # Add card template and css
        t: TemplateDict = mm.newTemplate('Cloze')
        t['qfmt'] = self.read('tpl/cloze_front.html')
        t['afmt'] = self.read('tpl/cloze_back.html')
        mm.addTemplate(m, t)
        m['css'] = self.read('tpl/cloze.css')

        # Add the Model (NoteTypeDict) to Anki
        mm.add_dict(notetype=m)

    def join(self, file: str, deck_name: str = None):
        """
        Parse the file content, map them on the model,
        then add/join them to collection.
        :param file: filepath of the kb md-format file
        :param deck_name: deck name where to import notes to
        """
        self.start_join(file, deck_name)

        # find deck or create if not exist
        deck_id: DeckId = mw.col.decks.id(deck_name)

        soup = self.make_soup(file)
        new_notes_count: int = 0
        # Traverse every heading and create note for it
        for heading in soup.find_all(self.TRACEBACK_FIELDS_MAP.keys()):

            # get heading_root
            heading_root: HeadingRoot = self.get_heading_root(heading)
            root_str = '.'.join(heading_root.values())
            # create note
            logging.debug(f'Importing MD - get heading: "{root_str}"')

            # Check if heading has been imported (commented with note_id)
            noteid = self.get_commented_noteid(heading)
            if noteid:
                logging.debug(f'Importing MD - note already imported: "{root_str}"')
                continue

            # check if heading has cloze-deletion
            cloze_text, extra_text = self.get_cloze_text(heading)
            if not cloze_text:
                logging.debug(f'Importing MD - cloze-deletion not found, skip: "{root_str}"')
                continue

            # Create a note, assign field values
            note = Note(mw.col, mw.col.models.byName(self.model_name))
            note['root'] = root_str
            note['Text'] = cloze_text
            note['Extra'] = extra_text
            for key, value in heading_root.items():
                note[self.TRACEBACK_FIELDS_MAP[key]] = value
            if any(value.startswith(star) for star in ['⭐', ':star:'] for value in heading_root.values()):
                note.tags.append('marked')
            # todo what about user-defined tags
            # Standardize fields
            for name, value in note.items():
                note[name] = self.standardize_field(value)

            # add note to deck, and the note object will get assigned with id
            mw.col.add_note(note, deck_id)
            # TODO !!! NOW add comment to a dictionary, comment at the end of the file.
            self.comment_noteid(heading, note.id)
            new_notes_count += 1
            logging.debug(f'Importing MD - Note added, note.id: {note.id}')

        # Finally, comment the source file if new-notes imported
        if new_notes_count > 0:
            self.new_notes_count += new_notes_count
            self.write(file, self.handling_content)

        self.finish_join()

    def get_cloze_text(self, heading: Tag) -> (str, str):
        """
        Analyse the heading's content, get 'cloze' and 'extra' fields' value as plain text (raw html text).
        :param heading: heading tag
        :return: 'cloze' and 'extra' fields' plain text
        """
        # Get cloze text, skip if empty
        heading_soup: BeautifulSoup = self.get_heading_soup(heading)
        # Find all tags and delete the unexpected
        #   extract the blockquote tags to extra_text
        extra_text = ''
        for tag in heading_soup.find_all(True, recursive=False):
            if tag.name == 'blockquote':
                extra_text += str(tag.extract())
            elif tag.name == 'div' and 'arithmatex' not in tag.get('class', []):
                tag.decompose()
            elif tag.name not in ['p', 'ol', 'ul', 'div', 'blockquote']:
                tag.decompose()
        if not heading_soup: return '', ''

        # replace blockquote with the placeholder
        blockquote_tags = heading_soup.find_all('blockquote')
        ph_count = 0
        for bq_tag in blockquote_tags:
            ph_tag = heading_soup.new_tag('blockquote')
            ph_count += 1
            ph_tag['id'] = f'placeholder-{ph_count}'
            bq_tag.replace_with(ph_tag)

        # find all cloze-deletion, avoid including child tag, skip notes if empty
        cloze_tags: ResultSet
        cloze_tags = heading_soup.find_all('strong')
        cloze_tags += heading_soup.select('li > p') if not cloze_tags else []
        cloze_tags += heading_soup.select('li') if not cloze_tags else []
        # todo rename the class attribute to 'math'
        cloze_math_tags = heading_soup.select('div.arithmatex') if self.config['math'] else []
        if not cloze_tags and not cloze_math_tags: return '', ''

        # cloze deletion
        cloze_count = 0
        for cloze_tag in cloze_tags:
            cloze_count += 1
            if len(cloze_tag.contents) == 1:
                cloze_tag.string = '{{c' + str(cloze_count) + ':: ' + cloze_tag.string + '}}'
            elif len(cloze_tag.contents) > 1:
                cloze_tag.contents[0].insert_before('{{c' + str(cloze_count) + ':: ')
                b = cloze_tag.find('blockquote')
                if b:
                    b.insert_before(' }}')
                else:
                    cloze_tag.contents[-1].insert_after(' }}')
        if self.config['math']:
            for cloze_math_tag in cloze_math_tags:
                cloze_count += 1
                cloze_math_tag.string = '\\[\n{{c' + str(cloze_count) + ':: ' + cloze_math_tag.string[3:-3] + ' }}\n\\]'

        # replace blockquote with the original
        ph_count = 0
        for bq_tag in blockquote_tags:
            ph_count += 1
            ph_tag = heading_soup.select_one(f'blockquote#placeholder-{ph_count}')
            ph_tag.replace_with(bq_tag)

        # Add image files to media
        self.join_img(heading_soup)

        # logging.debug('Text field after cloze-deletion: ' + str(heading_soup))
        return str(heading_soup), extra_text


class OnesideJoint(MdJoint):
    DEFAULT_NAME = 'Oneside'
    FILE_SUFFIX = 'oneside'
