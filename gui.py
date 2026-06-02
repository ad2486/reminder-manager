import threading
import time
from datetime import datetime, timezone

import customtkinter as ctk
from PIL import Image, ImageDraw

from core import add_reminder, remove_reminder, listar, editar
from core.storage import load_reminders, save_reminders
from core.notifier import notify

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def _make_icon_image(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2
    r = size // 2 - 3
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(41, 128, 185, 255))
    draw.polygon(
        [(cx, cy - r // 2 - 2), (cx - r // 2 + 2, cy + 2), (cx + r // 2 - 2, cy + 2)],
        fill=(255, 255, 255, 255),
    )
    draw.rectangle(
        [cx - 3, cy + r // 2 - 1, cx + 3, cy + r // 2 + 5],
        fill=(255, 255, 255, 255),
    )
    return img



class AddDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None

        self.title("Novo Lembrete")
        self.geometry("400x250")
        self.resizable(False, False)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome do lembrete")
        self.entry_nome.pack(padx=20, pady=(20, 10), fill="x")

        frame_tempo = ctk.CTkFrame(self, fg_color="transparent")
        frame_tempo.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(frame_tempo, text="Horas", width=40).pack(side="left")
        self.entry_horas = ctk.CTkEntry(frame_tempo, width=60)
        self.entry_horas.insert(0, "0")
        self.entry_horas.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(frame_tempo, text="Minutos", width=50).pack(side="left")
        self.entry_minutos = ctk.CTkEntry(frame_tempo, width=60)
        self.entry_minutos.insert(0, "30")
        self.entry_minutos.pack(side="left", padx=(4, 0))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))

        ctk.CTkButton(btn_frame, text="Salvar", command=self._save).pack(
            side="left", padx=5
        )
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy).pack(
            side="left", padx=5
        )

        self.wait_visibility()
        self.grab_set()

    def _save(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            return
        try:
            horas = int(self.entry_horas.get().strip() or "0")
            minutos = int(self.entry_minutos.get().strip() or "0")
        except ValueError:
            return
        total = horas * 60 + minutos
        if total < 1:
            return
        self.result = add_reminder(nome, total)
        self.destroy()


class EditDialog(ctk.CTkToplevel):
    def __init__(self, parent, reminder):
        super().__init__(parent)
        self.reminder = reminder
        self.result = None

        self.title("Editar Lembrete")
        self.geometry("400x250")
        self.resizable(False, False)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome do lembrete")
        self.entry_nome.insert(0, reminder["message"])
        self.entry_nome.pack(padx=20, pady=(20, 10), fill="x")

        frame_tempo = ctk.CTkFrame(self, fg_color="transparent")
        frame_tempo.pack(padx=20, pady=(0, 10), fill="x")

        interval = reminder["interval"]
        horas = interval // 60
        minutos = interval % 60

        ctk.CTkLabel(frame_tempo, text="Horas", width=40).pack(side="left")
        self.entry_horas = ctk.CTkEntry(frame_tempo, width=60)
        self.entry_horas.insert(0, str(horas))
        self.entry_horas.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(frame_tempo, text="Minutos", width=50).pack(side="left")
        self.entry_minutos = ctk.CTkEntry(frame_tempo, width=60)
        self.entry_minutos.insert(0, str(minutos))
        self.entry_minutos.pack(side="left", padx=(4, 0))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))

        ctk.CTkButton(btn_frame, text="Salvar", command=self._save).pack(
            side="left", padx=5
        )
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy).pack(
            side="left", padx=5
        )

        self.wait_visibility()
        self.grab_set()

    def _save(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            return
        try:
            horas = int(self.entry_horas.get().strip() or "0")
            minutos = int(self.entry_minutos.get().strip() or "0")
        except ValueError:
            return
        total = horas * 60 + minutos
        if total < 1:
            return
        self.result = editar(
            self.reminder["id"], message=nome, interval_minutes=total
        )
        self.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lembretes")
        self.geometry("680x540")
        self.minsize(520, 420)

        self._monitoring = False
        self._stop_event = threading.Event()
        self._thread = None
        self._tray_icon = None

        self._build_list_frame()
        self._build_bottom_frame()
        self._refresh_list()

        self.protocol("WM_DELETE_WINDOW", self._quit_app)
        self.after(100, self._setup_tray)
        self.after(300, self._toggle_monitoring)

    def _setup_tray(self):
        try:
            import pystray
            from pystray import MenuItem as Item

            icon_image = _make_icon_image()
            menu = [
                Item("Abrir", lambda: self.after(0, self._show_window), default=True),
                Item("Sair", lambda: self.after(0, self._quit_app)),
            ]
            self._tray_icon = pystray.Icon("lembretes", icon_image, "Lembretes", menu)
            t = threading.Thread(target=self._tray_icon.run, daemon=True)
            t.start()
        except Exception:
            pass

    def _show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def _hide_window(self):
        self.withdraw()

    def _quit_app(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
        if self._tray_icon:
            self._tray_icon.stop()
            self._tray_icon = None
        self.quit()
        self.destroy()

    def _build_list_frame(self):
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#1a3a5a",
            scrollbar_button_hover_color="#2a5a8a",
        )
        self._scroll.pack(padx=20, pady=(50, 5), fill="both", expand=True)

    def _build_bottom_frame(self):
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(padx=20, pady=(0, 18), fill="x")

        ctk.CTkButton(
            bottom,
            text="+ Adicionar",
            command=self._open_add_dialog,
        ).pack(side="left")

        ctk.CTkButton(
            bottom,
            text="─",
            width=32,
            height=24,
            command=self._hide_window,
        ).pack(side="left", padx=(8, 0))

        self.lbl_status = ctk.CTkLabel(
            bottom, text="", text_color="#5a7a9a"
        )
        self.lbl_status.pack(side="left", padx=(15, 0))

        self.btn_monitor = ctk.CTkButton(
            bottom,
            text="Iniciar Monitoramento",
            command=self._toggle_monitoring,
        )
        self.btn_monitor.pack(side="right")

    def _open_add_dialog(self):
        dlg = AddDialog(self)
        self.wait_window(dlg)
        if dlg.result is not None:
            self._refresh_list()

    def _remove(self, reminder_id):
        remove_reminder(reminder_id)
        self._refresh_list()

    def _edit(self, reminder):
        dlg = EditDialog(self, reminder)
        self.wait_window(dlg)
        if dlg.result is not None:
            self._refresh_list()

    def _refresh_list(self):
        for w in self._scroll.winfo_children():
            w.destroy()

        reminders = listar()
        if not reminders:
            lbl = ctk.CTkLabel(
                self._scroll,
                text="Nenhum lembrete cadastrado.",
                text_color="#4a6a8a",
            )
            lbl.pack(pady=40)
            return

        today = datetime.now(timezone.utc).date()
        for r in reminders:
            row = ctk.CTkFrame(self._scroll, fg_color="#111e2e", corner_radius=8)
            row.pack(fill="x", pady=3)

            next_dt = datetime.fromtimestamp(r["next_trigger"], tz=timezone.utc)
            remaining = r["next_trigger"] - time.time()
            if remaining <= 0:
                remaining_str = "agora"
            else:
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                remaining_str = f"{mins}min {secs}s"

            if next_dt.date() == today:
                hora = next_dt.strftime("%H:%M:%S")
            else:
                hora = next_dt.strftime("%d/%m %H:%M")

            ctk.CTkLabel(
                row,
                text=f"{r['message']}",
                anchor="w",
                width=200,
            ).pack(side="left", padx=(12, 4), pady=8)

            interval_h = r["interval"] // 60
            interval_m = r["interval"] % 60
            if interval_h:
                interval_str = f"{interval_h}h {interval_m}min"
            else:
                interval_str = f"{interval_m}min"

            ctk.CTkLabel(
                row,
                text=interval_str,
                anchor="w",
                width=70,
                text_color="#5a8aaa",
            ).pack(side="left", padx=4, pady=8)

            ctk.CTkLabel(
                row,
                text=f"{hora}  ({remaining_str})",
                anchor="w",
                width=170,
                text_color="#5a8aaa",
            ).pack(side="left", padx=4, pady=8)

            ctk.CTkButton(
                row,
                text="Editar",
                width=55,
                command=lambda r=r: self._edit(r),
            ).pack(side="right", padx=(0, 2))
            ctk.CTkButton(
                row,
                text="Remover",
                width=65,
                fg_color="#4a1a1a",
                hover_color="#6a2222",
                text_color="#d47a7a",
                command=lambda rid=r["id"]: self._remove(rid),
            ).pack(side="right", padx=2)

    def _monitor_loop(self):
        while not self._stop_event.is_set():
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
            self._stop_event.wait(1)

    def _toggle_monitoring(self):
        if self._monitoring:
            self._stop_event.set()
            if self._thread:
                self._thread.join(timeout=2)
            self._monitoring = False
            self.btn_monitor.configure(text="Iniciar Monitoramento")
            self.lbl_status.configure(text="")
        else:
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()
            self._monitoring = True
            self.btn_monitor.configure(text="Parar Monitoramento")
            self.lbl_status.configure(text="Monitorando...")
            self._poll_list()

    def _poll_list(self):
        if self._monitoring:
            self._refresh_list()
            self.after(3000, self._poll_list)


def run():
    App().mainloop()


if __name__ == "__main__":
    run()
