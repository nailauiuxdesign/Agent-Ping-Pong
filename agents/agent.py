
import sys
import json
import os

class Agent:
    def __init__(self, name):
        self.name = name

    def handle_message(self, msg):
        # Procesa el mensaje y responde
        response = {
            "type": "response",
            "content": f"{self.name} received: {msg.get('content', msg)}"
        }
        print(json.dumps(response), flush=True)

if __name__ == "__main__":
    agent_name = os.environ.get("AGENT_NAME", "PingPongAgent")
    agent = Agent(agent_name)
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            agent.handle_message(msg)
        except Exception as e:
            print(json.dumps({"type": "error", "error": str(e)}), flush=True)
