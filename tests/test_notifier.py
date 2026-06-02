from core.notifier import notify


def test_notify_does_not_crash():
    notify("Teste", "Mensagem de teste")
