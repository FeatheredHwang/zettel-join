---
note-type: cloze
title: "Cloze Note Example"
---

# Cloze Note Example

> [!TIP]
> 
> Try to write a short name for your heading instead of questions like "How to buildup your md file for cloze deletion", since the addon join the headings to be root field as header of Anki card.

This is an example of how to write markdown for "Cloze (traceable)" Note-type. "Cloze (traceable)" is part of "zettel-join" Anki-addon.

**Each heading** in the markdown file will be considered as a single note, up-to three levels (h1-h3). If h4-h6 exists, it will be included in its upper h3 heading.

After join/importation, a **comment** with Note Id will be inserted after the heading.

## Field Map

- Headings will be joined together, from h1 to h\[1-6\], as 'root' field. 
- Content under the heading (except blockquotes) will map to 'Text' field, where cloze-deletion happens.
- Blockquotes under the heading will map to 'Extra' field.

> [!Note]
>
> For best practice, map heading to book's section (h1 is chapter, h2 is section), limit heading's level no more than three.

## Cloze-deletion rules

The most concerned question is, how the addon recognize cloze deletions. The addon will find cloze-deletions in the text field by the following rules.

> These rules won't work in blockquote contents.
> 

> [!WARNING] 
>
> ZK-join *won't* accept nested cloze-deletion. For example, if you write MD like:
> ```
> 1. **strong** word inside a list item
> ```
> the `strong` word will be a cloze-deletion, while the list item not.

### Strong and emphasis(italic) words

**Strong** words surrounded by `**`, **emphasis** words surrounded by `*`, both will join cloze deletion. 

### List items

List items, no matter ordered or unordered, if there is no special element exists inside, will join cloze deletion. 

For example, there are four collection data types in the Python programming language:

1. List
2. Tuple
3. Set
4. Dictionary

### Table

By default, table **data** will join cloze deletion.

Allowing table and table inside blockquote. Failed with table inside list due to python-markdown's limit.

For example, there are four collection data types in the Python programming language:

| collection data types | ordered               | changeable   | duplicate |
| --------------------- | --------------------- | ------------ | --------- |
| List                  | ordered               |              | allow     |
| Tuple                 | ordered               | unchangeable | allow     |
| Set                   | unordered (unindexed) | unchangeable | no        |
| Dictionary            | ordered               | changeable   | no        |

### Math blocks

Anki natively [support MathJax](https://docs.ankiweb.net/math.html), while Typora also [render math using MathJax](https://support.typora.io/Math/#cross-reference). 

By default, math block will join cloze deletion, while inline math (such as $\bar x$) excluded. 

$$
E = mc^2
$$

And reference is also supported: $\ref{eq:sample}$

$$
\int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
\label{eq:sample}\tag{A}
$$

The best practice is put only one equation in each math-block. 

> [!WARNING]
>
> DO NOT use 'equation' environment to replace 'align', or Typora will raise:
>
> ```
> Error: Multiple \label
> ```

> [!Note]
>
> Math blocks won't be influenced by other cloze-deletion rules.

### No cloze-deletion found

If there is no cloze-deletion found under the heading, it won't create any note for it.



## Features

### Frontmatter

Frontmatter at the front of the file will be rendered separately from file content. For example:

```
---
note-type: cloze
---
```

For now, frontmatter is used to indicate which note-type should the MD file mirror to.

### Extra info

All the **blockquotes** will be rendered as 'Extra' field, which show up in the back side of note but not in the front.

Cloze-deletion won't happen in blockquotes.

### Fenced code block support

Allowing fenced code block.

Allowing the nesting of fences under blockquotes or lists.

```python
import os
```

### Image support

Allowing images with relative or absolute path.

Allowing both Markdown syntax `![alt](src)` and HTML syntax `<img src="src" alt="alt">`.

For example:

![forest](.assets/forest.jpg)

> Photos by [Luca Bravo](https://unsplash.com/@lucabravo), free to use under the [Unsplash License](https://unsplash.com/license)

Since folders inside the Anki media folder are not supported, the addon will insert its **dirname** (way to the root of Kästen) before the filename as **prefix**, then join/copy images directly to the media folder. In the above example, assuming the image file is under `/About this addon/MD examples/` directory, image's name would be standardized like `About_this_addon.MD_example.forest.jpg`.

### Emoji support

Emoji with syntax `:snake:` is supported, which would output :snake:

### :star:Mark note

If you add ​`:star:`​/⭐ at the beginning of this heading (or upper level heading), the note generated from this heading will be **marked**. For example, the h1 heading is indicated as marked, then all the h2 and h3 headings that under the h1 heading will get marked too.

### Line break

To create a line break or new line (`<br>`), end a line with **two or more** spaces, and then type return.   
In Typora if you type `shift + return` you will go to a new line rather than a new paragraph (after an empty line)

### To be continued...

Read more about [Typora Markdown Reference](https://support.typora.io/Markdown-Reference/)

---

Divided by this horizontal line, you can add additional info at the end of the file,  which will not be included to Anki notes.
