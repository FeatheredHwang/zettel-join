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
    def parse(cls, file: str) -> list[int]:
        """
        Parse the file content, map them on the model,
        then add/join them to collection.
        :param file: filepath
        :rtype: list[int]
        :return: list of id to the created notes
        """
        pass

    @classmethod
    def verify(cls, file: str) -> bool:
        """
        check if the file appropriate for the model
        :param file: filepath
        :rtype: bool
        :return: appropriate or not
        """
        pass

    @staticmethod
    def read_file(file: str) -> str:
        """
        Open the file path and read the file content
        :param file: filepath
        :return: file content
        """

        try:
            # Attempt to open the file
            with open(file, 'r', encoding='utf-8') as file:
                # Read the entire content of the file
                file_content = file.read()
                logging.debug(f"File <{file}> read successfully.")
                return file_content

        except FileNotFoundError:
            logging.error(f"File <{file}> not found. Please make sure the file exists.")
        except IOError as e:
            logging.error("An error occurred while reading the file:", e)

        return ''
