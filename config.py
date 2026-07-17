import logging
import os
import sys

from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "main.py")
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")
LOG_FILE = os.path.join(SCRIPT_DIR, "watcher.log")

load_dotenv(ENV_FILE)

# Under pythonw.exe there is no console, so sys.stderr is None and a StreamHandler
# would crash on the first log call.
_handlers = [logging.FileHandler(LOG_FILE, encoding="utf-8")]
if sys.stderr is not None:
    _handlers.append(logging.StreamHandler())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=_handlers,
)
logger = logging.getLogger("file_organizer")


def get_folder_to_track() -> str:
    """Resolve the folder to watch: FOLDER_TO_TRACK in .env/env wins, otherwise
    the OS Downloads folder is looked up (registry on Windows, ~/Downloads elsewhere)."""
    env_folder = os.getenv("FOLDER_TO_TRACK")
    if env_folder:
        return env_folder

    try:
        import winreg
        shell_folders = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, shell_folders) as key:
            return winreg.QueryValueEx(key, downloads_guid)[0]
    except (OSError, ImportError):
        pass

    return os.path.join(os.path.expanduser("~"), "Downloads")


def get_destination_root(watch_folder: str) -> str:
    """Where the category subfolders get created. Defaults to the watched folder itself."""
    return os.getenv("DESTINATION_ROOT") or watch_folder


FOLDER_TO_TRACK = get_folder_to_track()
DESTINATION_ROOT = get_destination_root(FOLDER_TO_TRACK)
