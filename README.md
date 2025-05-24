<div align="center">

<img src="doc/logo.svg" width="80">

# PyNote

***A Python application for managing your Pronote account with a modern graphical interface, allowing you to view notes effortlessly.***

[![Commits](https://img.shields.io/github/commit-activity/t/MadeByRoucoule/PyNote?style=flat)](https://github.com/MadeByRoucoule/PyNote/commits/main/)
[![Stars](https://img.shields.io/github/stars/MadeByRoucoule/PyNote?style=social&label=Stars)](https://github.com/MadeByRoucoule/PyNote)
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

![Built with Python3](https://img.shields.io/badge/built%20with-Python3-yellow.svg)
![platforms](https://img.shields.io/badge/Platforms-Linux%20|%20Windows%20|%20Mac%20-purple.svg)
[![Licence](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/MadeByRoucoule/PyNote/blob/master/LICENCE.txt)
___
<img src="doc/screenshot_home_page.png" height="250px">
<img src="doc/screenshot_notes_page.png" height="250px">

</div>

## 🚀 Features
### ✅ Currently, you can:
- 📊 **Pronote Integration**: Connect seamlessly to your Pronote account to fetch notes,
- 🗂 **Data Management**: View detailed information on grades and averages per period,
- 🔄 **Real-Time Updates**: Update displayed data automatically as you navigate through periods and subjects.
___
## 🔧 Shortly:
- ⏳️ **Pronote Workflow**: Added timetable and assignment display to the dashboard
- 💾 **Data Export**: Save your Pronote data (grades, averages, etc.) in JSON and Excel files.

# Developer Documentation
## Run the project:
First, clone the repository :
```bash
git clone https://github.com/MadeByRoucoule/PyNote.git
cd PyNote
```
Then run the program with the following command (using [uv tool](https://github.com/astral-sh/uv), so install it before running the command - see [the documentation page on this](https://docs.astral.sh/uv/))
```bash
uv run "src/main.py"
```