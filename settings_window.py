import os
import tkinter as tk
from tkinter import filedialog, messagebox

import pystray
from dotenv import set_key

from config import ENV_FILE, SCRIPT_DIR, logger
from icons import ICON_OFF, ICON_ON
from organizer import WatcherService


def show_settings_window(root: tk.Tk, service: WatcherService, icon: pystray.Icon) -> None:
    # Called via root.after() so it always runs on the Tk thread, never directly
    # from pystray's own thread (mixing two native event loops on one thread deadlocks).
    window = tk.Toplevel(root)
    window.title("File Organizer Settings")
    window.resizable(False, False)

    watch_var = tk.StringVar(value=service.watch_folder)
    dest_var = tk.StringVar(value=service.destination_root)

    def browse(var: tk.StringVar) -> None:
        chosen = filedialog.askdirectory(parent=window, initialdir=var.get() or SCRIPT_DIR)
        if chosen:
            var.set(chosen)

    tk.Label(window, text="Folder to watch (source):").grid(
        row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0)
    )
    tk.Entry(window, textvariable=watch_var, width=48).grid(row=1, column=0, padx=(10, 0), pady=4)
    tk.Button(window, text="Browse...", command=lambda: browse(watch_var)).grid(
        row=1, column=1, padx=10, pady=4
    )

    tk.Label(window, text="Destination folder (where sorted subfolders go):").grid(
        row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0)
    )
    tk.Entry(window, textvariable=dest_var, width=48).grid(row=3, column=0, padx=(10, 0), pady=4)
    tk.Button(window, text="Browse...", command=lambda: browse(dest_var)).grid(
        row=3, column=1, padx=10, pady=4
    )

    def on_save() -> None:
        watch_folder = watch_var.get().strip()
        destination_root = dest_var.get().strip() or watch_folder

        if not os.path.isdir(watch_folder):
            messagebox.showerror(
                "Invalid folder", f"Folder to watch does not exist:\n{watch_folder}", parent=window
            )
            return
        try:
            os.makedirs(destination_root, exist_ok=True)
        except OSError as exc:
            messagebox.showerror(
                "Invalid folder", f"Could not create destination folder:\n{exc}", parent=window
            )
            return

        set_key(ENV_FILE, "FOLDER_TO_TRACK", watch_folder)
        set_key(ENV_FILE, "DESTINATION_ROOT", destination_root)

        service.reconfigure(watch_folder, destination_root)
        icon.icon = ICON_ON if service.running else ICON_OFF
        logger.info("Settings updated: watching %s, sorting into %s", watch_folder, destination_root)
        window.destroy()

    button_row = tk.Frame(window)
    button_row.grid(row=4, column=0, columnspan=2, pady=12)
    tk.Button(button_row, text="Save", command=on_save, width=10).pack(side="left", padx=5)
    tk.Button(button_row, text="Cancel", command=window.destroy, width=10).pack(side="left", padx=5)

    window.lift()
    window.attributes("-topmost", True)
    window.after(100, lambda: window.attributes("-topmost", False))
    window.focus_force()
