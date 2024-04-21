"""
Zip up the add-on for sharing purpose.
Please see [the add-on documentation](https://addon-docs.ankiweb.net/sharing.html)
 for information on creating and uploading add-ons.
"""

import os
import shutil


ADDON_DIR_NAME = 'zettel_join'
ADDON_PACKAGE_NAME = f'zettel-join.ankiaddon'


# noinspection PyUnusedLocal
def zip_filter(path: str, names: list[str]) -> list[str]:
    """
    Filter out the test, lib and __pycache__ directory.
    Besides, AnkiWeb can not accept zip files that contain pycache folders.
    :param path: root directory path, as 'root' in 'os.walk'
    :param names: name list of files and dirs
    :return: filtered name list of files and dirs
    """
    filter_out: list[str] = ['__pycache__', 'lib', 'test']
    return [item for item in filter_out if item in names]


if __name__ == '__main__':
    if os.path.exists('build'):
        shutil.rmtree('build')
    shutil.copytree(f'../{ADDON_DIR_NAME}', f'build/{ADDON_DIR_NAME}', ignore=zip_filter)
    shutil.make_archive(f'build/{ADDON_PACKAGE_NAME}', 'zip', f'build/{ADDON_DIR_NAME}')
    shutil.rmtree(f'build/{ADDON_DIR_NAME}')
    os.rename(f'build/{ADDON_PACKAGE_NAME}.zip', f'build/{ADDON_PACKAGE_NAME}')
