# KBjoint

## Description

---

Join/Import your knowledge base (for now only md files supported) into Anki Notes.

[Link to add-on](https://ankiweb.net/shared/info/822767335)

**IMPORTANT**: *Addon is still under development.* While likely compatible with earlier versions, add-on versions v0.1 and up have only been extensively tested with Anki `⁨23.12.1`. 

### Features

1. support markdown files (Typora-flavor preferred)
2. support Math Blocks indicated by '$$', which will be added to cloze deletion.
3. support Images which is stored locally and will be added to media folder.
4. allow emojifying content such as: `:snake:` , output 🐍

### How to use

#### Prepare knowledge-base file system

The file system of your KB is supposed to built as the follow structure:

```
KB_root_folder
|___.root
	|___(...)
|___Area01
	|___Book01
		|___ChapterName01[cloze].md
		|___ChapterName02[cloze].md
|___Area02
	|___(...)
```

1. Most importantly, include a '.root' folder in your KB's root, this will indicate this folder is a Knowledge Base.
2. Hidden files and folders starts with `.` will get skipped.
3. Folder name will be joined together as deck's name such as: `Area01::Book01`
4. Add suffix like `[cloze]` to the end of filename, which indicates which joint it uses. For more information, see [Joints](###Joints) 

#### Joints

A Joint will map your note to a specific NoteType(Model). For now, KBjoint support joints as below:

| Joint      | [FileSuffix] | NoteType          |
| ---------- | ------------ | ----------------- |
| ClozeJoint | [cloze]      | Cloze (traceable) |

#### Prepare MD file for **cloze** joint

The MD File Structure is supposed like this:

```markdown
# ChapterName (H1 heading map to 'Chapter' field)

Each heading will be considered as a single note, up-to three levels. Headings will be joined together as 'root' field. In this heading's content there's no cloze-deletion, so it can't become a Note.

## :star:SectionName (H2 heading map to 'Section' field)

**Strong** tags will be transfered to cloze deletion. If you add :star:/⭐ at the beginning of this heading (or upper level heading), the note will **get marked**.

### SubSectionName (H3 heading map to 'SubSection' field)

Sub-heading of a marked heading will also get marked.

- list item will be transfered to cloze deletion
- no matter ordered list or unordered list

If Strong words exists as well as list items, list items will be ignored for cloze-deletion.

### Another SubSectioin

At last, math block will be added to cloze deletion, but inline math not (such as $\bar x$). 

$$
E = mc^2
$$

___

Additional Info (which will not include to note)

```

1. Each heading will be considered as a single note, up-to three levels. Headings will be joined together as root field.
2. Strong words will be considered as cloze-deletion. If not, then list items.
3. If you add ​`:star:`​/`⭐ `at the beginning of this heading (or upper level heading), the note will **get marked**.

When the add-on is downloaded, a `KBjoin` option will be added to the `Tools` menu. Click it and choose your Knowledge Base Location, and that's all.

### Changelog

*TODO Addon is still under development. Version hasn't been setup yet*

#### Version 0.1 -- 2024-04-04

Added

- KB examination and walk through
- Cloze Joint
- Images, Math Blocks and Emojis support

### Help And Support

You can message me at [feathered.hwang@hotmail.com](feathered.hwang@hotmail.com). Constructive feedback and suggestions are always welcome!

If you like KBjoint, please give it a  :thumbsup: thumbs up and share it with your friends, so that more people can enjoy it!

### Credit And License

Licensed under the **GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007**. This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**. For more information on the license please see the [LICENSE file](https://github.com/FeatheredHwang/KBjoint/blob/main/LICENSE) accompanying this add-on. The source code is available on  [GitHub](https://github.com/FeatheredHwang/KBjoint). Pull requests and other contributions are welcome!

---



### Develop Guide

#### Develop Environment

- Windows 11
- Python 3.11
- Anki 23.12.1
- IDE: PyCharm

#### File Location

  Q: Where can I find the Anki files?
  A: in your `appdata` folder. Try typing `%APPDATA%\Anki2` in the location field.

#### Python and Pip

Upgrade pip

```batch
python.exe -m pip install --upgrade pip
```

Use domestic source to improve download speed (if you live in China)

```batch
pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

#### Git

##### Commit Name Rules

Here is a list of keywords that classify commit types,  inspired by [Files](https://github.com/files-community/Files) project.

1. Features
2. Fix
3. Code Quality
4. Doc
5. Github
6. IDEA

#### Mistakes I've made

##### mw is None before profile-loaded

Error Example
```python
from aqt import mw

mm = mw.col.models
```
this will return:
```
AttributeError: 'NoneType' object has no attribute 'models'
```

##### To connect the function to QAction

```python
from KBjoint import *

action = QAction('KB Join', mw)
# Wrong
action.triggered.connect(kb_join())
# Right
action.triggered.connect(kb_join)
```

##### Union type hints</br>

For now, Anki uses Python 3.9 writing union types as `X | Y` allowed in Python 3.10 and later versions.

```python
from typing import Union
# Wrong
def open_kb_dir() -> str | None:
  pass
# Right
def open_dir() -> Union[str, None]:
  pass
```

##### `<script>` tag get deleted in HTML editor of fields

`<style>` and `<script>` tag get deleted as soon as the focus leave HTML editor of fields:
<br>As Anki want to provide better card preloading in the future (preload next card while showing current card), and for that, the field HTML may not contain any styles/scripts.
<br>In this case, when I use `mdx_math` (python-markdown-math) or `pymdownx.arithmatex` (pymdown-extensions) to parse math, their returned **MathJax-style math** `<script type="math/tex; mode=display">...</script>` will get deleted.

##### How to use `python-markdown` extensions

The Python-Markdown documentation explains how to use extensions:

> The list of extensions may contain instances of extensions and/or strings of extension names.
>
> `extensions=[MyExtension(), "path.to.my.ext"]`
>
> The preferred method is to pass in an instance of an extension. 
> Strings should only be used when it is **impossible**
> to import the Extension Class directly (from the command line or in a template).

##### How to write math in markdown

This Anki addon uses `python-markdown` to render the md file,
with `pymdownx.arithmatex` to render math. The way how we 
write markdown matters.

Error Example 1:

```markdown
text = r"""
Bad Example here:
$$
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
$$
Because we didn't leave blank line above and after '$$'.
"""
```
this will return:
```html
<p>Bad Example here:
$$
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
$$
Because we didn't leave blank line above and after '$$'.</p>
```

Error Example 2:

```python
import markdown
from pymdownx.arithmatex import ArithmatexExtension

def test_pymd_extension():
    text = r"""
    This is inline $\left\{\frac{1}{n^2}\right\}$
    
    $$
    \int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
    $$
    """
    math_extension = ArithmatexExtension()
    html = markdown.markdown(text, extensions=[ArithmatexExtension()])
```
this will return (mention the white space before '$$')
```markdown
<pre><code>$$
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
$$
</code></pre>
```

Good Example:
```markdown
text = r"""
This is inline $\left\{\frac{1}{n^2}\right\}$

but this is displayed 

$$
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
$$

centred on its own line.
"""
```
this will return:
```html
<p>This is inline <span class="arithmatex"><span class="MathJax_Preview">\left\{\frac{1}{n^2}\right\}</span><script type="math/tex">\left\{\frac{1}{n^2}\right\}</script></span>
but this is displayed </p>
<div class="arithmatex">
<div class="MathJax_Preview">
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
</div>
<script type="math/tex; mode=display">
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
</script>
</div>
<p>centred on its own line.</p>
```
