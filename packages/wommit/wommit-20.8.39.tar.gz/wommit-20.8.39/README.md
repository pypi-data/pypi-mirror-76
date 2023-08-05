# Wommit

**W**rite c**ommit** **t**ool

---

[![PyCalVer 20.08.0032-dev][version_img]][version_ref]
[![PyPI Releases][pypi_img]][pypi_ref]

#### A package for intuitively formatting appealing commmit messages with emojis, using an assortment of different methods.

![CHECK ME OUT](https://i.imgur.com/VIXvQXY.png)

---
### Installation:
`pip install wommit`

---
### Usage:


**Autocomplete mode**
![EXAMPLE](https://i.imgur.com/EORqAkh.gif)

**Menu mode**
![EXAMPLE2](https://i.imgur.com/Wky0kOE.gif)

- **Tab** will call the autocompleters, although `complete while typing` is activated.
  - Starting *autocomplete mode* by hitting **Tab** will bring up the **types** added to the project.
- Adding `(` after the feature in *autocomplete mode* will autocomplete the scopes added to the project.  
- `#` in the body of either mode will autocomplete active issues and PRs.
- `(` in the body of either mode will autocomplete recent commits.
- Answering yes to the Breaking Change prompt in *menu mode* or writing `BREAKING CHANGE` in the *autocomplete mode* will
mark the commit as a breaking change.
  - *Autocomplete mode* will attempt to autocomplete `BREAKING CHANGE:` if it's on a clean line.
- Both *modes* will only terminate if their input is correctly formatted.

---
### Commands

`wommit ...`:

- `c`: Commit all staged files using an intuitive selection menu or a fast autocompletion prompt.

  *Options:*
  
  - `-m`: Use menu mode, overriding default./
  - `-e`: Use autocompletion mode, overriding default.
  - `-a`: Add all files to commit. (`git add .`)
  - `-m [MESSAGE]`: Write a manual commit message, and commits if it's in the accepted format, as well as converting known types to emojis. 
  - `-g`: Use global settings and data instead of local.
  - `--test`:  Test either of the modes without commiting.
  
- `check`: Manually check previously added commit. 

  *Options:*

  - `-id [HASH]`: Check a commit message with the specified ID.
  - `-ids [HASH1] [HASH2]`: Check all commit messages between two IDs (newest ID first).
  - `-m [MESSAGE]`:  Check if the given string passes the check.
  - `-l`:  Check all local commits that have not been pushed.
  
- `configure ...`: Opens a prompt for adding/removing types and scopes.

    - `e`: Edit current types and scopes.
    - `p`: Prints all types and scopes.
    - `s`: Edit settings.

    *Options:*

  - `-g`: Edit global settings.
  - `-t`: Manually test the functionality.
 
 - `changelog`: Prints out a changelog generated from commits since last release.
 
    *Options:*
    - `-r`: Prints a changelog designed for Github releases.
    - `-b`: Prints an easily readable changelog.
    - `-e`: EXPERIMENTAL: edit the latest Github release with the generated changelog.
    - `post`: Checks commits between two latest releases instead of latest to now.
  
 - `format`: Pastes the format a message needs to meet in order to pass the check.
 
 
 ---
 
 ## Info
 
 Use the [wommit-changelog-action](https://github.com/bkkp/wommit-changelog-action) in your wommit project to automatically release your project with appropriate changelogs.

[version_img]: https://img.shields.io/static/v1.svg?label=Wommit&message=20.08.0032-dev&color=blue
[version_ref]: https://pypi.org/project/wommit/
[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/wommit/

