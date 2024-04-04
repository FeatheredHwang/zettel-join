"""
Zip up the add-on and giving it a name ending in '.ankiaddon'.
"""

import os
import shutil

ADDON_NAME = 'KBjoint'
ADDON_PACKAGE_NAME = f'{ADDON_NAME}.ankiaddon'

# !IMPORTANT! assign 'TEST_MODE' to False before zipup

if __name__ == '__main__':
    if os.path.exists(ADDON_PACKAGE_NAME):
        os.remove(ADDON_PACKAGE_NAME)
    shutil.make_archive(f'{ADDON_PACKAGE_NAME}', 'zip', f'../{ADDON_NAME}')
    os.rename(f'{ADDON_PACKAGE_NAME}.zip', f'{ADDON_PACKAGE_NAME}')
