import json
import logging
import os
from typing import Any

from aqt import gui_hooks
from aqt import mw
# from aqt.qt import *
from aqt.qt import QFileDialog, QAction, qconnect
from aqt.utils import showInfo, askUser

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
logging.info(f'Logging file path: {log_file_path}')

# Config set up
##################################################
# legacy type
ConfigDict = dict[str, Any]

config: ConfigDict = {}


def load_json_config():
    """
    Load previous config from json file
    """
    config_json_file: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'config@{mw.pm.name.replace(" ", "-")}.json'
    )

    global config
    if os.path.exists(config_json_file):
        with open(config_json_file) as f:
            config = json.load(f)
        logging.info(f'Config File Found: {os.path.basename(config_json_file)}\n'
                     f'The earlier configs: \n{json.dumps(config)}')
    else:
        config = {
            'config_json_file': config_json_file,
        }
        logging.info(f'Config File Not Found: {config_json_file}')


def save_json_config():
    """
    Write present config to json file
    """
    with open(config['config_json_file'], 'w') as f:
        f.write(json.dumps(config, indent=4))


gui_hooks.profile_did_open.append(load_json_config)
gui_hooks.profile_will_close.append(save_json_config)


# import test modules if exist
##################################################
try:
    from .test import *
except ImportError:
    logging.info("test module doesn't exist.")


# add hook to crete note
##################################################

def build_models():
    TreeJoint.build_model()
    # If there are other type of joint/model, put them here


gui_hooks.profile_did_open.append(build_models)


# Add menu item
##################################################

def kb_join():
    """
    Join your knowledge base to Anki
    """
    # for read-friendly
    _kb_join()


# create a new menu item
action = QAction('KB Join', mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, kb_join)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


# KB join function
##################################################


def _kb_join():
    """
    Join your knowledge base to Anki
    :return: None
    """

    logging.info('================================\n'
                 'Trying to open KB dir.')
    top_dir = open_kb_dir()
    if not top_dir:
        logging.warning('Opening KB dir cancelled, no cards imported.\n'
                        '================================================================')
        return

    # TODO leave the file traverse job to joint
    #   and include joint's file analyse - if suitable for this model/joint

    # todo: Popup a process bar to show the process
    # and stop user doing anything else before importation done.
    # mw.progress.start(max=1, parent=mw)
    # Processing...
    # mw.progress.update()
    # mw.progress.finish()

    # Traverse the directory tree using os.walk()
    for root, dirs, files in os.walk(top_dir):

        # Filter out hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # Calculate the relative path of the current directory
        relative_root = os.path.relpath(root, top_dir)

        # replace os.sep with '::' as deck's name
        deck_name = relative_root.replace(os.sep, '::')
        logging.debug(f'Create deck name using relative directory path: `{deck_name}`')

        for file in files:
            # judge if a file is a Markdown (.md) file
            if file.endswith('.md'):
                logging.debug(f'Inside the directory a md file found: `{file}`')
                TreeJoint.parse(str(os.path.join(root, file)), str(deck_name))

    logging.warning('__How Many__ notes imported.\n'
                    '================================================================')
    # todo using message show parse result
    showInfo('__How Many__ notes imported')

    # With notes added, refresh the deck browser
    mw.deckBrowser.refresh()
    # todo open the notesBrowser window, show the last added notes


def open_kb_dir() -> str | None:
    """
    Get KB directory to traverse
    :return: The directory path of chosen
    """
    try:
        init_dir = config['last_top_dir']
    except KeyError:
        init_dir = os.path.expanduser("~")
    # noinspection PyTypeChecker
    top_directory = QFileDialog.getExistingDirectory(
        mw,
        'Open the Knowledge Base Directory',
        directory=init_dir
    )

    # check if user cancelled selection
    if not top_directory:
        logging.info('Opening KB directory cancelled.')
        return None

    # save config
    config['last_top_dir'] = top_directory

    # check if KB-folder or not, in case we open a sub of the top-directory
    if not os.path.exists(os.path.join(top_directory, 'ROOT')):
        if askUser("The directory you choose do not contain KB 'ROOT' file inside.\n"
                   "Choose again? "):
            open_kb_dir()
        else:
            logging.info('Opening KB directory cancelled.')
            return None

    logging.info(f'Chosen root directory of your knowledge base : {top_directory}')
    return top_directory
