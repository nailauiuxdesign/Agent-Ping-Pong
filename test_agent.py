import os
import subprocess
import json

# Mensajes de prueba
messages = [
    {"content": "Hi agent"},
    {"content": "How are you?"},
    {"content": "Ping Pong!"},
]

# Inicia el agente como subproceso
proc = subprocess.Popen(
    ["python3", "agents/agent.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    env={**os.environ, "AGENT_NAME": "TestAgent"}
)

# Envía los mensajes y lee las respuestas
for msg in messages:
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    response = proc.stdout.readline()
    print("Respuesta del agente:", response.strip())

proc.stdin.close()
proc.terminate()