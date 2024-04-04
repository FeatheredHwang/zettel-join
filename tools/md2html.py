"""
Transfer markdown files to html for parse convenience,

while using env to protect private information like filepath,
for details: https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/
"""
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv

import markdown
from markdown import Extension
from pymdownx.emoji import EmojiExtension, to_alt
from pymdownx.arithmatex import ArithmatexExtension

# loading variables from .env file
load_dotenv()


def transfer_mds_to_htmls():
    """
    Transfer markdown files to html for parse convenience
    """
    kb_dir = os.getenv("TEST_KB_DIR")

    extensions: list[Extension] = []

    # add emoji extension
    emoji_extension = EmojiExtension()
    emoji_extension.config['emoji_generator'] = [to_alt, '']
    extensions.append(emoji_extension)
    # add math extension
    math_extension = ArithmatexExtension()
    math_extension.config['preview'] = [False, ""]
    math_extension.config['generic'] = [True, ""]
    extensions.append(math_extension)

    print(kb_dir)
    for root, dirs, files in os.walk(kb_dir):
        # print(root, dirs, files)
        # dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.') and f.endswith('.md')]
        if root.endswith('.backup'):
            for file in files:
                print(file)
                with open(os.path.join(root, file), mode='r', encoding='utf-8') as md_file:
                    # Read the entire content of the file
                    file_content = md_file.read()
                    print(f"File <{os.path.join(root, file)}> read successfully")
                html_content = markdown.markdown(file_content, extensions=extensions)
                with open(os.path.join(root, file + '.html'), 'w', encoding='utf-8') as md_file:
                    md_file.write(html_content)
                    print(f"File <{os.path.join(root, file + '.html')}> write successfully")


if __name__ == '__main__':
    print(f'CWD: {os.getcwd()}')
    transfer_mds_to_htmls()
