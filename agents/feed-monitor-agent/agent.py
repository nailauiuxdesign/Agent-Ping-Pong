from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import subprocess
import os
import time
import threading
import json
import sys

app = FastAPI(title="Feed Monitor Agent")

FEEDS_FILE = "feeds.txt"
POLL_INTERVAL = 120  # segundos (2 minutos)
ORCHESTRATOR_SCRIPT = "../../agents/orchestrator/agent.py"  # Ruta al orquestador

def get_feeds():
    """Lee los feeds desde el archivo feeds.txt."""
    feeds_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", FEEDS_FILE))
    if not os.path.exists(feeds_file_path):
        raise FileNotFoundError(f"Feeds file not found: {feeds_file_path}")
    with open(feeds_file_path) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def run_orchestrator(feed_url):
    """Llama al orquestador para procesar un feed."""
    proc = subprocess.Popen(
        [os.sys.executable, ORCHESTRATOR_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    coral_msg = {
        "sender": "feed-monitor-agent",
        "receiver": "orchestrator",
        "content": feed_url
    }
    stdout, _ = proc.communicate(input=json.dumps(coral_msg) + "\n")
    return stdout.strip()

def monitor_feeds():
    """Monitorea los feeds en feeds.txt y llama al orquestador."""
    print(f"[Feed Monitor] Monitoring feeds listed in {FEEDS_FILE} every {POLL_INTERVAL} seconds...")
    while True:
        try:
            feeds = get_feeds()
            print(f"[Feed Monitor] {len(feeds)} feeds pendientes de procesar en este ciclo.")
            for idx, feed_url in enumerate(feeds, 1):
                print(f"[Feed Monitor] ({idx}/{len(feeds)}) Checking feed: {feed_url}")
                try:
                    result = run_orchestrator(feed_url)
                    print(f"[Feed Monitor] Orchestrator response for {feed_url}: {result}")
                except Exception as e:
                    print(f"[Feed Monitor] Error processing feed {feed_url}: {e}")
            print(f"[Feed Monitor] Sleeping {POLL_INTERVAL} seconds...")
            time.sleep(POLL_INTERVAL)
        except Exception as e:
            print(f"[Feed Monitor] Unexpected error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    monitor_thread = threading.Thread(target=monitor_feeds, daemon=True)
    monitor_thread.start()
    print("[Feed Monitor] Monitoring thread started.")
    yield  # Application is running
    print("[Feed Monitor] Application shutdown. Monitoring thread will stop.")

app = FastAPI(title="Feed Monitor Agent", lifespan=lifespan)

@app.get("/")
def read_root():
    """Endpoint básico para verificar que el agente está funcionando."""
    return {"message": "Feed Monitor Agent is running"}

@app.post("/trigger")
def trigger_monitoring():
    """Endpoint para forzar un ciclo de monitoreo manual."""
    try:
        feeds = get_feeds()
        results = []
        for feed_url in feeds:
            result = run_orchestrator(feed_url)
            results.append({"feed_url": feed_url, "result": result})
        return {"message": "Manual feed monitoring completed", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Cambia el puerto si es necesario