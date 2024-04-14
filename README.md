# Zettel Join

## Description

---

This addon is keen to Join/Import your Zettlekasten (or just a dozen of MD files as it be) into Anki Notes.

[Link to add-on](https://ankiweb.net/shared/info/822767335)

**IMPORTANT**: *This Addon is still under development.* While likely compatible with earlier versions, add-on versions v0.1 and the uppers have only been extensively tested with Anki `⁨23.12.1`. 

### Features

1. support markdown files (Typora-flavor preferred)
2. support Math Blocks indicated by '$$', which will be added to cloze deletion.
3. support Images which is stored locally and will be added to media folder.
4. allow emojifying content such as: `:snake:` , output 🐍

### Zettelkasten, what it is?

Zettelkasten is a German word that loosely translates to "note box" or "slip box". Zettels means "Index cards" and Kasten means A box or crate. It is also the name of  a **note-taking technique** that involves writing one idea per note, and storing it in one place, such as a box. The method was popularized by German sociologist **Niklas Luhmann**, who used it to collect and organize all his research notes in boxes. Read the [official introduction](https://zettelkasten.de/introduction/) to learn more about it.

This addon encourage you to recognize your notes system as a Zettlekasten, aimed to your [12 Favorite Problems](https://umbrex.com/resources/tools-for-thinking/what-is-twelve-favorite-problems/#:~:text=The%20concept%20of%20%E2%80%9CTwelve%20Favorite,significant%20progress%20in%20their%20field.), not a so-called knowledge base that stored everything. 

Don't bother though. For now, you can just think of it as a folder containing a dozen of MD files. 

### How to use

#### Prepare your Zettelkasten file system

The file system of your ZK is supposed to built as the follow structure:

```
Slipbox-root-folder
│  
├─.root
├─ProjectA
│  ├─BookX
│  │      Chapter01[cloze].md
│  │      Chapter02[cloze].md
│  │      
│  └─BookY
│         (...)
│
└─ProjectB
      (...)
```

1. Most importantly, include a '.root' folder in your KB's root, this will indicate this folder is a Knowledge Base.
2. Hidden files and folders starts with `.` will be ignored.
3. Folder name will be joined together as deck's name such as: `ProjectA::BookX`
4. Add suffix like `[cloze]` to the end of filename, which indicates which joint it uses. For more information, see [FileSuffix](###FileSuffix and NoteType) 

#### FileSuffix and NoteType

The "FileSuffix" indicates which NoteType(Model) should your MD note map to. The addon will create NoteTypes after the profile loaded. And it will recognize if the MD file has valid "FileSuffix" then import it.

```
| [FileSuffix] | NoteType          |
| ------------ | ----------------- |
| [cloze]      | Cloze (traceable) |
```

> Unfortunately, AnkiWeb doesn't support markdown table.

Look at the examples to learn about how to write a MD file.

#### One-click import

When the add-on is downloaded, a `KBjoin` option will be added to the `Tools` menu. Click it and choose your Knowledge Base Location, and that's all.

### Changelog

*This Addon is still under development. Version hasn't been setup yet*

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
- Python 3.9
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

