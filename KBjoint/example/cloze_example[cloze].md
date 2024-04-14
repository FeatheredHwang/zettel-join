# :star:Cloze Note Example

> [!TIP]
> 
> Try to write a short name instead of questions like "How to buildup your md file for cloze deletion"

This is an example of how to write markdown for KB-join purpose. 

Each heading in the markdown file will be considered as a single note, up-to three levels (h1-h3). If h4-h6 exists, it will be included in its upper h3 heading.

After join/importation, a comment with Note Id will be inserted after the heading.

If you add :star:/⭐ at the beginning of this heading (or upper level heading), the note generated from this heading will **get marked**. For example, the h1 heading is indicated as marked, then all the h2 and h3 headings that under the h1 heading will get marked too.

- H1 headings will map to 'Chapter' field, corresponding to **chapters** in the book.
- H2 headings will map to 'Section' field,  corresponding to **Sections** in the book.
- H3 headings will map to 'Subsection' field,  corresponding to **Subsections** in the book.**
- 1-3 headings will be joined together as 'root' field. 
- Content under the heading (except blockquotes) will map to 'Text' field, where cloze-deletion happens.
- Blockquotes under the heading will map to 'Extra' field.

## Cloze-deletion rules

The most concerned question is, how the addon recognize cloze deletions. The addon will find cloze-deletions in the text field by the following rules.

> These rules won't work in blockquote contents.

### Strong and emphasis(italic) words

**Strong** words surrounded by `**`, *emphasis* words surrounded by `*`, both will join cloze deletion. 

> After cloze-deletion, it would look like:
>
> ```
> **{{c1:: Strong }}** words, *{{c2:: emphasis }}* words
> ```

### List items

List items, no matter ordered or unordered, will join cloze deletion if no strong/emphasis exists inside. If there are more than one paragraph inside the item, only the first paragraph will join cloze deletion. For example, there are four collection data types in the Python programming language:

1. List

2. Tuple

3. Set

   > Set items are unchangeable

4. Dictionary

> After  cloze-deletion, it would look like:
>
> ```
> 1. {{c1:: List }}
> 
> 2. {{c2:: Tuple }}
> 
> 3. {{c3:: Set }}
> 
>    > Set items are unchangeable
> 
> 4. {{c4:: Dictionary }}
> ```

> The above example works ill for memorize, due to ["Avoid sets" rule](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge), you'd better to convert a set into a meaningful listing:
>
> - **List** is a collection which is ordered and changeable. Allows duplicate members.
> - **Tuple** is a collection which is ordered and **unchangeable**. Allows duplicate members.
> - ...
>
> or make a table for comparison convenience.

> [!WARNING] 
> 
> If Strong words exists as well as list items, list items will be *ignored* for cloze-deletion.

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
The best practice is put only one equation in each math-block. If you wanna put two or more equations into a single math-block,  you can use **'align'** environment and mark each equation with a label. The addon will do cloze-deletion one-by-one.
$$
\begin{align}
  x &= x + 1 					\label{eq:1}\tag{1}	\\
  \text{eggs} &= \text{bacon} 	\label{eq:2}\tag{2}
\end{align}
$$

> With label assigned, the math block would be like this after cloze-deletion:
>
> ```
> $$
> \begin{align}
> 	{{c1:: x &= x + 1 }}                  \label{eq1}\tag{1}  \\
> 	{{c2:: \text{eggs} &= \text{bacon} }} \label{eq2}\tag{2}
> \end{align}
> $$
> ```
>
> Without label assigned:
>
> ```
> $$
> {{c1::
> \begin{aligned}
> S & = \frac{\pi r^2}{2} \\
> & = \frac{1}{2} \pi r^2
> \end{aligned}
> }}
> $$
> ```
>
> 

> [!WARNING]
>
> DO NOT use 'equation'  environment to replace 'align', or it will raise:
> $$
> \begin{equation}
> x = x + 1					\label{eq1}\tag{1}	\\
> \text{eggs} = \text{bacon}	\label{eq2}\tag{2}
> \end{equation}
> $$

> [!Note]
>
> Math blocks won't be influenced by other cloze-deletion rules.



### To be continued...

#### Table

Tables will be supported in the future.

For example, there are four collection data types in the Python programming language:

| collection data types | ordered               | changeable   | duplicate |
| --------------------- | --------------------- | ------------ | --------- |
| List                  | ordered               |              | allow     |
| Tuple                 | ordered               | unchangeable | allow     |
| Set                   | unordered (unindexed) | unchangeable | no        |
| Dictionary            | ordered               |              | no        |

Set *items* are unchangeable, but you can remove and/or add items whenever you like.

[2]: As of Python version 3.7, dictionaries are *ordered*. In Python 3.6 and earlier, dictionaries are *unordered*.

#### User defined tags

User defined tags will be supported in the future.

**Bi-directional link** will be parsed as tags.

#### Mind Map

Due to ["Use mnemonic techniques" rule](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge)...

### No cloze-deletion found

If there is no cloze-deletion found under the heading, it won't create any note for this note.

## Hint info rule

All the blockquotes will be considered as hints, which show up in the back side of note but not in the front.

Cloze-deletion won't happen in blockquotes.

___

You can add additional info at the end of the file,  which will not be included to Anki.



[2]: 