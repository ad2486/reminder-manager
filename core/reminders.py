import uuid
from datetime import datetime, timezone

from .storage import load_reminders, save_reminders


def add_reminder(message, interval_minutes):
    reminders = load_reminders()
    interval_seconds = interval_minutes * 60
    reminder = {
        "id": str(uuid.uuid4()),
        "message": message,
        "interval": interval_minutes,
        "next_trigger": (datetime.now(timezone.utc).timestamp() + interval_seconds),
    }
    reminders.append(reminder)
    save_reminders(reminders)
    return reminder


def remove_reminder(reminder_id):
    reminders = load_reminders()
    filtered = [r for r in reminders if r["id"] != reminder_id]
    if len(filtered) == len(reminders):
        return False
    save_reminders(filtered)
    return True


def listar():
    return load_reminders()


def editar(reminder_id, message=None, interval_minutes=None):
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            if message is not None:
                r["message"] = message
            if interval_minutes is not None:
                r["interval"] = interval_minutes
                r["next_trigger"] = datetime.now(timezone.utc).timestamp() + interval_minutes * 60
            save_reminders(reminders)
            return r
    return None
