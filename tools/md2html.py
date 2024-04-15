"""
Transfer markdown files to html for parse convenience,
"""
import os
import pathlib
import shutil
from dotenv import load_dotenv

import markdown
from markdown import Extension
from markdown.extensions.tables import TableExtension
# PyMdown Extensions Documentation https://facelessuser.github.io/pymdown-extensions/
from pymdownx.emoji import EmojiExtension, to_alt
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.superfences import SuperFencesCodeExtension

# load variables from .env file
load_dotenv('../zettel_join/.env')


def transfer_mds_to_htmls():
    """
    Transfer markdown files to html for parse convenience
    """
    # using os module to get environment variables
    test_kasten_path = os.getenv('TEST_KASTEN_PATH')
    md_ex_path = os.getenv('MD_EX_PATH')

    ex_dst_path = pathlib.Path(os.path.join(test_kasten_path, 'About this addon/MD examples/.backup'))
    # if path not exist, create it
    ex_dst_path.mkdir(parents=True, exist_ok=True)
    # copy MD examples from the project dir, overwrite if file exists
    shutil.copytree(md_ex_path, ex_dst_path, dirs_exist_ok=True)

    extensions: list[Extension] = []

    # add emoji extension
    emoji_ext = EmojiExtension()
    emoji_ext.config['emoji_generator'] = [to_alt, '']
    extensions.append(emoji_ext)
    # add math extension
    math_ext = ArithmatexExtension()
    math_ext.config['preview'] = [False, ""]
    math_ext.config['generic'] = [True, ""]
    # math_ext.setConfig('generic', True)
    extensions.append(math_ext)
    # add fenced_code extension
    fenced_code_ext = SuperFencesCodeExtension()
    extensions.append(fenced_code_ext)
    # add table extension
    table_ext = TableExtension()
    table_ext.setConfig('use_align_attribute', True)
    extensions.append(table_ext)

    print(test_kasten_path)
    for root, dirs, files in os.walk(test_kasten_path):
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
