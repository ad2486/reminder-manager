import json
import time

from core.scheduler import _check_and_fire


def test_check_and_fire_dispatches_due_reminder(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    data_file.write_text(
        json.dumps([
            {
                "id": "x1",
                "message": "Alerta",
                "interval": 30,
                "next_trigger": time.time() - 5,
            }
        ]),
        encoding="utf-8",
    )

    notified = []

    def fake_notify(title, msg):
        notified.append((title, msg))

    monkeypatch.setattr("core.scheduler.notify", fake_notify)

    _check_and_fire()

    assert len(notified) == 1
    assert notified[0] == ("Lembrete", "Alerta")

    dados = json.loads(data_file.read_text(encoding="utf-8"))
    assert dados[0]["next_trigger"] > time.time()


def test_check_and_fire_skips_future(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    data_file.write_text(
        json.dumps([
            {
                "id": "x2",
                "message": "Futuro",
                "interval": 30,
                "next_trigger": time.time() + 9999,
            }
        ]),
        encoding="utf-8",
    )

    notified = []

    def fake_notify(title, msg):
        notified.append((title, msg))

    monkeypatch.setattr("core.scheduler.notify", fake_notify)

    _check_and_fire()

    assert len(notified) == 0
