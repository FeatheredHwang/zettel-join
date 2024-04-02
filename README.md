# KBjoint

Join/Import your knowledge base (majorly md files) into Anki Notes

Features:

1. support markdown files (Typora-flavour preferred)
2. support Math Blocks indicated by '$$', which will be added to cloze deletion.
3. support Images which is stored locally and will be added to media folder.
4. allow emojifying content such as: `it's raining :cat:s and :dog:s!`

## Develop Guide

### Develop Environment

- Windows 11
- Python 3.11
- Anki 23.12.1
- IDE: Pycharm

### File Location

  Q: Where can I find the Anki files?
  A: in your appdata folder. Try typing `%APPDATA%\Anki2` in the location field.

### Python and Pip

Upgrade pip

```batch
python.exe -m pip install --upgrade pip
```

Use domestic source to improve download speed (if you live in China)

```batch
pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

### Git

#### Commit Name Rules

Here is a list of keywords that classify commit types, 
inspired by [Files](https://github.com/files-community/Files) project.

1. Features
2. Fix
3. Code Quality
4. Doc
5. Github
6. IDEA

### Mistakes I've made

#### mw is None before profile-loaded

Error Example
```python
from aqt import mw

mm = mw.col.models
```
this will return:
```
AttributeError: 'NoneType' object has no attribute 'models'
```

#### To connect the function to QAction

```python
from KBjoint import *

action = QAction('KB Join', mw)
# Wrong
action.triggered.connect(kb_join())
# Right
action.triggered.connect(kb_join)
```
   
#### Union type hints</br>

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

#### `<script>` tag get deleted in HTML editor of fields

`<style>` and `<script>` tag get deleted 
as soon as the focus leave HTML editor of fields:
<br>As anki want to provide better card preloading 
in the future (preload next card while showing current card), 
and for that, the field HTML may not contain any styles/scripts.
<br> In this case, when I use `mdx_math` (python-markdown-math)
or `pymdownx.arithmatex` (pymdown-extensions) 
to parse math, their returned **MathJax-style math**
`<script type="math/tex; mode=display">...</script>`
will get deleted.

#### How to use `python-markdown` extensions

<br>The Python-Markdown documentation 
explains how to use extensions:
> The list of extensions may contain instances of extensions and/or strings of extension names.
>
> `extensions=[MyExtension(), "path.to.my.ext"]`
>
> The preferred method is to pass in an instance of an extension. 
> Strings should only be used when it is **impossible**
> to import the Extension Class directly (from the command line or in a template).

#### How to write math in markdown

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
