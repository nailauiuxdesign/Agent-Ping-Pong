from agent import Agent
import time

# Creamos dos agentes
agent1 = Agent("Agent1")
agent2 = Agent("Agent2")

# Simulación simple
agent1.send_message(agent2, "Hello Agent2!")
agent2.process_messages()

agent2.send_message(agent1, "Hi Agent1! Got your message.")
agent1.process_messages()
