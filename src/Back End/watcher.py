import time
import json
import os
import psutil
import win32gui
import win32process
import subprocess
from threading import Thread

# التطبيقات النظامية اللي ما نغلقها حتى لو مش في القائمة
system_whitelist = [
    "explorer.exe",
    "searchapp.exe",
    "startmenuexperiencehost.exe",
    "ctfmon.exe",
    "runtimebroker.exe",
    "shellexperiencehost.exe",
    "applicationframehost.exe",
    "python.exe",
    "photos.exe"
]

# تحميل التطبيقات المسموحة من المستخدم
def load_allowed_apps():
    try:
        with open("allowed_apps.json", "r") as f:
            return [os.path.basename(p).lower() for p in json.load(f)]
    except:
        return []

# معرفة التطبيق النشط
def get_active_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        return proc.name().lower(), pid
    except Exception:
        return None, None

# مراقبة التطبيق النشط
def monitor_active_window():
    allowed_apps = load_allowed_apps()
    print("🚀 بدأ المراقبة الذكية للنوافذ...")

    while True:
        name, pid = get_active_process_name()

        if name not in allowed_apps and name not in system_whitelist and pid != None:
            try:
                psutil.Process(pid).kill()
                print(name ,"غير مسموح به")
                Thread(target=lambda: subprocess.run(["python","gui.py"]),daemon=True).start()
            except Exception as e:
                print(f"⚠️ تعذر الإغلاق: {e}")

        time.sleep(1)

if __name__ == "__main__":
    monitor_active_window()
