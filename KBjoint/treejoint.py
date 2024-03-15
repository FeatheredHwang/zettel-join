"""
The `Topic Tree` model structure:

```
MainTopic
|___Subtopic_1
|___Subtopic_2
...
|___Subtopic_n
```

"""

import logging
import os
import re
import sys

from anki.decks import DeckId

# import markdown2 from the local libray, cause Anki doesn't include this module
try:
    from .Lib import markdown2
    # TODO markdown2 parser doesn't support latex
except ImportError as e:
    logging.warning(f'"markdown2" module not found, exit: {e}')
    sys.exit()

from bs4 import BeautifulSoup, Comment

from anki.notes import Note
from anki.models import ModelManager, NotetypeDict, TemplateDict
from aqt import mw

from .joint import Joint


class TreeJoint(Joint):
    """
    A joint to import md files to 'Cloze with root' model.
    """

    MODEL_NAME: str = 'Cloze (traceable)'
    FILE_SUFFIX: str = 'traceable'
    FIELD_LIST: list[str] = [
        'root',
        'Book Title',
        'Part',
        'Chapter',
        'Section',
        'Subsection',
        'Text',
        'Front Extra',
        'Back Extra',
    ]
    # SUBTOPIC_AMOUNT: int = 6
    # TEMPLATE_PLACEHOLDER: str = '%n'

    @classmethod
    def build_model(cls):
        """
        Build the custom model. The model designed under minimum information principle.
        :Return: NotetypeDict
        """

        # Using model manager is the only way to add new model
        mm: ModelManager = mw.col.models
        t: TemplateDict

        # verify if model exists. If not, build model
        m: NotetypeDict = mw.col.models.byName(cls.MODEL_NAME)
        if m:
            # TODO How to update the model? Using version to keep user's custom changes
            logging.info(f'NoteType {m["name"]} already exist, skip building')
            return
        logging.info(f'Building Model <{cls.MODEL_NAME}> ...')

        m = mm.new(cls.MODEL_NAME)

        # Set the working directory to the path of current Python script
        #   used to find template files by absolute path
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        logging.debug(f'Current working directory is: {os.getcwd()}')

        # Add fields and Card
        for fld in cls.FIELD_LIST:
            mm.addField(m, mm.newField(fld))

        # Add card template
        t = mm.newTemplate(cls.MODEL_NAME)
        t['qfmt'] = cls.read_file('templates/cloze_front.html')
        t['afmt'] = cls.read_file('templates/cloze_back.html')
        mm.addTemplate(m, t)

        # Add css
        m['css'] = cls.read_file('templates/css.css')

        # Add the Model (NoteTypeDict) to Anki
        mm.add_dict(m)
        logging.info(f'Model <{m["name"]}> added to Anki')

    @classmethod
    def parse(cls, file: str, deck_name: str) -> list[int]:
        """
        Parse the file content, map them on the model,
        then add/join them to collection.
        :param deck_name: deck name that generated from file path
        :param file: absolute filepath
        :return: list of id to the created notes
        """
        # TODO verify the file...

        cls.build_model()

        # Get bs4 soup based on md file
        md_content = cls.read_file(file)
        content = markdown2.markdown(md_content)
        soup = BeautifulSoup(content, "html.parser")

        head_levels: list[str] = ['h1', 'h2', 'h3']

        for head_level in head_levels:
            for head in soup.find_all(head_level):
                logging.debug(head)

                # Create a note
                note = Note(mw.col, mw.col.models.by_name(cls.MODEL_NAME))

                if head_level == 'h1':
                    note['Chapter'] = str(head)
                elif head_level == 'h2':
                    note['Section'] = str(head)
                    note['Chapter'] = str(head.find_previous_sibling('h1'))
                elif head_level == 'h3':
                    note['Subsection'] = str(head)
                    note['Section'] = str(head.find_previous_sibling('h2'))
                    note['Chapter'] = str(head.find_previous_sibling('h1'))

                traceback = [note['Chapter'], note['Section'], note['Subsection']]
                note['root'] = ''.join(s for s in traceback if s)

                # Attention: .next_sibling will return None
                next_sibling = head.find_next_sibling()
                while next_sibling:
                    logging.debug(next_sibling)
                    if next_sibling.name in head_levels:
                        break
                    elif next_sibling.name == 'hr':
                        break
                    # elif next_sibling.name == 'blockquote':
                    elif next_sibling.name in ['p', 'ol', 'ul']:
                        note['Text'] += str(next_sibling)
                    else:
                        break
                    next_sibling = next_sibling.find_next_sibling()

                # get deck and model
                deck_id: DeckId = mw.col.decks.id(deck_name)  # Find or Create if not exist
                # add note to deck, and the note object will get assigned with id
                mw.col.add_note(note, deck_id)
                logging.info(f'Note added, note.id: {note.id}')
