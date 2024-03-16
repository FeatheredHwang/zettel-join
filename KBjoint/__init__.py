import json
import logging
import os
from typing import Any, Union

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

# for test convenience, add the model while profile opened
gui_hooks.profile_did_open.append(TreeJoint.build_model)


# Add 'KB Join' menu item
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

    top_dir = open_kb_dir()
    if not top_dir:
        logging.warning('Opening KB dir: empty dir path, no cards imported.\n')
        return
    else:
        logging.info(f'\nThe KB located at {top_dir}')

    # TODO using GitPython to monitor changes and record each file's notetype

    # todo: Popup a process bar to show the process
    #   and stop user doing anything else before importation done.
    # mw.progress.start(max=1, parent=mw)
    # # Processing...
    # mw.progress.update()
    # mw.progress.finish()

    # TODO leave the file traverse job to joint
    #   and include joint's file analyse - if suitable for this model/joint

    # Calculate how many cards imported
    new_notes_count = 0

    # Traverse the directory tree using os.walk()
    for root, dirs, files in os.walk(top_dir):

        # Filter out hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # Calculate the relative path of the current directory
        relative_root = os.path.relpath(root, top_dir)

        # replace os.sep with '::' as deck's name
        deck_name = relative_root.replace(os.sep, '::')
        # TODO only take two levels of the dir path
        # todo 'part' for the third level of dir path
        logging.debug(f'Create deck name using relative directory path: `{deck_name}`')

        for file in files:
            # if a file is marked, mark the notes too.
            if file.startswith('⭐'):
                logging.info('important notes found')
            # judge if a file is a Markdown (.md) file
            if file.endswith('.md'):
                logging.debug(f'Inside the directory a md file found: `{file}`')
                new_notes_count += len(TreeJoint.parse(str(os.path.join(root, file)), str(deck_name)))

    # todo using message show parse result
    logging.info(f'{new_notes_count} notes imported.\n'
                 '================================================================')
    showInfo(f'{new_notes_count} notes imported')

    # With notes added, refresh the deck browser
    mw.deckBrowser.refresh()
    # todo open the notesBrowser window, show the last added notes


# The | symbol for type hinting is introduced in Python 3.10 and later versions.
# For now, Anki uses Python 3.9
# def open_kb_dir() -> str | None:
def open_kb_dir() -> Union[str, None]:
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
        logging.info('Opening KB dir: cancelled')
        return

    # save config
    config['last_top_dir'] = top_directory

    # check if KB-folder or not, in case we open a sub of the top-directory
    if not os.path.exists(os.path.join(top_directory, 'ROOT')):
        logging.info("Opening KB dir: dir not valid - 'ROOT' file missing, ask user for choose-again")
        if askUser("The directory you choose does not contain KB 'ROOT' file inside.\n"
                   "Choose again? "):
            return open_kb_dir()
        else:
            logging.info('Opening KB dir: choose-again cancelled.')
            return

    logging.info(f'Opening KB dir: dir valid, shown below \n  {top_directory}')
    return top_directory
