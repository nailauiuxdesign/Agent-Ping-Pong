# backend/main.py
import subprocess, sys, json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PodcastRequest(BaseModel):
    rss_feed_url: str
    target_lang: str = "es"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/podcasts")
def create_podcast(req: PodcastRequest):
    msg = {
        "sender": "api",
        "receiver": "orchestrator",
        "content": req.rss_feed_url,
        "target_lang": req.target_lang
    }
    proc = subprocess.run(
        [sys.executable, "agents/orchestrator/agent_api_integrated.py"],
        input=json.dumps(msg) + "\n",
        text=True,
        capture_output=True
    )
    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=proc.stderr)
    try:
        response = json.loads(proc.stdout)
        return {"episodes": response.get("content")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {proc.stdout}")