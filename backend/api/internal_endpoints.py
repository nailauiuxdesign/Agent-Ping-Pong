# backend/api/internal_endpoints.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/internal")

@router.post("/episodes/{podcast_id}")
def create_episode(podcast_id: int, payload: dict):
    print(f"[internal] Episode update for podcast {podcast_id}: {payload}")
    return {"status": "ok", "episode": payload}

@router.put("/translations/{podcast_id}/{target_lang}")
def update_translation(podcast_id: int, target_lang: str, payload: dict):
    print(f"[internal] Translation update for podcast {podcast_id}, lang={target_lang}: {payload}")
    return {"status": "ok", "translation": payload}
