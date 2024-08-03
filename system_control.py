import socket
import os
import pyautogui
import ctypes

def is_connected():
    """Check if the system is connected to the internet."""
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def control_system(action):
    """Perform a system control action (e.g., shutdown, restart, etc.)."""
    actions = {
        "shutdown": "shutdown /s /t 1",
        "restart": "shutdown /r /t 1",
        "log off": "shutdown /l",
        "volume up": "nircmd.exe changesysvolume 2000",
        "volume down": "nircmd.exe changesysvolume -2000",
        "mute": "nircmd.exe mutesysvolume 1",
        "unmute": "nircmd.exe mutesysvolume 0"
    }

    try:
        if action in actions:
            os.system(actions[action])
            return f"{action.capitalize()} executed."
        elif action == "screenshot":
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            return "Screenshot taken."
        elif action.startswith("brightness"):
            try:
                level = int(action.split()[-1])
                set_brightness(level)
                return f"Brightness set to {level}%."
            except ValueError:
                return "Invalid brightness level specified."
        else:
            return "Unknown system control action."
    except Exception as e:
        return f"Error executing system control action: {e}"

def set_brightness(level):
    """Set the screen brightness to the specified level."""
    level = max(0, min(level, 100))

    class PHYSICAL_MONITOR(ctypes.Structure):
        _fields_ = [('handle', ctypes.wintypes.HANDLE),
                    ('description', ctypes.wintypes.WCHAR * 128)]

    user32 = ctypes.windll.user32
    hdc = user32.GetDC(0)
    monitors = (PHYSICAL_MONITOR * 1)()
    monitor_count = ctypes.c_uint()

    if user32.GetPhysicalMonitorsFromHDC(hdc, monitor_count, monitors):
        for monitor in monitors:
            user32.SetMonitorBrightness(monitor.handle, level)
    user32.ReleaseDC(0, hdc)
