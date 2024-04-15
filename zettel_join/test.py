"""
For test convenience:
- add a parallel "kb join test" to the tools menu
- reset test kb and then join it as soon as Anki opened
"""

import logging
import os
import pathlib
import shutil

from .lib import dotenv

from aqt import mw, gui_hooks
from aqt.qt import QAction, qconnect

from . import kb

logging.debug(f'CWD - current working directory: {os.getcwd()}')

# loading variables from .env file
dotenv.load_dotenv()

TEST_MODE: bool = True
test_kasten_path = os.getenv('TEST_KASTEN_PATH')
md_ex_path = os.getenv('MD_EX_PATH')


def reset_test_kb():
    """
    Replace all the test md files in KB, with the original
    """
    ex_dst_path = pathlib.Path(os.path.join(test_kasten_path, 'About this addon/MD examples/.backup'))
    # if path not exist, create it
    ex_dst_path.mkdir(parents=True, exist_ok=True)
    # copy MD examples from the project dir
    for root, dirs, files in os.walk(md_ex_path):
        for file in files:
            # Copy a file, replace if destination file already exist
            shutil.copy(
                os.path.join(root, file),
                os.path.join(ex_dst_path, file)
            )
    # replace test files with the backup
    for root, dirs, files in os.walk(test_kasten_path):
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
    kb.KnowledgeBase(top_dir=test_kasten_path, test_mode=TEST_MODE).join()


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

    # delete test models after we open Anki
    gui_hooks.profile_did_open.append(remove_test_models)
    # delete test models before we close Anki
    gui_hooks.profile_will_close.append(remove_test_models)

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
