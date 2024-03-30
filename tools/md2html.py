import os
import markdown

from markdown import Extension
from pymdownx.emoji import EmojiExtension, to_alt
from pymdownx.arithmatex import ArithmatexExtension


def transfer_mds_to_htmls():
    kb_dir = r'D:\Projects\.test\KB-test'

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
        print(root)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.') and f.endswith('.md')]
        for file in files:
            print(file)
            with open(os.path.join(root, file), 'r', encoding='utf-8') as md_file:
                # Read the entire content of the file
                file_content = md_file.read()
                print(f"File <{md_file}> read successfully")
            html_content = markdown.markdown(file_content)
            with open(os.path.join(root, file + '.html'), 'w', encoding='utf-8') as md_file:
                md_file.write(html_content)


if __name__ == '__main__':
    print('Hello World')
    transfer_mds_to_htmls()
