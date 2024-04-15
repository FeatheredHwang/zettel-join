"""
Install packages to local libray since they are not included in Anki
"""

import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)


# Register modules/packages Here!
MODULE_MAP: dict[str, str] = {
    # 'module_name': 'package_name',
    'emojis': 'emojis',
    'pymdownx': 'pymdown-extensions',
    'dotenv': 'python-dotenv'
}

# pip options
# -i, --index-url <url>
#   Base URL of the Python Package Index (default https://pypi.org/simple)
INDEX_URL = 'https://mirrors.aliyun.com/pypi/simple'
# -t, --target <dir>
#   Install packages into <dir>. By default, this will not replace existing files/folders in <dir>.
#   Use --upgrade to replace existing packages in <dir> with new versions.
TARGET_DIR = 'lib'


def check_modules():
    """
    check if modules exist, install module if not
    """
    logger.debug(f'CWD: {os.getcwd()}')
    # sys.path contains a list of directories that the interpreter will search in for the required module.
    sys.path.append(os.path.join(os.getcwd(), TARGET_DIR))
    logger.info(f'Import module - add path to sys.path: {sys.path[-1]}')
    # download modules
    for module_name in MODULE_MAP.keys():
        if os.path.exists(os.path.join(TARGET_DIR, module_name)):
            logger.debug(f'Import module - modules already exist: "{module_name}".')
        else:
            logger.info(
                f'Import module - module not found, install package with pip: "{MODULE_MAP[module_name]}".')
            command = ['pip', 'install', '-i', INDEX_URL, '--target', TARGET_DIR, MODULE_MAP[module_name]]
            subprocess.check_call(command)
            # todo not let the command-line show up while install package, and print the output to log
    logger.debug('Import module finished.\n')


check_modules()
