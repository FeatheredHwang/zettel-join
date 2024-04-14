"""
Update Addon files
"""

import os
import shutil
# using env to protect private information like filepath
# to learn how to use it: https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

# load variables from .env file
load_dotenv('../zettel_join/.env')
addon_path = os.getenv('ADDON_PATH')
anki_path = os.getenv('ANKI_PATH')

# close Anki if the process exists (mpv is one of Anki's process, which will occupy addon folder)
os.system("""tasklist | find /i "anki.exe" && ( taskkill /im "anki.exe" /f )""")
os.system("""tasklist | find /i "mpv.exe" && ( taskkill /im "mpv.exe" /f )""")


def ignore_pycache(path, names):
    # Filter out the __pycache__ directory
    return ['__pycache__'] if '__pycache__' in names else []


# Update Addon files
if os.path.exists(addon_path):
    # use the rmtree() function to delete a folder that is not empty
    shutil.rmtree(addon_path)
    print(f'SUCCESS: The Addon directory {addon_path} has been deleted.')
# overwrite if des exists
shutil.copytree('../zettel_join', addon_path, dirs_exist_ok=True, ignore=ignore_pycache)
print(f'SUCCESS: The Addon directory {addon_path} has been copied.')

# open Anki
os.system(f""" start "" "{anki_path}" """)
