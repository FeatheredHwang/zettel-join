"""
For test convenience:
- add a parallel "kb join test" to the tools menu
- reset test kb and then join it as soon as Anki opened
"""

import dotenv
import logging
import os
import pathlib
import shutil

from aqt import mw, gui_hooks
from aqt.qt import QAction, qconnect

from .. import kb


logger = logging.getLogger(__name__)
logger.debug(f'CWD: {os.getcwd()}')

TEST_MODE: bool = True
dotenv.load_dotenv('./.env')  # loading variables from .env file
test_kasten_path = os.getenv('TEST_KASTEN_PATH')
addon_path = os.getenv('ADDON_PATH')


def reset_test_kb():
    """
    Replace all the test md files in KB, with the original
    """
    # delete all the dirs except the hidden ones
    for d in os.listdir(test_kasten_path):
        if not d.startswith('.'):
            shutil.rmtree(os.path.join(test_kasten_path, d), ignore_errors=True)
    # Add example MDs to the test kasten
    dst_path = pathlib.Path(os.path.join(test_kasten_path, 'About this addon/MD examples'))
    dst_path.mkdir(parents=True, exist_ok=True)  # create dir if path not exist
    src_path = os.path.join(addon_path, 'ex')
    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)  # overwrite if file exists
    # Add sync-test MDs to the test kasten
    dst_path = pathlib.Path(os.path.join(test_kasten_path, 'sync-test/pre-edit'))
    dst_path.mkdir(parents=True, exist_ok=True)
    src_path = os.path.join(addon_path, 'test/sync-test')
    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)


def do_file_edit():
    """
    Update the sync-test md files in filepath level.
    """
    # copy directory
    dst_path = pathlib.Path(os.path.join(test_kasten_path, 'sync-test/post-edit'))
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    src_path = os.path.join(test_kasten_path, 'sync-test/pre-edit')
    os.rename(src_path, dst_path)
    # move & rename a file
    os.rename(os.path.join(dst_path, 'pre-modify[cloze].md'),
              os.path.join(dst_path, 'post-modify[cloze].md'))
    # delete a file
    os.remove(os.path.join(dst_path, 'pre-delete[cloze].md'))
    # add a file
    os.rename(os.path.join(dst_path, '.post/post-add[cloze].md'),
              os.path.join(dst_path, 'post-add[cloze].md'))


def md2notes_sync():
    """
    Update the sync-test md files in all levels.
    """
    do_file_edit()


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
    logger.info('\n' +
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

    # add 'md2notes sync (test)' to the tools menu
    action = QAction('md2notes sync (test)', mw)
    qconnect(action.triggered, md2notes_sync)
    mw.form.menuTools.addAction(action)
