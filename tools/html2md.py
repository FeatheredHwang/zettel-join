"""
Transfer html files to markdown for test convenience,
"""
import os
from dotenv import load_dotenv

import bs4
import markdownify

# load variables from .env file
load_dotenv('../zettel_join/test/.env')


def transfer_html_to_md():
    # using os module to get environment variables
    test_kasten_path = os.getenv('TEST_KASTEN_PATH')
    ex_path = os.path.join(test_kasten_path, 'About this addon/MD examples')

    # render the files
    for root, dirs, files in os.walk(ex_path):
        files = [f for f in files if not f.startswith('.') and f.endswith('.html')]
        for file in files:
            print(file)
            with open(os.path.join(root, file), mode='r', encoding='utf-8') as html_file:
                # Read the entire content of the file
                html_content = html_file.read()
                print(f"File <{os.path.join(root, file)}> read successfully")
            md_content = markdownify.markdownify(html_content, heading_style="ATX")
            with open(os.path.join(root, file + '.md'), 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)
                print(f"File <{os.path.join(root, file + '.html')}> write successfully")


if __name__ == '__main__':
    print(f'CWD: {os.getcwd()}')
    transfer_html_to_md()
