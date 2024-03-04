# -*- coding: utf-8 -*-
# Copyright: Kyle Hwang <feathered.hwang@hotmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import logging


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
