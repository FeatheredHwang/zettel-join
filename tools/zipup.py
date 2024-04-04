"""
Zip up the add-on and giving it a name ending in '.ankiaddon'.
"""

import os
import shutil

if __name__ == '__main__':
    shutil.make_archive('KBjoint', 'zip', '../KBjoint')
    os.rename('KBjoint.zip', 'KBjoint.ankiaddon')
