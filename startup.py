import os
import sys

from config import MAIN_SCRIPT, logger

# Windows-only: registers/removes a per-user auto-start entry, no admin rights needed.
STARTUP_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
STARTUP_VALUE_NAME = "FileOrganizer"


def get_launch_command() -> str:
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.exists(pythonw):
        pythonw = sys.executable
    return f'"{pythonw}" "{MAIN_SCRIPT}"'


def is_startup_enabled() -> bool:
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_REG_PATH) as key:
            winreg.QueryValueEx(key, STARTUP_VALUE_NAME)
        return True
    except OSError:
        return False


def set_startup_enabled(enabled: bool) -> None:
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
        if enabled:
            winreg.SetValueEx(key, STARTUP_VALUE_NAME, 0, winreg.REG_SZ, get_launch_command())
            logger.info("Enabled start on login")
        else:
            try:
                winreg.DeleteValue(key, STARTUP_VALUE_NAME)
            except FileNotFoundError:
                pass
            logger.info("Disabled start on login")
