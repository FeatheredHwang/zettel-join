"""
For test convenience:
- add a parallel "kb join test" to the tools menu
- reset test kb and then join it as soon as Anki opened
"""

import logging
import os
import shutil

from .lib import dotenv

from aqt import mw, gui_hooks
from aqt.qt import QAction, qconnect

from . import kb

logging.debug(f'CWD - current working directory: {os.getcwd()}')

# loading variables from .env file
dotenv.load_dotenv()

TEST_MODE: bool = True
TEST_KB_DIR = os.getenv('TEST_KB_DIR')
PROJECT_DOC_DIR = os.getenv('PROJECT_DOC_DIR')


def reset_test_kb():
    """
    Replace all the test md files in KB, with the original
    """
    # copy doc files from the project dir
    for root, dirs, files in os.walk(PROJECT_DOC_DIR):
        for file in files:
            # Copy a file, replace if destination file already exist
            shutil.copy(
                os.path.join(root, file),
                os.path.join(TEST_KB_DIR, 'About this addon/doc/.backup', file)
            )
    for root, dirs, files in os.walk(TEST_KB_DIR):
        if root.endswith('.backup'):
            for file in files:
                if file.endswith('.md'):
                    shutil.copy(
                        os.path.join(root, file),
                        os.path.join(os.path.dirname(root), file)
                    )


def remove_test_models():
    """
    remove all the models
    """
    mm = mw.col.models
    mm.remove(mm.id_for_name('Cloze (traceable) (test)'))
    mm.remove(mm.id_for_name('Oneside (test)'))


def join_test_kb():
    """
    Join your TEST knowledge base to Anki
    """
    kb.KnowledgeBase(top_dir=TEST_KB_DIR, test_mode=TEST_MODE).join()


def output_model():
    """
    logging model dictionary for look-through convenience
    # todo write to file rather than logging, do not use logging in test modules
    """
    logging.info('\n' +
                 str(mw.col.models.by_name('Cloze traceable (test)'))
                 )


if TEST_MODE:
    # reset test kb each time while we open ANki
    gui_hooks.profile_did_open.append(reset_test_kb)

    # join test kb as soon as Anki opened
    gui_hooks.profile_did_open.append(join_test_kb)

    # add kb_join_test to the tools menu
    action = QAction('KB Join (test)', mw)
    qconnect(action.triggered, join_test_kb)
    mw.form.menuTools.addAction(action)

    # add output_model to the tools menu
    action = QAction('output Model (test)', mw)
    qconnect(action.triggered, output_model)
    mw.form.menuTools.addAction(action)
else:
    # delete test models after we open Anki
    gui_hooks.profile_did_open.append(remove_test_models)
