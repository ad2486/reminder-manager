import platform
import subprocess
import shutil


def _notify_linux(title, message):
    if not shutil.which("notify-send"):
        print(f"[{title}] {message}")
        return
    subprocess.run(
        ["notify-send", title, message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _notify_windows(title, message):
    try:
        from win10toast import ToastNotifier

        ToastNotifier().show_toast(title, message, duration=5)
    except ImportError:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, title, 0)


def _notify_macos(title, message):
    subprocess.run(
        [
            "osascript",
            "-e",
            f'display notification "{message}" with title "{title}"',
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def notify(title, message):
    system = platform.system()
    if system == "Linux":
        _notify_linux(title, message)
    elif system == "Windows":
        _notify_windows(title, message)
    elif system == "Darwin":
        _notify_macos(title, message)
    else:
        print(f"[{title}] {message}")
