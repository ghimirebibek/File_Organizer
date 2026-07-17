# File Organizer — Automatically Sort Your Windows Downloads Folder

A lightweight Python system tray app that watches your Downloads folder (or any folder you choose) and automatically sorts new files into subfolders by type — images, audio, video, programs, documents, and everything else. No more digging through a messy Downloads folder.

This started as a first automation project — a simple script to sort files, since grown into a small always-on tray application with a Settings GUI, auto-start on login, and live folder watching.

**Platform: Windows only.** It relies on the Windows registry (auto-detecting your Downloads folder and registering auto-start) and `os.startfile`. It will not run as-is on macOS or Linux.

## Features

- **Automatic sorting** — watches a folder in real time and moves new files into `Downloaded Images`, `Downloaded Audio`, `Downloaded Video`, `Downloaded Programs`, `Downloaded Documents`, or `Downloaded Misc` based on file extension.
- **Download-aware** — waits for a file's size to stop changing before moving it, so in-progress downloads never get moved half-finished. Partial-download files (`.crdownload`, `.part`, `.tmp`, `.download`) are ignored until they're complete.
- **System tray app** — runs quietly in the background with a status icon (green = watching, grey = stopped). No terminal window required.
- **Manual on/off switch** — start or stop watching anytime from the tray menu, without closing the app.
- **Settings GUI** — pick your source (watched) folder and destination folder with a folder browser, no config file editing required.
- **Optional auto-start on login** — a checkbox in the tray menu, off by default.
- **Configurable via `.env`** — for anyone who prefers editing a text file over a GUI.

## Requirements

- Windows 10/11
- Python 3.9+

## Installation

```
pip install -r requirements.txt
```

This installs `watchdog` (filesystem watching), `python-dotenv` (config file support), `pystray` (system tray icon), and `Pillow` (icon rendering).

## Usage

Run it:

```
python main.py
```

Or launch it without a console window using `pythonw`:

```
pythonw main.py
```

Once running, look for its dot icon in the system tray (you may need to click the "^" overflow arrow to see it). Right-click it to open the menu:

| Menu item | What it does |
|---|---|
| **Status: Running / Stopped** | Read-only indicator of the current state |
| **Start Watching / Stop Watching** | Manual on/off switch — pause or resume without closing the app |
| **Settings...** | Opens a window to change the watched folder and/or destination folder |
| **Open Log** | Opens `watcher.log`, which records every file moved and any errors |
| **Open Watched Folder** | Opens the folder currently being watched |
| **Open Destination Folder** | Opens the folder where sorted subfolders are created |
| **Start with Windows** | Checkbox — enable to launch automatically (via `pythonw`, no console window) next time you log in. Off by default; toggle anytime |
| **Exit** | Stops watching and closes the app |

### Changing the watched or destination folder

The easiest way: **Settings...** in the tray menu. Browse to a source folder (the one to watch) and a destination folder (where the sorted subfolders get created — this can be the same as the source, or a completely different folder/drive). Click **Save** and it takes effect immediately, no restart needed.

Alternatively, copy `.env.example` to `.env` and set the values directly:

```
FOLDER_TO_TRACK=C:\Users\YourName\Downloads
DESTINATION_ROOT=C:\Users\YourName\Downloads
```

If `FOLDER_TO_TRACK` is left unset, the OS Downloads folder is detected automatically. If `DESTINATION_ROOT` is left unset, it defaults to the watched folder (subfolders are created inside it).

## Project structure

| File | Responsibility |
|---|---|
| `main.py` | Entry point — starts the watcher and the tray app |
| `config.py` | Environment/`.env` loading, logging setup, folder resolution |
| `organizer.py` | Core sorting logic: file categories, the watch handler, start/stop service |
| `tray_app.py` | Builds the system tray icon and menu |
| `settings_window.py` | The Settings GUI (Tkinter) |
| `startup.py` | Windows "run at login" registration |
| `icons.py` | Generates the green/grey tray icon images |

## Contributing

Issues and pull requests are welcome — this is a small, evolving personal-automation project, and improvements (including cross-platform support) are appreciated.
