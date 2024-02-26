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
    def verify(cls, filepath: str) -> bool:
        """
        check if the file appropriate for the model
        :param filepath: filepath
        :rtype: bool
        :return: appropriate or not
        """
        # In advance, check if only one h1 exist

        # Then, check h2 amount at least 1
        # h2_tags = soup.find_all('h2')
        # h2_count = len(h2_tags)
        # if not h2_count:
        #     logging.warning('Cannot find any note(h2 tag), please check your original MD file.')
        #     # return
        #     exit(1)
        # else:
        #     logging.debug(f'{h2_count} h2-tag(s) found')

        # TODO verify function
        #   check if note id comment exist
        #   if subtopics' count more than 6?
        #   ...

        pass

    @classmethod
    def parse(cls, filepath: str, deck_name: str) -> list[int]:
        """
        Parse the file content, map them on the model,
        then add/join them to collection.
        :param deck_name: deck name that generated from file path
        :type deck_name: str
        :param filepath: filepath
        :rtype: list[int]
        :return: list of id to the created notes
        """

        # Inspect your target HTML
        md_content = cls.read_file(filepath)
        content = markdown2.markdown(md_content)
        soup = BeautifulSoup(content, "html.parser")

        new_note_ids = []
        h1_content = soup.h1.text + '－'

        h2_tags = soup.find_all('h2')
        h2_count = len(h2_tags)
        logging.debug(f'{h2_count} h2-tag(s) found')

        # find if NoteType comment exist
        comm = soup.find(string=lambda text: isinstance(text, Comment))
        if comm and soup.index(comm) < soup.index(soup.find()):
            m = re.match(r'\s*NoteType:\s*(?P<notetype>\w+)\s*', comm)
            if not m:
                logging.warning(f'Unexpected comment found: <!--{comm}-->')
            else:
                # notetype_name = m.group('notetype')
                # TODO: check if it is the same as this joint, using model ID
                logging.info(f'NoteType comment found: <!--{comm}-->')
        else:
            # there must be two '\n' at the end of the pattern,
            #  or the comment will be parsed as part of next element,
            #  and soup.index(comm) will report: 'element not in tag'
            md_content = re.sub('^', f'\n<!-- NoteType: {cls.MODEL_NAME} -->\n\n', md_content)
            logging.debug('No comment found at the beginning of the soup, NoteType commented ')

        # Then, find all the sibling tags previous to the first h2 tag (MainTopic field)
        #   where are supposed to contain the previous note_tag paragraph and extra blockquote that shared between notes
        tags = []
        extra = ''
        for sibling in h2_tags[0].find_previous_siblings():
            if not sibling:
                break

            if sibling.name == 'p' \
                    and re.fullmatch(r'Tags:\s*', sibling.contents[0], flags=re.IGNORECASE):
                # Parse the tags field
                for code in sibling.find_all('code', recursive=False):
                    # note.tags.append(code.text)
                    tags.append(code.text)
                logging.debug(f'Tags updated: {tags}')

            elif sibling.name == 'blockquote':
                # Parse the 'Extra' field (blockquote tag before h1)
                extra += str(soup.blockquote)
                logging.debug('Extra field updated: {}'.format(extra.replace('\n', '')[:30]))
            else:
                logging.warning(f'Unexpected tag when parsing: {sibling}')

        # Later, parse each h2 tag and its next siblings as its content
        for h2_index in range(h2_count):

            logging.info(f'h2_tags[{h2_index}] parsing start')

            # look up comment and see if note_id included
            comm = h2_tags[h2_index].find_next_sibling(string=lambda text: isinstance(text, Comment))
            if comm and soup.index(comm) < soup.index(h2_tags[h2_index].find_next_sibling()):

                m = re.fullmatch(r'\s*NoteId:\s*(?P<note_id>\w+)\s*', comm, flags=re.IGNORECASE)

                if m:
                    logging.info(f'NoteId comment found: <!--{comm}-->, note already imported, skip import.')
                    note_id = m.group('note_id')
                    new_note_ids.append(note_id)
                    continue
                    # TODO get note by id, then compare and update note
                else:
                    logging.warning(f'Unexpected comment found: <!--{comm}-->')
            else:
                logging.debug(f'No comment found behind the h2 tag: {h2_tags[h2_index]}')

            # Create a note
            note = Note(mw.col, mw.col.models.by_name(cls.MODEL_NAME))

            # Pass h2 text for note_id comment
            h2_txt = h2_tags[h2_index].text
            # Connect h1 and h2 value as MainTopic field
            h2_tags[h2_index].string.insert_before(h1_content)

            topic_field = 'MainTopic'
            body_field = 'MainTopicBody'
            note[topic_field] = str(h2_tags[h2_index])
            note[body_field] = ''

            logging.debug(f'{topic_field} added: {note[topic_field]}')

            # find all the sibling tags next to h1 tag (MainTopic field)
            h3_index = 0
            for sibling in h2_tags[h2_index].find_next_siblings():

                if sibling.name == 'h3':
                    h3_index += 1

                    topic_field = f'Subtopic_{h3_index}'
                    body_field = f'SubtopicBody_{h3_index}'

                    note[topic_field] = str(sibling)
                    note[body_field] = ''

                    logging.debug(f'{topic_field} added: {note[topic_field]}')

                elif sibling.name == 'blockquote':
                    # 'blockquote' tag belongs to 'topicHint' field when after heading
                    # for now, skip this tag
                    logging.debug('Hint field skipped: {}'.format(str(sibling).replace('\n', '')[:30]))

                elif sibling.name in ['h2', 'hr']:
                    # which means we get to the end of the note
                    logging.debug('reach the end of this note')
                    break

                else:
                    note[body_field] += str(sibling)
                    logging.debug('{field} updated: {content}'.format(
                        field=body_field, content=note[body_field].replace('\n', '')[:30]
                    ))

            logging.info(f'h2_tags[{h2_index}] parsing finish')

            # get deck and model
            deck_id: DeckId = mw.col.decks.id(deck_name)  # Find or Create if not exist
            logging.info(f'TEMP| deck_id: {deck_id}')
            note['Extra'] = extra
            logging.debug('Extra field added: {}'.format(note['Extra'][:30]))
            note.tags = tags
            logging.debug('Tags added: {}'.format(note.tags))

            # add note to deck, and the note object will get assigned with id
            mw.col.add_note(note, deck_id)
            logging.info(f'Note added, note.id: {note.id}')
            # todo make the note imported un-editable,
            #  but able to open the associated md file and update note after close the file.

            md_content = re.sub(
                # there must be two '\n' at the end of the pattern,
                #  or the comment will be parsed as part of next element
                r'(\n##\s*{}\s*\n\n)'.format(h2_txt),
                r'\1' + f'\n<!-- NoteId: {note.id} -->\n',
                md_content)
            logging.debug(f'Note-id commented after h2 "{h2_txt}"')

            new_note_ids.append(note.id)

        cls.write_file(md_content, filepath)

        return new_note_ids
