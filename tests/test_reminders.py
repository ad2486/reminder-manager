import pytest
from core.reminders import add_reminder, remove_reminder, listar, editar


def test_add_reminder(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    r = add_reminder("teste", 30)
    assert r["message"] == "teste"
    assert r["interval"] == 30
    assert "id" in r
    assert r["next_trigger"] > 0

    all_reminders = listar()
    assert len(all_reminders) == 1
    assert all_reminders[0]["id"] == r["id"]


def test_remove_reminder(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    r = add_reminder("teste", 30)
    assert remove_reminder(r["id"]) is True
    assert listar() == []


def test_remove_nonexistent(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    assert remove_reminder("fake-id") is False


def test_list_empty(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    assert listar() == []


def test_edit_message(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    r = add_reminder("original", 30)
    edited = editar(r["id"], message="editado")
    assert edited["message"] == "editado"
    assert edited["interval"] == 30


def test_edit_interval(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    r = add_reminder("teste", 30)
    edited = editar(r["id"], interval_minutes=60)
    assert edited["interval"] == 60
    assert edited["next_trigger"] > 0


def test_edit_nonexistent(monkeypatch, tmp_path):
    data_file = tmp_path / "reminders.json"
    monkeypatch.setattr("core.storage.DATA_FILE", str(data_file))

    assert editar("fake-id", message="x") is None
