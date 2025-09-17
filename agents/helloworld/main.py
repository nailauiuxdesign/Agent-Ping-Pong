import sys
import json

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            content = msg.get("content", "")
            if content.strip().lower() == "helloworld":
                response = {
                    "sender": "helloworld-agent",
                    "receiver": msg.get("sender", "unknown"),
                    "content": "goodbye world"
                }
            else:
                response = {
                    "sender": "helloworld-agent",
                    "receiver": msg.get("sender", "unknown"),
                    "content": "unknown command"
                }
            print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {
                "sender": "helloworld-agent",
                "receiver": "unknown",
                "content": f"error: {str(e)}"
            }
            print(json.dumps(error_response), flush=True)
