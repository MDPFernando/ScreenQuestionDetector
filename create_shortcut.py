import os
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut():
    desktop = winshell.desktop()
    path = os.path.join(desktop, "Screen Question Detector.lnk")
    
    # Target is the compiled executable in the dist folder
    target = os.path.abspath(r"dist\Screen Question Detector.exe")
    
    # Working directory MUST be the project root so it can find the .env file
    working_dir = os.path.abspath(".")
    
    icon = os.path.abspath("icon.ico")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = working_dir
    shortcut.IconLocation = icon
    shortcut.save()
    
    print(f"Shortcut created successfully at: {path}")

if __name__ == "__main__":
    create_desktop_shortcut()
