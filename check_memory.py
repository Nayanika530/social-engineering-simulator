import psutil
import subprocess
import time
import sys
process = subprocess.Popen([sys.executable, "app/app.py"], env={**__import__("os").environ, "FLASK_DEBUG": "0"})
time.sleep(25)
p = psutil.Process(process.pid)
mem_mb = p.memory_info().rss / 1024 / 1024
print(f"\nActual RAM used: {mem_mb:.0f} MB")
process.terminate()
