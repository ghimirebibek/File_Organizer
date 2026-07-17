import tkinter as tk

from config import DESTINATION_ROOT, FOLDER_TO_TRACK
from organizer import WatcherService
from tray_app import build_tray_icon


def main() -> None:
    service = WatcherService(FOLDER_TO_TRACK, DESTINATION_ROOT)
    service.start()

    root = tk.Tk()
    root.withdraw()  # no visible window until Settings is opened

    icon = build_tray_icon(service, root)
    icon.run_detached()

    root.mainloop()


if __name__ == "__main__":
    main()
