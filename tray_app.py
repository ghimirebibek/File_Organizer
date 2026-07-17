import os
import tkinter as tk

import pystray

from config import LOG_FILE
from icons import ICON_OFF, ICON_ON
from organizer import WatcherService
from settings_window import show_settings_window
from startup import is_startup_enabled, set_startup_enabled


def build_tray_icon(service: WatcherService, root: tk.Tk) -> pystray.Icon:
    def toggle(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        if service.running:
            service.stop()
        else:
            service.start()
        icon.icon = ICON_ON if service.running else ICON_OFF

    def open_log(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        os.startfile(LOG_FILE)

    def open_watch_folder(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        os.startfile(service.watch_folder)

    def open_destination_folder(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        os.startfile(service.destination_root)

    def open_settings(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        root.after(0, lambda: show_settings_window(root, service, icon))

    def quit_app(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        service.stop()
        icon.stop()
        root.after(0, root.quit)

    def toggle_startup(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        set_startup_enabled(not is_startup_enabled())

    menu = pystray.Menu(
        pystray.MenuItem(
            lambda item: "Status: Running" if service.running else "Status: Stopped",
            None,
            enabled=False,
        ),
        pystray.MenuItem(
            lambda item: "Stop Watching" if service.running else "Start Watching",
            toggle,
        ),
        pystray.MenuItem("Settings...", open_settings),
        pystray.MenuItem("Open Log", open_log),
        pystray.MenuItem("Open Watched Folder", open_watch_folder),
        pystray.MenuItem("Open Destination Folder", open_destination_folder),
        pystray.MenuItem(
            "Start with Windows",
            toggle_startup,
            checked=lambda item: is_startup_enabled(),
        ),
        pystray.MenuItem("Exit", quit_app),
    )

    return pystray.Icon("file_organizer", ICON_ON, "File Organizer", menu)
