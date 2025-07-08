import subprocess
import time
from threading import Thread

Thread(target=lambda: subprocess.run(["python","src/Back End/watcher.py"])).start()

Thread(target=lambda: subprocess.run(["python","src/Front End/gui.py"]),daemon=True).start()