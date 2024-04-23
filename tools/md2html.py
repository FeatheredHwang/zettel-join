"""
Transfer markdown files to html for parse convenience,
"""
import os
import pathlib
import shutil
from dotenv import load_dotenv

import frontmatter
import markdown
from markdown import Extension
from markdown.extensions.tables import TableExtension
# pymdownx Extensions Documentation https://facelessuser.github.io/pymdown-extensions/
from pymdownx.emoji import EmojiExtension, to_alt
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.superfences import SuperFencesCodeExtension

# load variables from .env file
load_dotenv('../zettel_join/test/.env')


def transfer_md_to_html():
    """
    Transfer markdown files to html for parse convenience
    """
    # using os module to get environment variables
    test_kasten_path = os.getenv('TEST_KASTEN_PATH')
    md_ex_path = os.getenv('MD_EX_PATH')

    # copy example directory
    ex_dst_path = pathlib.Path(os.path.join(test_kasten_path, 'About this addon/MD examples'))
    ex_dst_path.mkdir(parents=True, exist_ok=True)  # create dir if not exist
    shutil.copytree(md_ex_path, ex_dst_path, dirs_exist_ok=True)  # copy MD examples, overwrite if file exists

    # register examples
    extensions: list[Extension] = []
    # add emoji extension
    emoji_ext = EmojiExtension()
    emoji_ext.setConfig('emoji_generator', to_alt)
    extensions.append(emoji_ext)
    # add math extension
    math_ext = ArithmatexExtension()
    math_ext.setConfig('preview', False)
    math_ext.setConfig('generic', True)
    extensions.append(math_ext)
    # add fenced_code extension
    fenced_code_ext = SuperFencesCodeExtension()
    extensions.append(fenced_code_ext)
    # add table extension
    table_ext = TableExtension()
    table_ext.setConfig('use_align_attribute', True)
    extensions.append(table_ext)

    # render the files
    print(ex_dst_path)
    for root, dirs, files in os.walk(ex_dst_path):
        files = [f for f in files if not f.startswith('.') and f.endswith('.md')]
        for file in files:
            print(file)
            with open(os.path.join(root, file), mode='r', encoding='utf-8') as md_file:
                # Read the entire content of the file
                # file_content = md_file.read()
                post = frontmatter.load(md_file)
                print(post.metadata)
                print(f"File <{os.path.join(root, file)}> read successfully")
            html_content = markdown.markdown(post.content, extensions=extensions)
            with open(os.path.join(root, file + '.html'), 'w', encoding='utf-8') as md_file:
                md_file.write(html_content)
                print(f"File <{os.path.join(root, file + '.html')}> write successfully")


if __name__ == '__main__':
    print(f'CWD: {os.getcwd()}')
    transfer_md_to_html()
