"""The Axiom agent loop - ties brain + memory + tools together."""
from .brain import Brain
from .memory import Memory


class Axiom:
    def __init__(self):
        self.memory = Memory()
        self.brain = Brain()

    def say(self, user_text: str) -> str:
        self.memory.log_turn("user", user_text)
        reply = self.brain.think(user_text, self.memory)
        self.memory.log_turn("assistant", reply)
        return reply
