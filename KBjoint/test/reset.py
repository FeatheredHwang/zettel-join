import os
import shutil


kb_dir = r'D:\Projects\.test\KB-test'


for root, dirs, files in os.walk(kb_dir):
    if root.endswith('.backup'):
        for file in files:
            # Copy a file
            shutil.copy(
                os.path.join(root, file),
                os.path.join(os.path.dirname(root), file)
            )

# Delete a file
# os.remove(file_to_delete)
