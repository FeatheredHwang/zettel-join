"""
Create a symbolic link of log file in project dir, pointing to it in addon dir
[!Note]
Run the IDE as administrator, then run current script
"""
import os
from dotenv import load_dotenv


load_dotenv('../zettel_join/.env')

src = os.path.join(os.getenv('ADDON_PATH'), 'DEBUG.log')
dst = os.path.join(os.getenv('PROJECT_PATH'), 'DEBUG.log')
os.symlink(src, dst)
print("symlink created")

# it raises "OSError: [WinError 1314] A required privilege is not held by the client" if not run as administrator
# open powershell as administrator, and execute command below:
"""
New-Item -ItemType SymbolicLink -Path "D:/Projects/Anki-addon/zettel-join/.log" -Target "C:/Users/feath/AppData/Roaming/Anki2/addons21/zettel-join/root.log" 
"""
