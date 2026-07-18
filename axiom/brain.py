"""Axiom's brain: the connection to the language model.

With an ANTHROPIC_API_KEY it uses Claude (full master-mechanic reasoning + tools).
Without one it runs a limited mock that still nails the exact lookups
(trouble codes, oil capacity, wiring sources) from the offline data.
"""
import re
from . import config, tools

CODE_RE = re.compile(r"\b([PBCU][0-9]{4})\b", re.IGNORECASE)


class Brain:
    def __init__(self):
        self.client = None
        if config.ANTHROPIC_API_KEY:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
            except Exception as e:
                print(f"[brain] Could not start Anthropic client ({e}); using mock mode.")

    def think(self, user_text, memory):
        if self.client is None:
            return self._mock(user_text, memory)
        return self._real(user_text, memory)

    # ---------- real LLM path ----------
    def _real(self, user_text, memory):
        system = config.PERSONA + "\n\nWhat you remember about this person/vehicle:\n" + memory.recall()
        history = [{"role": t["role"], "content": t["content"]} for t in memory.recent_turns()]
        messages = history + [{"role": "user", "content": user_text}]
        # Live web search: Anthropic runs the searches server-side. Axiom uses it
        # for specs, TSBs, recalls, and known-pattern failures not in local files.
        all_tools = tools.SCHEMAS + [{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
        for _ in range(10):
            resp = self.client.messages.create(
                model=config.MODEL, max_tokens=2500, system=system,
                tools=all_tools, messages=messages,
            )
            if resp.stop_reason == "pause_turn":
                # Mid web-search - hand the partial turn back and let it continue.
                messages.append({"role": "assistant", "content": resp.content})
                continue
            if resp.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": resp.content})
                results = []
                for block in resp.content:
                    if block.type == "tool_use":
                        out = tools.run_tool(block.name, block.input, memory)
                        results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(out)})
                messages.append({"role": "user", "content": results})
                continue
            return "".join(b.text for b in resp.content if b.type == "text")
        return "(stopped after too many tool calls)"

    # ---------- offline mock path ----------
    def _mock(self, user_text, memory):
        t = user_text.lower()

        if "what do you know" in t or "what do you remember" in t:
            return "Here's what I've learned so far:\n" + memory.recall()

        # Exact OBD-II code lookup (works great offline)
        m = CODE_RE.search(user_text)
        if m:
            return tools.lookup_code({"code": m.group(1)})

        # Verified spec lookup (torque, lug torque, fluids) - works offline
        if any(w in t for w in ("torque", "lug", "ft-lb", "spec", "atf", "fluid type", "coolant type")):
            return tools.spec_lookup({"query": user_text})

        # Oil capacity
        if "oil" in t and ("quart" in t or "capacity" in t or "how much" in t or "type" in t):
            veh = (user_text.lower()
                   .replace("how many quarts of oil does a", "")
                   .replace("how much oil does a", "")
                   .replace("oil capacity for", "")
                   .replace("take", "").replace("?", "").strip(" .a"))
            return tools.oil_capacity({"vehicle": veh})

        # Wiring diagram
        if "wiring" in t or "diagram" in t:
            return tools.wiring_diagram({"vehicle": user_text, "system": "requested system"})

        if "time" in t or "date" in t:
            return tools.get_time()
        if "remember" in t:
            fact = user_text.split("remember", 1)[1].strip(" :,.")
            return memory.remember(fact or "(nothing specified)")
        if any(c.isdigit() for c in t) and any(op in t for op in "+-*/"):
            allowed = "0123456789+-*/(). "
            expr = "".join(c for c in user_text if c in allowed).strip()
            return tools.calculate({"expression": expr})

        return ("(mock brain - limited) I can do exact trouble-code lookups, oil capacity, and "
                "wiring-diagram sources offline right now. For full top-5 diagnostics and "
                "step-by-step repair help, add an ANTHROPIC_API_KEY to .env to switch on my full brain.")
