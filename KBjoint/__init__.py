import os
import logging

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

# TODO rename the project to KBjoint

# TODO markdown2 parser doesn't support latex

# TODO Write a markdown2 extension:
#  markdown2 parser transfer two blank lines (in markdown file) into a blank line (in html file)

# TODO Markup the deck is connected to my knowledge-base and note is associated with knowledge base

# TODO make the note imported un-editable, but able to open the associated md file and update note after close the
#  file.

# TODO: Popup a process bar to show the process
# and stop user doing anything else before importation done.
# mw.progress.start(max=1, parent=mw)
# Processing...
# mw.progress.update()
# mw.progress.finish()


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
try:
    from .treejoint import TreeJoint
except ImportError:
    logging.info("joint module doesn't exist.")

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
    # TODO check if KB-folder or not
    logging.info(f'the knowledge base root directory you chosen: {top_directory}')

    # Traverse the directory tree using os.walk()
    for root, dirs, files in os.walk(top_directory):

        # Filter out hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # Calculate the relative path of the current directory
        relative_root = os.path.relpath(root, top_directory)

        for file in files:
            # TODO import joint's file analyse - if suitable for me
            # judge if a file is a Markdown (.md) file
            if file.endswith('.md'):
                # Calculate the relative path of each file
                relative_file_path = os.path.join(relative_root, file)
                # replace os.sep with '::' as deck's name
                deck_name = relative_root.replace(os.sep, '::')
                logging.debug(f'Found a md file: <{file}> with deck name <{deck_name}>')
                # TODO parse the file with TopicTree

    # With notes added, refresh the deck browser
    mw.deckBrowser.refresh()
    # TODO refresh the notesBrowser window
