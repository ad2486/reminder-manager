# Reminder Manager

🇺🇸 English | 🇧🇷 [Português](README.pt-BR.md)

```
 _____  ______ __  __ _____ _   _ _____  ______ _____  
|  __ \|  ____|  \/  |_   _| \ | |  __ \|  ____|  __ \ 
| |__) | |__  | \  / | | | |  \| | |  | | |__  | |__) |
|  _  /|  __| | |\/| | | | | . ` | |  | |  __| |  _  / 
| | \ \| |____| |  | |_| |_| |\  | |__| | |____| | \ \ 
|_|  \_\______|_|  |_|_____|_| \_|_____/|______|_|  \_\
                                                   by @ad2486
```

A cross-platform reminder manager with a modern GUI, native notifications, and system tray support.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-linux%20|%20windows%20|%20macos-lightgrey)
![Tests](https://github.com/ad2486/reminder-manager/actions/workflows/tests.yml/badge.svg)

## Features

- ⏰ Add, edit, and remove reminders with custom intervals
- 🔔 Native desktop notifications (Linux, Windows, macOS)
- 🖥️ Modern dark-themed GUI (CustomTkinter)
- 🎯 Real-time monitoring with countdown display
- 📌 Minimize to system tray
- 💾 JSON-based persistence
- ⚙️ Full CLI for terminal management

## Requirements

- Python 3.10+
- Linux: `notify-send` (libnotify) for notifications
- Linux (GNOME/Wayland): [AppIndicator extension](https://extensions.gnome.org/) for system tray

## Installation

### Via pip (recommended)

```bash
git clone https://github.com/ad2486/reminder-manager.git
cd reminder-manager
pip install .
```

Then simply run:

```bash
lembretes
```

### Manual

```bash
git clone https://github.com/ad2486/reminder-manager.git
cd reminder-manager
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python gui.py
```

## Usage

### GUI

```bash
lembretes
# or
python gui.py
```

| Action | How to |
|---|---|
| Add reminder | Click "Adicionar", fill in name, hours and minutes |
| Edit | Click "Editar" on the reminder card |
| Remove | Click "Remover" on the reminder card |
| Minimize to tray | Click the "─" button |
| Start/Stop monitoring | Button in the bottom right corner |

### CLI

```bash
python main.py add "Drink water" 30
python main.py list
python main.py remove <id>
python main.py start
python main.py gui
```

## Project structure

```
reminder-manager/
├── core/
│   ├── __init__.py       # Exports main functions
│   ├── reminders.py      # CRUD operations
│   ├── storage.py        # JSON persistence
│   ├── scheduler.py      # Reminder scheduler
│   └── notifier.py       # Native notifications
├── tests/
│   ├── test_storage.py
│   ├── test_reminders.py
│   ├── test_scheduler.py
│   └── test_notifier.py
├── gui.py                # GUI application
├── main.py               # CLI + entrypoint
├── pyproject.toml        # Package config
└── requirements.txt
```

## About

Hi! I'm **Arthur Duarte**, a Brazilian high school student passionate about programming.

I'm currently learning HTML/CSS/JS for fullstack freelance work, and I've already built backend projects with Python and Flask. My goal is to study Computer Science in college and work as a developer.

This project was built to learn about GUI development with CustomTkinter, native notifications, and system tray integration.

- 🐙 GitHub: [@ad2486](https://github.com/ad2486)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
