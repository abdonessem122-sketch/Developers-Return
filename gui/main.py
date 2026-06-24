import ctypes
import platform
from .windows import Window

if platform.system() == "Linux":
    exploit = ctypes.CDLL("exploits.so")
elif platform.system() == "Windows":
    exploit = ctypes.WinDLL("exploits.dll")
else:
    raise OSError("Unsupported OS")

root = Window(800 , 600 , "Developer Return 1.0 Alpha")
root.create_menu_bar()
