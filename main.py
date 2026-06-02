import argparse
import sys

from core import add_reminder, remove_reminder, listar
from core.scheduler import start


def cmd_add(args):
    r = add_reminder(args.message, args.interval)
    print(f"Lembrete adicionado: {r['id']}")


def cmd_list(args):
    reminders = listar()
    if not reminders:
        print("Nenhum lembrete.")
        return
    for r in reminders:
        print(f"{r['id']}  |  {r['message']}  |  a cada {r['interval']}min")


def cmd_remove(args):
    if remove_reminder(args.id):
        print("Lembrete removido.")
    else:
        print("ID não encontrado.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="reminder-manager")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Adicionar lembrete")
    p_add.add_argument("message", help="Mensagem do lembrete")
    p_add.add_argument("interval", type=int, help="Intervalo em minutos")

    p_remove = sub.add_parser("remove", help="Remover lembrete")
    p_remove.add_argument("id", help="ID do lembrete")

    sub.add_parser("list", help="Listar lembretes")
    sub.add_parser("start", help="Iniciar monitoramento (terminal)")
    sub.add_parser("gui", help="Abrir interface gráfica")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "start":
        start()
    elif args.command == "gui":
        from gui import run
        run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
