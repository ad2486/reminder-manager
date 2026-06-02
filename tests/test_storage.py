import json
import os

import pytest
from core.storage import load_reminders, save_reminders, DATA_FILE


def test_save_and_load(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    reminders = [{"id": "1", "message": "teste", "interval": 30, "next_trigger": 100.0}]
    save_reminders(reminders)
    assert data_file.exists()

    loaded = load_reminders()
    assert loaded == reminders


def test_load_missing_file(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    assert load_reminders() == []


def test_load_invalid_json(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))
    data_file.write_text("{ invalido", encoding="utf-8")

    assert load_reminders() == []
