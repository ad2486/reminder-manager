# Lembretes Manager

🇧🇷 Português | 🇺🇸 [English](README.md)

```text
██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██████╗ ███████╗██████╗ ███████╗
██╔══██╗██╔════╝████╗ ████║██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝
██████╔╝█████╗  ██╔████╔██║██║██╔██╗ ██║██████╔╝█████╗  ██████╔╝███████╗
██╔══██╗██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██╔══██╗██╔══╝  ██╔══██╗╚════██║
██║  ██║███████╗██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗██║  ██║███████║
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
                                                                 by @ad2486
```

Gerenciador de lembretes com interface gráfica, notificações nativas e suporte a bandeja do sistema.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-linux%20|%20windows%20|%20macos-lightgrey)
![Tests](https://github.com/ad2486/reminder-manager/actions/workflows/tests.yml/badge.svg)

## Funcionalidades

- ⏰ Adicionar, editar e remover lembretes com intervalo personalizado
- 🔔 Notificações nativas do sistema (Linux, Windows e macOS)
- 🖥️ Interface gráfica com tema escuro (CustomTkinter)
- 🎯 Monitoramento em tempo real com contagem regressiva
- 📌 Minimizar para bandeja do sistema
- 💾 Persistência em JSON
- ⚙️ CLI completa para gerenciamento via terminal

## Requisitos

- Python 3.10+
- Linux: `notify-send` (libnotify) para notificações
- Linux (GNOME/Wayland): extensão [AppIndicator](https://extensions.gnome.org/) para bandeja

## Instalação

### Via pip (recomendado)

```bash
git clone https://github.com/ad2486/reminder-manager.git
cd reminder-manager
pip install .
```

Depois é só rodar:

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

## Uso

### Interface gráfica

```bash
lembretes
# ou
python gui.py
```

| Ação | Como fazer |
|---|---|
| Adicionar lembrete | Clique em "Adicionar", preencha nome, horas e minutos |
| Editar | Clique em "Editar" no card do lembrete |
| Remover | Clique em "Remover" no card do lembrete |
| Minimizar pra bandeja | Clique no botão "─" |
| Iniciar/Parar monitoramento | Botão no canto inferior direito |

### CLI

```bash
python main.py add "Tomar água" 30
python main.py list
python main.py remove <id>
python main.py start
python main.py gui
```

## Estrutura do projeto

```
reminder-manager/
├── core/
│   ├── __init__.py       # Exporta funções principais
│   ├── reminders.py      # CRUD de lembretes
│   ├── storage.py        # Persistência em JSON
│   ├── scheduler.py      # Agendador de disparos
│   └── notifier.py       # Notificações nativas
├── tests/
│   ├── test_storage.py
│   ├── test_reminders.py
│   ├── test_scheduler.py
│   └── test_notifier.py
├── gui.py                # Interface gráfica
├── main.py               # CLI + entrypoint
├── pyproject.toml        # Configuração do pacote
└── requirements.txt
```

## Sobre

Oi! Eu sou **Arthur Duarte**, estudante de ensino médio e apaixonado por programação.

Atualmente estou aprendendo HTML/CSS/JS para freelance fullstack, e já construí projetos backend com Python e Flask. Meu objetivo é cursar Ciência da Computação na faculdade e trabalhar como desenvolvedor.

Esse projeto foi feito para aprender sobre interfaces gráficas com CustomTkinter, notificações nativas, e integração com a bandeja do sistema.

- 🐙 GitHub: [@ad2486](https://github.com/ad2486)

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
