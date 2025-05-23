<div align="center">
  
<img src="doc/logo.svg" width="80">

# PyNote

***A Python application for managing your Pronote account with a modern graphical interface, allowing you to view notes effortlessly.***

[![Commits](https://img.shields.io/github/commit-activity/t/MadeByRoucoule/PyNote?style=flat)](https://github.com/MadeByRoucoule/PyNote/commits/main/)
[![Stars](https://img.shields.io/github/stars/MadeByRoucoule/PyNote?style=social&label=Stars)](https://github.com/MadeByRoucoule/PyNote)

<img src="doc/screenshot_home_page.png" height="250px">
<img src="doc/screenshot_notes_page.png" height="250px">
<img src="doc/screenshot_login_page.png" height="250px">

</div>

## 🚀 Features

- 📚 **Pronote Integration**: Connect seamlessly to your Pronote account to fetch notes, timetables, and homework.
- 🗂 **Data Management**: View detailed information on grades and averages per period.
- 💾 **Data Export**: Save your Pronote data (notes, averages, etc.) to JSON and Excel files.
- 🔄 **Real-Time Updates**: Update displayed data automatically as you navigate through periods and subjects.

## Run the project

First, clone the repository :
```bash
git clone https://github.com/MadeByRoucoule/PyNote.git
cd PyNote
```
Then run the program with the following command (using [uv tool](https://github.com/astral-sh/uv), so install it before running the command - see [the documentation page on this](https://docs.astral.sh/uv/))
```bash
uv run "src/main.py"
```