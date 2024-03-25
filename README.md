# KBjoint
Join/Import your knowledge base (majorly md files) into Anki Notes

## Develop Guide

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
   
2. Writing union type hints</br>
   For now, Anki uses Python 3.9
   writing union types as `X | Y` allowed in Python 3.10 and later versions.

   ```python
   from typing import Union
   # Wrong
   def open_kb_dir() -> str | None:
     pass
   # Right
   def open_dir() -> Union[str, None]:
     pass
   ```