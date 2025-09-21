import sys
import json
import subprocess
import os

# --- Helper to run sub-agents ---
def run_agent(agent_path, msg):
    proc = subprocess.Popen(
        [sys.executable, agent_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(input=json.dumps(msg) + "\n")

    if proc.returncode != 0:
        raise RuntimeError(f"Agent {agent_path} failed: {stderr}")

    try:
        return json.loads(stdout)
    except Exception as e:
        raise RuntimeError(f"Invalid JSON from {agent_path}: {stdout}\nError: {str(e)}")

# --- Agent call wrappers ---
def call_rss_fetch(feed_url):
    path = os.path.join(os.path.dirname(__file__), "..", "rss-fetch-agent", "agent.py")
    msg = {"sender": "orchestrator", "receiver": "rss-fetch-agent", "content": feed_url}
    return run_agent(path, msg).get("content", [])

def call_transcription(audio_url):
    path = os.path.join(os.path.dirname(__file__), "..", "transcription-agent", "agent.py")
    msg = {"sender": "orchestrator", "receiver": "transcription-agent", "content": audio_url}
    return run_agent(path, msg).get("content", "")

def call_translation(text, target_lang="es"):
    path = os.path.join(os.path.dirname(__file__), "..", "translation-agent", "agent.py")
    msg = {
        "sender": "orchestrator",
        "receiver": "translation-agent",
        "content": text,
        "target_lang": target_lang
    }
    return run_agent(path, msg).get("content", "")

def call_tts(text, voice_id=None):
    path = os.path.join(os.path.dirname(__file__), "..", "tts-agent", "agent.py")
    msg = {
        "sender": "orchestrator",
        "receiver": "tts-agent",
        "content": text
    }
    if voice_id:
        msg["voice_id"] = voice_id
    return run_agent(path, msg).get("content", "")

# --- Main orchestrator flow ---
if __name__ == "__main__":
    for line in sys.stdin:
        msg = {}
        try:
            msg = json.loads(line)
            feed_url = msg.get("content")
            target_lang = msg.get("target_lang", "es")
            podcast_id = msg.get("podcast_id", 1)

            # 1. Fetch RSS
            entries = call_rss_fetch(feed_url)
            if not entries or not entries[0].get("audio_url"):
                response = {
                    "sender": "orchestrator",
                    "receiver": msg["sender"],
                    "content": "No audio found in RSS feed."
                }
                print(json.dumps(response), flush=True)
                continue

            # Take first episode only for demo
            audio_url = entries[0]["audio_url"]

            # 2. Transcribe audio
            transcript = call_transcription(audio_url)

            # 3. Translate
            translation = call_translation(transcript, target_lang)

            # 4. Generate TTS
            audio_file = call_tts(translation)

            # Final response
            response = {
                "sender": "orchestrator",
                "receiver": msg["sender"],
                "content": {
                    "transcript": transcript,
                    "translation": translation,
                    "audio_file": audio_file
                },
                "podcast_id": podcast_id
            }
            print(json.dumps(response), flush=True)

        except Exception as e:
            import traceback
            traceback.print_exc()
            error_response = {
                "sender": "orchestrator",
                "receiver": msg.get("sender", "unknown"),
                "content": f"Error: {str(e)}"
            }
            print(json.dumps(error_response), flush=True)
