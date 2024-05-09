# Zettel Join

## Description

---

Join/Import your ZettelKästen  (or just a dozen of MD files as it be) into Anki Notes.

[Link to add-on](https://ankiweb.net/shared/info/822767335)

**IMPORTANT**: *This Addon is still under development.* While likely compatible with earlier versions, add-on v0.1.0-beta and the uppers have only been extensively tested with Anki `⁨23.12.1`. 

### Features

1. Join MD notes to 'Cloze (treacable)' model
2. support math block, code block, table, image and emoji

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
│  │      Chapter01.md
│  │      Chapter02.md
│  │      
│  └─BookY
│         (...)
│
└─ProjectB
      (...)
```

1. Most importantly, include a '.root' folder in your Kästen's root, this will indicate this folder is a Knowledge Base.
2. Hidden files and folders starts with `.` will be ignored.
3. Folder name will be joined together as deck's name such as: `ProjectA::BookX`
4. Add frontmatter like `note-type: cloze` at the start of file content, which indicates what Note-type it uses. For more information, see  section.

> Actually you can create as many level of folder as you like. For note-taking best practice, I encourage you to control the depth of folder no more than 3.

#### NoteType

The "note-type" frontmatter indicates which NoteType(Model) should your MD note map to. The addon will create the NoteType automatically.  

```
| short | NoteType |
| ----- | -------- |
| cloze | ZK Cloze |
```

> Unfortunately, AnkiWeb doesn't support markdown table.

Look at the [examples](https://github.com/FeatheredHwang/zettel-join/tree/main/zettel_join/doc/ex) to learn about how to write a MD file.

#### One-click import

When the add-on is downloaded, a `ZK Join` option will be added to the `Tools` menu. Click it and choose your Knowledge Base Location, and that's all.

### Changelog

*This Addon is still under development. Version hasn't been setup yet*

#### v0.1.0-beta -- 2024-04-20

What's Changed

- Join MD notes to 'Cloze (treacable)' model
- support math block, code block, table, image and emoji

[Full Changelog](https://github.com/FeatheredHwang/zettel-join/commits/0.1.0-beta)

### Help And Support

**Please do not use reviews for bug reports or support requests.** I don't get notified of your reviews, and properly troubleshooting an issue through them is nearly impossible. Instead, please either use the [issue tracker](https://github.com/FeatheredHwang/zettel-join/issues) (preferred), [add-on support forums](https://forums.ankiweb.net/t/zettel-join-support-thread/43867?u=featheredhwang), or just message me at  feathered.hwang@hotmail.com. Constructive feedback and suggestions are always welcome!

### Credit And License

Copyright © 2024 [Feathered Hwang](https://github.com/FeatheredHwang) 

Licensed under the **GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007**. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. For more information on the license please see the [LICENSE file](https://github.com/FeatheredHwang/zettel-join/blob/main/LICENSE) accompanying this add-on. The source code is available on  [GitHub](https://github.com/FeatheredHwang/zettel-join). Pull requests and other contributions are welcome!

### Support My Work

If you like zettel-join, please give it a  :thumbsup: thumbs up and share it with your friends, so that more people can enjoy it!

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

