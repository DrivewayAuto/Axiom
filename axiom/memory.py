"""Axiom's memory: this is how it 'remembers and learns'.

Two layers:
  1. conversation_log.jsonl  - the full transcript, append-only (long-term recall)
  2. memory.json             - distilled facts Axiom has chosen to remember
                               (e.g. "Bobby works at Driveway Auto Doctor")
"""
import json
import time
from . import config


class Memory:
    def __init__(self):
        self.facts = self._load_facts()

    # ---------- learned facts ----------
    def _load_facts(self):
        if config.MEMORY_FILE.exists():
            return json.loads(config.MEMORY_FILE.read_text())
        return {"facts": []}

    def remember(self, fact: str):
        """Store a durable fact. This is the 'learning' step."""
        entry = {"fact": fact, "learned_at": time.strftime("%Y-%m-%d %H:%M")}
        self.facts["facts"].append(entry)
        config.MEMORY_FILE.write_text(json.dumps(self.facts, indent=2))
        return f"Got it - I'll remember that: {fact}"

    def recall(self) -> str:
        """Everything Axiom knows, formatted for its context."""
        if not self.facts["facts"]:
            return "(nothing learned yet)"
        return "\n".join(f"- {f['fact']}" for f in self.facts["facts"])

    def forget_all(self):
        self.facts = {"facts": []}
        config.MEMORY_FILE.write_text(json.dumps(self.facts, indent=2))

    # ---------- conversation log ----------
    def log_turn(self, role: str, content: str):
        with open(config.CONVO_FILE, "a") as f:
            f.write(json.dumps({"t": time.time(), "role": role, "content": content}) + "\n")

    def recent_turns(self, n=None):
        n = n or config.SHORT_TERM_WINDOW
        if not config.CONVO_FILE.exists():
            return []
        lines = config.CONVO_FILE.read_text().splitlines()[-n:]
        return [json.loads(l) for l in lines]
