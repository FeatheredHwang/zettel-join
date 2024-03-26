# KBjoint
Join/Import your knowledge base (majorly md files) into Anki Notes

## Develop Guide

Upgrade pip

```batch
python.exe -m pip install --upgrade pip
```

Use domestic source to improve download speed.

```batch
pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```


### Develop Environment

- Windows 11
- Python 3.11
- Anki 23.12.1
- IDE: Pycharm

### Mistakes I've made

1. To connect the function to QAction

   ```python
   from KBjoint import *
   
   action = QAction('KB Join', mw)
   # Wrong
   action.triggered.connect(kb_join())
   # Right
   action.triggered.connect(kb_join)
   ```
   
2. Union type hints</br>
   For now, Anki uses Python 3.9
   writing union types as `X | Y` allowed 
   in Python 3.10 and later versions.

   ```python
   from typing import Union
   # Wrong
   def open_kb_dir() -> str | None:
     pass
   # Right
   def open_dir() -> Union[str, None]:
     pass
   ```
   
3. `<style>` and `<script>` tag get deleted 
   as soon as the focus leave the html editor:
   <br>As anki want to provide better card preloading 
   in the future (preload next card while showing current card), 
   and for that, the field HTML may not contain any styles/scripts.
   <br> In this case, when I use `mdx_math` (python-markdown-math)
   or `pymdownx.arithmatex` (pymdown-extensions) 
   to parse math, their returned **MathJax-style math**
   `<script type="math/tex; mode=display">...</script>`
   will get deleted.

4. Using `python-markdown` extensions:
   <br>The Python-Markdown documentation 
   explains how to use extensions:
   > The list of extensions may contain instances of extensions and/or strings of extension names.
   > 
   > `extensions=[MyExtension(), "path.to.my.ext"]`
   > 
   > The preferred method is to pass in an instance of an extension. 
   > Strings should only be used when it is **impossible**
   > to import the Extension Class directly (from the command line or in a template).
   
   