import sys
import json
import subprocess


def call_rss_monitor_agent(feed_url):
    proc = subprocess.Popen(
        [sys.executable, "agents/rss-monitor-agent/agent.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    coral_msg = {
        "sender": "orchestrator",
        "receiver": "rss-monitor-agent",
        "content": feed_url
    }
    stdout, _ = proc.communicate(input=json.dumps(coral_msg) + "\n")
    response = json.loads(stdout)
    return response.get("content", [])

def call_transcription_agent(audio_url):
    proc = subprocess.Popen(
        [sys.executable, "agents/transcription-agent/agent.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    coral_msg = {
        "sender": "orchestrator",
        "receiver": "transcription-agent",
        "content": audio_url
    }
    stdout, _ = proc.communicate(input=json.dumps(coral_msg) + "\n")
    response = json.loads(stdout)
    return response.get("content", "")

def call_translation_agent(text, target_lang="es"):
    proc = subprocess.Popen(
        [sys.executable, "agents/translation-agent/agent.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    coral_msg = {
        "sender": "orchestrator",
        "receiver": "translation-agent",
        "content": text,
        "target_lang": target_lang
    }
    stdout, _ = proc.communicate(input=json.dumps(coral_msg) + "\n")
    response = json.loads(stdout)
    return response.get("content", "")

def call_tts_agent(text, voice_id=None):
    msg = {"sender":"orchestrator","receiver":"tts-agent","content":text}
    if voice_id:
        msg["voice_id"] = voice_id
    return run_agent("agents/tts-agent/agent.py", msg)  # assuming run_agent returns parsed content


if __name__ == "__main__":
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            feed_url = msg.get("content")
            new_episodes = call_rss_monitor_agent(feed_url)
            print("DEBUG NEW EPISODES:", new_episodes, file=sys.stderr)
            if not isinstance(new_episodes, list) or not new_episodes:
                response = {
                    "sender": "orchestrator",
                    "receiver": msg["sender"],
                    "content": "No hay episodios nuevos."
                }
                print(json.dumps(response), flush=True)
                continue
            # Procesar cada episodio nuevo
            results = []
            target_lang = msg.get("target_lang", "es")
            for ep in new_episodes:
                audio_url = ep.get("audio_url")
                if not audio_url:
                    continue
                print(f"DEBUG: Procesando audio_url: {audio_url}", file=sys.stderr)
                transcript = call_transcription_agent(audio_url)
                print(f"DEBUG: Transcript obtenido: {transcript[:100]}...", file=sys.stderr)
                translation = call_translation_agent(transcript, target_lang)
                print(f"DEBUG: Traducción obtenida: {translation[:100]}...", file=sys.stderr)
                results.append({
                    "title": ep.get("title"),
                    "audio_url": audio_url,
                    "transcript": transcript,
                    "translation": translation
                })
            response = {
                "sender": "orchestrator",
                "receiver": msg["sender"],
                "content": results
            }

            # previous flow produced 'translation' (string) and you may have language info
            tts_result = call_tts_agent(translation, voice_id=os.getenv("TTS_DEFAULT_VOICE_ID"))
            # tts_result expected to be a dict with audio_url
            audio_url = tts_result.get("audio_url") or tts_result.get("content",{}).get("audio_url")
            # now you can pass audio_url to RSS publisher or return it to the user

            print(json.dumps(response), flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_response = {
                "sender": "transcription-agent",
                "receiver": msg.get("sender", "unknown"),
                "content": f"Error: {str(e)}"
            }
            print(json.dumps(error_response), flush=True)