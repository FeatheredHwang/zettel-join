"""
For test convenience:
- add a parallel "kb join test" to the tools menu
- reset test kb and then join it as soon as Anki opened
"""

import logging
import os
import shutil

from aqt import mw, gui_hooks
from aqt.qt import QAction, qconnect

from . import kb

logging.debug(f'CWD - current working directory: {os.getcwd()}')

TEST_MODE: bool = True
TEST_KB_DIR = r'D:\Projects\.test\KB-test'


def reset_test_kb():
    """
    Replace all the test md files in KB, with the original
    """
    for root, dirs, files in os.walk(TEST_KB_DIR):
        if root.endswith('.backup'):
            for file in files:
                # Copy a file, replace if destination file already exist
                if file.endswith('.md'):
                    shutil.copy(
                        os.path.join(root, file),
                        os.path.join(os.path.dirname(root), file)
                    )


def kb_join_test():
    """
    Join your TEST knowledge base to Anki
    """
    # remove all the models
    mm = mw.col.models
    mm.remove(mm.id_for_name('Cloze (traceable) (test)'))
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
    gui_hooks.profile_did_open.append(kb_join_test)

    # add kb_join_test to the tools menu
    action = QAction('KB Join (test)', mw)
    qconnect(action.triggered, kb_join_test)
    mw.form.menuTools.addAction(action)

    # add output_model to the tools menu
    action = QAction('output Model (test)', mw)
    qconnect(action.triggered, output_model)
    mw.form.menuTools.addAction(action)
