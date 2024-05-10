"""
Create a symbolic link of log file in project dir, pointing to it in addon dir
[!Note]
Run the IDE as administrator, then run current script
"""
import os
from dotenv import load_dotenv


load_dotenv('../zettel_join/test/.env')

src = os.path.join(os.getenv('ADDON_PATH'), 'DEBUG.log')
dst = os.path.join(os.getenv('PROJECT_PATH'), 'DEBUG.log')
os.symlink(src, dst)
print("DEBUG.log symlink created")

# if it raises "OSError: [WinError 1314] A required privilege is not held by the client",
#   you should reopen IDE as administrator
