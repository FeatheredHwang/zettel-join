"""
Zip up the add-on and giving it a name ending in '.ankiaddon'.
"""

import shutil

if __name__ == '__main__':
    shutil.make_archive('KBjoint.ankiaddon', 'zip', '../KBjoint')
