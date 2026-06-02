import time
import signal
import sys

from .storage import load_reminders, save_reminders
from .notifier import notify


def _check_and_fire():
    reminders = load_reminders()
    now = time.time()
    modified = False
    for r in reminders:
        if r["next_trigger"] <= now:
            notify("Lembrete", r["message"])
            r["next_trigger"] = now + r["interval"] * 60
            modified = True
    if modified:
        save_reminders(reminders)


def start():
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    print("Agendador iniciado. Pressione Ctrl+C para parar.")
    while True:
        _check_and_fire()
        time.sleep(1)
