import logging
import os
import json
from typing import Any


from aqt import mw, gui_hooks


# todo Config set up
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
