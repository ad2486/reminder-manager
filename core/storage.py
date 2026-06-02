import json
import os
import shutil

DATA_DIR = os.path.expanduser("~/.lembretes")
DATA_FILE = os.path.join(DATA_DIR, "reminders.json")


def _migrate_old():
    old = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reminders.json")
    if os.path.exists(old) and not os.path.exists(DATA_FILE):
        os.makedirs(DATA_DIR, exist_ok=True)
        shutil.copy2(old, DATA_FILE)


def load_reminders():
    _migrate_old()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_reminders(reminders):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)
