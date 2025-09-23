# backend/api/agent_integration.py
import subprocess, sys, json
from pathlib import Path

class AgentManager:
    def __init__(self):
        base = Path(__file__).resolve().parent.parent  # project-root/backend
        self.orchestrator_path = str(base / "agents" / "orchestrator" / "agent_api_integrated.py")

    def process_rss_feed(self, feed_url: str, target_lang: str = "es", podcast_id: int = 1):
        msg = {
            "sender": "api",
            "receiver": "orchestrator",
            "content": feed_url,
            "podcast_id": podcast_id,
            "target_lang": target_lang
        }
        proc = subprocess.run(
            [sys.executable, self.orchestrator_path],
            input=json.dumps(msg) + "\n",
            text=True,
            capture_output=True
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Agent error: {proc.stderr}")
        try:
            return json.loads(proc.stdout)
        except Exception:
            raise RuntimeError(f"Invalid JSON from orchestrator: {proc.stdout}")
