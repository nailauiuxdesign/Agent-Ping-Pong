class Agent:
    def __init__(self, name):
        self.name = name
        self.inbox = []

    def send_message(self, other_agent, message):
        print(f"{self.name} sends to {other_agent.name}: {message}")
        other_agent.inbox.append(message)

    def process_messages(self):
        while self.inbox:
            msg = self.inbox.pop(0)
            # Regla simple: responde con mensaje predeterminado
            response = f"Received '{msg}'!"
            print(f"{self.name} processes message: {msg} -> responds: {response}")
