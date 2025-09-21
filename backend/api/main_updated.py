# backend/api/main_updated.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_integration import AgentManager
from internal_endpoints import router as internal_router

app = FastAPI(title="Global Podcaster API")
agent_manager = AgentManager()

class PodcastRequest(BaseModel):
    rss_feed_url: str
    target_lang: str = "es"

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/podcasts")
def create_podcast(req: PodcastRequest):
    try:
        result = agent_manager.process_rss_feed(req.rss_feed_url, req.target_lang, podcast_id=1)
        return {"episodes": result.get("content")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# include internal agent routes
app.include_router(internal_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
