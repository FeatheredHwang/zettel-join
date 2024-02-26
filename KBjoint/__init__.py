import os
import logging

from aqt import mw
# from aqt.qt import *
from aqt.qt import QFileDialog, QAction, qconnect
# from aqt.utils import showInfo, askUser
from aqt.utils import showInfo
from anki.hooks import addHook

from .treejoint import TreeJoint

# Logging set up
##################################################

# Set the working directory to the current Python script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(os.getcwd(), 'default.log')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_file_path,
                    filemode='w')
# log the module's directory
logging.info(f'logger file path: {log_file_path}')
print(f'logger file path: {log_file_path}')

# import modules after logging setup
##################################################
# import test module if exist
try:
    from .test import *
except ImportError:
    logging.info("test module doesn't exist.")


# add hook to crete note
##################################################

def build_models():
    TreeJoint.build_model()
    # If there are other type of joint/model, put them here


# TODO learn more about hook, how many kinds of hook exist
addHook("profileLoaded", build_models)


# Add menu item
##################################################

def kb_join() -> None:
    """
    Join your knowledge base to Anki
    :return: None
    """
    # for read-friendly
    _kb_join()


# create a new menu item, "test"
action = QAction('KB Join', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, kb_join)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


def _kb_join() -> None:
    """
    Join your knowledge base to Anki
    :return: None
    """

    # Set the working directory to the path of current Python script
    #   used to find template files by absolute path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logging.info(f'Current working directory is: {os.getcwd()}')

    # Get the top-level directory to traverse
    top_directory = QFileDialog.getExistingDirectory(mw, 'Open', directory=os.path.expanduser("~"))
    # todo!!! open the last-opened directory
    # TODO check if KB-folder or not, what if we open a sub-directory of the top-directory
    # if not askUser("blahblah"):
    #     pass
    #     return
    # else:
    #     pass
    logging.info(f'chosen root directory of your knowledge base : {top_directory}')

    # TODO leave the file traverse job to joint
    #   and include joint's file analyse - if suitable for this model/joint

    # todo: Popup a process bar to show the process
    # and stop user doing anything else before importation done.
    # mw.progress.start(max=1, parent=mw)
    # Processing...
    # mw.progress.update()
    # mw.progress.finish()

    # Traverse the directory tree using os.walk()
    for root, dirs, files in os.walk(top_directory):

        # Filter out hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # Calculate the relative path of the current directory
        relative_root = os.path.relpath(root, top_directory)

        # replace os.sep with '::' as deck's name
        deck_name = relative_root.replace(os.sep, '::')
        logging.debug(f'Create deck name using relative directory path: `{deck_name}`')

        for file in files:
            # judge if a file is a Markdown (.md) file
            if file.endswith('.md'):
                logging.debug(f'Inside the directory a md file found: `{file}`')
                TreeJoint.parse(str(os.path.join(root, file)), str(deck_name))

    # todo using message show parse result
    showInfo('Import succeed. __How Many__')

    # With notes added, refresh the deck browser
    mw.deckBrowser.refresh()
    # todo refresh the notesBrowser window, show the last added notes
