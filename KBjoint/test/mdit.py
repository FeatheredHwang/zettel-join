import os
import markdown2

kb_dir = r'D:\Projects\.test\KB-test'


for root, dirs, files in os.walk(kb_dir):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    files = [f for f in files if not f.startswith('.') and f.endswith('.md')]
    for file in files:
        with open(os.path.join(root, file), 'r', encoding='utf-8') as md_file:
            # Read the entire content of the file
            file_content = md_file.read()
            print(f"File <{md_file}> read successfully")
        html_content = markdown2.markdown(file_content)
        with open(os.path.join(root, file + '.html'), 'w', encoding='utf-8') as md_file:
            md_file.write(html_content)
