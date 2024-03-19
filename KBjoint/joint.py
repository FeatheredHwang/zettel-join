# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import logging
import sys
import re
from typing import Union

from anki.notes import NoteId

# import markdown2 from the local libray, cause Anki doesn't include this module
try:
    from .Lib import markdown2
    # TODO markdown2 parser doesn't support latex
    # todo markdown2 parser doesn't support :star: (emoji)
except ImportError as import_error:
    logging.warning(f'"markdown2" module not found, exit: {import_error}')
    sys.exit()

from bs4 import BeautifulSoup, Tag, Comment


class Joint:
    """
    A joint is consisted of:
        a model (where the knowledge points are mapped on)
        and join-function (import, output, etc. e.g.file-parsing)
    """

    MODEL_NAME: str

    @classmethod
    def build_model(cls) -> int:
        """
        Build up the model
        :rtype: int
        :return: id of the (created/exist) model
        """
        pass

    @classmethod
    def verify(cls, filepath: str) -> bool:
        """
        check if the file appropriate for the model
        :param filepath: filepath
        :rtype: bool
        :return: appropriate or not
        """
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
        pass

    @staticmethod
    def read_file(filepath: str) -> str:
        """
        Open the file and read the file content.

        :param filepath: The path of the file to read from.
        :return: The content of the file.
        """

        try:
            # Attempt to open the file
            with open(filepath, 'r', encoding='utf-8') as f:
                # Read the entire content of the file
                file_content = f.read()
                logging.debug(f"File <{filepath}> read successfully: {file_content[:20]}")
                return file_content

        except FileNotFoundError:
            logging.error(f"File <{filepath}> not found. Please make sure the file exists.")
        except IOError as e:
            logging.error("An error occurred while reading the file:", e)

        return ''

    @staticmethod
    def write_file(content: str, filepath: str):
        """
        Write content to a file.
        
        :param content: The content to write to the file.
        :type content: str
        :param filepath: The path of the file to write to.
        :type filepath: str
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Success writing to {filepath}.")
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")


def read_file(file: str) -> str:
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
            logging.debug(f"File read successfully:  {file}")
            return file_content
    except FileNotFoundError:
        logging.error(f"File read error - File not found:  {file}")
    except IOError as e:
        logging.error("File read error: ", e)

    return ''


def write_file(file: str, content: str):
    """
    Write content to a file.

    :param content: The content to write to the file.
    :type content: str
    :param file: The path of the file to write to.
    :type file: str
    """
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Success writing to {file}.")
    except Exception as e:
        print(f"Error writing to {file}: {e}")


def get_soup(file: str) -> BeautifulSoup:
    md_content = read_file(file)
    content = markdown2.markdown(md_content)
    soup = BeautifulSoup(content, "html.parser")
    return soup


def get_sibling_comment(tag: Tag) -> Union[Comment, None]:
    """
    Get the comment right after the current tag
    :param tag:
    :return:
    """
    sib = tag.next_sibling
    while sib and isinstance(sib, str) and not isinstance(sib, Comment):
        sib = sib.next_sibling
        if isinstance(sib, Tag):
            return None
    return sib


def get_commented_noteid(heading: Tag) -> Union[NoteId, None]:
    """
    Get the noteid from comment right after the heading tag
    :param heading:
    :return:
    """
    comm = get_sibling_comment(heading)
    if not comm:
        return None
    m = re.fullmatch(r'\s*NoteId:\s*(?P<note_id>[0-9]{13})\s*', comm, flags=re.IGNORECASE)
    note_id = NoteId(m.group('note_id')) if m else None
    return note_id
