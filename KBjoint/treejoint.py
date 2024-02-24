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

import os
import logging

# import all the Qt GUI library
# import the "show info" tool from utils.py
# from aqt.utils import showInfo
from anki.models import ModelManager, NotetypeDict, TemplateDict
from aqt import mw

from .joint import Joint


class TreeJoint(Joint):
    """
    A joint to import md files to TopicTree model.
    """
    pass

    MODEL_NAME = 'TopicTree'
    SUBTOPIC_AMOUNT: int = 6
    TEMPLATE_PLACEHOLDER: str = '%n'

    @classmethod
    def build_model(cls):
        """
        Build the custom model
        :Return: NotetypeDict
        """

        # Using model manager is the only way to add new model
        mm: ModelManager = mw.col.models
        t: TemplateDict

        m: NotetypeDict = mw.col.models.byName(cls.MODEL_NAME)
        if m:
            # TODO How to update the model? Using version to keep user's custom changes
            logging.info(f'NoteType {m["name"]} already exist, skip building')
            return
        logging.info(f'Building NoteType <{cls.MODEL_NAME}> ...')

        m = mm.new(cls.MODEL_NAME)

        # Set the working directory to the path of current Python script
        #   used to find template files by absolute path
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        logging.debug(f'Current working directory is: {os.getcwd()}')

        # Add MainTopic fields and Card
        for fld in ['MainTopic', 'MainTopicBody', 'Extra']:
            mm.addField(m, mm.newField(fld))
        t = mm.newTemplate('MainTopic')
        t['qfmt'] = cls.read_file('templates/main-front.html')
        t['afmt'] = cls.read_file('templates/main-back.html')
        mm.addTemplate(m, t)
        logging.debug(f'Template <{t["name"]}> added to the notetype <{m["name"]}>')

        # Add Subtitle fields and Cards
        qfmt: str = cls.read_file('templates/sub-front.html')
        afmt: str = cls.read_file('templates/sub-back.html')
        for n in range(cls.SUBTOPIC_AMOUNT):

            n = n + 1  # range(n) returns a num list [0,1,...,n-1]
            for fld in ['Subtopic_{}', 'SubtopicBody_{}']:
                mm.addField(m, mm.newField(fld.format(n)))

            t = mm.new_template(f'Subtopic {n}')
            t['qfmt'] = qfmt.replace(cls.TEMPLATE_PLACEHOLDER, str(n))
            t['afmt'] = afmt.replace(cls.TEMPLATE_PLACEHOLDER, str(n))
            mm.addTemplate(m, t)
            logging.debug(f'Template <{t["name"]}> added to the notetype <{m["name"]}>')

        # Add css
        m['css'] = cls.read_file('templates/css.css')

        # Add the Model (NoteTypeDict) to Anki
        mm.add_dict(m)
        logging.info(f'NoteType <{m["name"]}> added to Anki')

    @classmethod
    def parse_file(cls):
        """
        Parse the md file and import its content
        """
        # get deck and model
        # deck_name = 'test'
        # model_name = 'Interpretation (md)'
        #

        # deck = mw.col.decks.by_name(deck_name)
        # model = mw.col.models.by_name(model_name)

        # note = Note(mw.col, model)
        #
        # note['MainTopic'] = 'MainTopic'
        # note['MainTopicBody'] = 'Body'
        # note['Extra'] = 'Extra'
        # note.tags.append('TESTtag')
        #
        # logging.info(f'adding Note, {note.fields}')
        # logging.info(f'_fmap, {note._fmap}')
        # # add note to deck, and the note object will get assigned with id
        # mw.col.add_note(note, deck['id'])
        # logging.info(f'note.id: {note.id}')

        pass
