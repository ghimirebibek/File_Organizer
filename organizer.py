import os
import shutil
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import logger

MISC_FOLDER = "Downloaded Misc"

CATEGORIES = {
    "Downloaded Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico",
    },
    "Downloaded Audio": {
        ".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma", ".aiff", ".alac",
        ".dsd", ".pcm", ".ape", ".au", ".mka", ".m3u", ".m3u8", ".pls", ".ra", ".rm",
        ".rmvb", ".vqf", ".mid", ".midi", ".mod", ".s3m", ".xm", ".it", ".mtm", ".umx",
        ".mo3", ".cda", ".wv", ".tak", ".tta", ".ofr", ".ofs", ".mpc", ".mpp", ".mp2",
        ".mp1", ".mpa", ".mpga", ".mpu", ".m1a", ".m2a", ".m4b", ".m4p", ".m4r",
    },
    "Downloaded Video": {
        ".mp4", ".avi", ".mov", ".m4v", ".mkv", ".wmv", ".flv", ".webm",
    },
    "Downloaded Programs": {
        ".exe", ".msi",
    },
    "Downloaded Documents": {
        ".txt", ".pdf", ".doc", ".docx", ".pptx", ".xlsx", ".ppt", ".xls", ".rtf",
        ".odt", ".ods", ".odp", ".odg", ".odf", ".odc", ".odb", ".odm", ".ott",
        ".stw", ".sxw", ".sxc", ".sxi", ".sxd", ".sxg", ".sxl", ".sxm",
    },
    MISC_FOLDER: set(),
}

# Browser/download-manager partial-file suffixes: never sort these, they're not finished yet.
IGNORED_SUFFIXES = {".tmp", ".crdownload", ".part", ".download"}


def ensure_category_folders(destination_root: str) -> None:
    os.makedirs(destination_root, exist_ok=True)
    for folder_name in CATEGORIES:
        path = os.path.join(destination_root, folder_name)
        if not os.path.exists(path):
            logger.info("Creating %s folder", folder_name)
            os.mkdir(path)


def category_for(extension: str) -> str:
    extension = extension.lower()
    for folder_name, extensions in CATEGORIES.items():
        if extension in extensions:
            return folder_name
    return MISC_FOLDER


def wait_until_stable(path: str, poll_interval: float = 1.0, timeout: float = 300.0) -> bool:
    """Poll a single file's size until it stops changing (download finished).
    Returns False if the file vanished (already moved/deleted) or the wait timed out."""
    start = time.monotonic()
    try:
        last_size = -1
        current_size = os.path.getsize(path)
        while last_size != current_size:
            last_size = current_size
            time.sleep(poll_interval)
            current_size = os.path.getsize(path)
            if time.monotonic() - start > timeout:
                logger.warning("Timed out waiting for %s to finish downloading", path)
                return False
        return True
    except FileNotFoundError:
        return False


def unique_destination(folder: str, filename: str) -> str:
    """If filename already exists in folder, append ' (1)', ' (2)', ... until it doesn't."""
    name, ext = os.path.splitext(filename)
    candidate = os.path.join(folder, filename)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(folder, f"{name} ({counter}){ext}")
        counter += 1
    return candidate


def organize_file(path: str, destination_root: str) -> None:
    filename = os.path.basename(path)
    _, extension = os.path.splitext(filename)
    if not extension or extension.lower() in IGNORED_SUFFIXES:
        return

    if not wait_until_stable(path):
        return

    category_folder = category_for(extension)
    destination = unique_destination(os.path.join(destination_root, category_folder), filename)

    try:
        shutil.move(path, destination)
        final_name = os.path.basename(destination)
        if final_name != filename:
            logger.info(
                "Moved %s -> %s (renamed to %s, a file with that name already existed)",
                filename, category_folder, final_name,
            )
        else:
            logger.info("Moved %s -> %s", filename, category_folder)
    except OSError as exc:
        logger.warning("Could not move %s: %s", filename, exc)


def organize_existing_files(watch_folder: str, destination_root: str) -> None:
    logger.info("Sorting existing files in %s", watch_folder)
    for entry in os.listdir(watch_folder):
        path = os.path.join(watch_folder, entry)
        if os.path.isfile(path):
            organize_file(path, destination_root)


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, destination_root: str):
        self.destination_root = destination_root

    def on_created(self, event):
        if not event.is_directory:
            organize_file(event.src_path, self.destination_root)

    def on_moved(self, event):
        # Browsers often download to a temp name (e.g. "file.crdownload") and
        # rename it to the final name once the download completes.
        if not event.is_directory:
            organize_file(event.dest_path, self.destination_root)


class WatcherService:
    """Starts/stops the folder watch. Safe to toggle repeatedly from the tray menu."""

    def __init__(self, watch_folder: str, destination_root: str):
        self.watch_folder = watch_folder
        self.destination_root = destination_root
        self.observer = None
        self._lock = threading.Lock()

    @property
    def running(self) -> bool:
        return self.observer is not None and self.observer.is_alive()

    def start(self) -> None:
        with self._lock:
            if self.running:
                return
            ensure_category_folders(self.destination_root)
            organize_existing_files(self.watch_folder, self.destination_root)

            handler = DownloadHandler(self.destination_root)
            observer = Observer()
            observer.schedule(handler, self.watch_folder, recursive=False)
            observer.start()
            self.observer = observer
            logger.info(
                "Watching %s (sorting into %s)...", self.watch_folder, self.destination_root
            )

    def stop(self) -> None:
        with self._lock:
            if not self.running:
                return
            self.observer.stop()
            self.observer.join()
            self.observer = None
            logger.info("Stopped watching.")

    def reconfigure(self, watch_folder: str, destination_root: str) -> None:
        was_running = self.running
        self.stop()
        self.watch_folder = watch_folder
        self.destination_root = destination_root
        if was_running:
            self.start()
