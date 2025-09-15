import time
import sys
import json

FEEDS_FILE = "feeds.txt"
POLL_INTERVAL = 120  # segundos (2 minutos)

def get_feeds():
    with open(FEEDS_FILE) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def run_orchestrator(feed_url):
    proc = subprocess.Popen(
        [sys.executable, "agents/agent.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    coral_msg = {
        "sender": "monitor",
        "receiver": "orchestrator",
        "content": feed_url
    }
    stdout, _ = proc.communicate(input=json.dumps(coral_msg) + "\n")
    print(stdout)

if __name__ == "__main__":
    import subprocess
    print(f"[RSS Monitor Loop] Monitoring feeds listed in {FEEDS_FILE} every {POLL_INTERVAL} seconds...")
    while True:
        feeds = get_feeds()
        print(f"[RSS Monitor Loop] {len(feeds)} feeds pendientes de procesar en este ciclo.")
        for idx, feed_url in enumerate(feeds, 1):
            print(f"[RSS Monitor Loop] ({idx}/{len(feeds)}) Checking feed: {feed_url}")
            run_orchestrator(feed_url)
        print(f"[RSS Monitor Loop] Sleeping {POLL_INTERVAL} seconds...")
        time.sleep(POLL_INTERVAL)
