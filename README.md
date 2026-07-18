# Project Axiom - Master Mechanic Edition

A chatbot built to be a master automotive mechanic. Ask it about a vehicle problem
and it gives the top 5 most-likely fixes (ranked), then a step-by-step diagnostic
for the #1 suspect. It also looks up trouble codes, oil capacities, and where to
get wiring diagrams.

## What it does

| Ask it... | What happens | Powered by |
|---|---|---|
| "My car shakes at idle, CEL on" | Top 5 ranked causes (parts, labor, difficulty) + step-by-step diagnosis | LLM brain (`brain.py`, persona in `config.py`) |
| "What does P0420 mean?" | Exact code definition + common causes, instantly, even offline | Offline OBD-II dictionary (`mechanic_data.py`) |
| "How many quarts of oil does a Honda Civic 1.5T take?" | Capacity + oil type (verify w/ manual) | Oil table (`mechanic_data.py`) + brain |
| "Wiring diagram for a Camry headlights" | Where to legally get OEM diagrams + how the circuit works | `tools.py` (diagrams are copyrighted - not reproduced) |

## The two brains

- **Full brain (recommended):** add an `ANTHROPIC_API_KEY` and Axiom uses Claude's
  deep mechanic knowledge for the ranked top-5 diagnostics, step-by-step procedures,
  and any code/spec it doesn't have bundled. It calls the lookup tools automatically.
- **Offline mock:** with no key, it still nails the *exact* lookups (trouble codes,
  oil capacity, wiring sources) from the bundled data. The open-ended diagnostics
  need the full brain.

## Run it

```bash
cd axiom
python chat.py
```

Runs immediately in offline mode. To switch on the full master-mechanic brain:

```bash
cp .env.example .env        # paste your ANTHROPIC_API_KEY (console.anthropic.com)
pip install -r requirements.txt
export $(cat .env | xargs)  # load the key
python chat.py
```

Try: "What's P0301?" / "oil capacity for ford f-150 5.0" /
"2018 Silverado 5.3 cranks but won't start" / "remember the customer's truck is a 2016 Ram 1500 5.7"

## How to make it a TRUE master mechanic (grow it)

1. **More codes & specs (biggest win, easy):** expand `OBD_CODES` and `OIL_SPECS` in
   `axiom/mechanic_data.py`. Every entry you add becomes instant + exact, no key needed.
2. **Exact factory data:** wiring diagrams and per-VIN specs are licensed. To get them
   inside Axiom, subscribe to a data provider (ALLDATA, Mitchell 1, etc.) and add a
   tool in `tools.py` that calls their API/your data. (Don't scrape paywalled diagrams.)
3. **Live web lookup:** add a `web_search` tool in `tools.py` so it can pull current
   TSBs, recalls, and torque specs at runtime.
4. **Memory of the bay:** it already remembers facts (`memory.py`). Use it to store each
   customer's vehicle, history, and prior repairs so it gets smarter the more you use it.
5. **VIN decode:** add a tool that decodes a VIN to year/make/model/engine so you don't
   have to type it each time (NHTSA has a free VIN API).

## Files

```
chat.py                  - run this to talk to Axiom
axiom/agent.py        - ties brain + memory + tools together
axiom/brain.py        - LLM connection + offline mock + tool loop
axiom/tools.py        - actions: lookup_code, oil_capacity, wiring_diagram, remember...
axiom/mechanic_data.py- offline OBD-II code dictionary + oil specs (EXPAND THIS)
axiom/memory.py       - remembers facts + full transcript across sessions
axiom/config.py       - master-mechanic persona + settings
```

> Safety: always verify capacities and torque specs against the factory service
> information for the exact year/make/model/engine before doing the work.
