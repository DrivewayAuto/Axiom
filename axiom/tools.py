"""Axiom's actions - how it looks things up and does things.

Add a function + a SCHEMAS entry and Axiom can use it immediately.
"""
import datetime
import re
from pathlib import Path
from . import mechanic_data
from .code_reference import FULL_CODES
from .enriched_codes import ENRICHED_CODES

SPEC_FILE = Path(__file__).parent / "spec_reference.md"


def get_time(_args=None):
    return datetime.datetime.now().strftime("It is %A, %B %d %Y, %I:%M %p.")


def calculate(args):
    expr = args.get("expression", "")
    allowed = set("0123456789+-*/(). ")
    if not set(expr) <= allowed:
        return "I can only do basic arithmetic for safety."
    try:
        return f"{expr} = {eval(expr)}"
    except Exception as e:
        return f"Couldn't compute that: {e}"


def lookup_code(args):
    """OBD-II trouble code lookup: enriched diagnostics first, then the curated
    dictionary, then the full 3000+ code reference."""
    code = (args.get("code", "") or "").strip().upper()

    # 1) Enriched entry: causes, test steps, follow-ups, shop notes
    e = ENRICHED_CODES.get(code)
    if e:
        out = [f"{code}: {e['definition']}  [system: {e['system']} | severity: {e['severity']}]"]
        out.append("  Common causes:")
        out += [f"   - {c}" for c in e["common_causes"]]
        out.append("  Diagnostic steps:")
        out += [f"   {i}. {s}" for i, s in enumerate(e["diagnostic_steps"], 1)]
        if e.get("follow_up_questions"):
            out.append("  Ask the customer/tech:")
            out += [f"   - {q}" for q in e["follow_up_questions"]]
        if e.get("notes"):
            out.append(f"  Shop notes: {e['notes']}")
        return "\n".join(out)

    # 2) Curated dictionary (definition + causes)
    result = mechanic_data.lookup_obd(code)
    if result:
        return result

    # 3) Full reference (definition only, 3000+ codes)
    d = FULL_CODES.get(code)
    if d:
        note = ""
        if code.startswith("P1"):
            note = " (P1 codes are manufacturer-specific - confirm the make before interpreting.)"
        return f"{code}: {d}{note}"

    return (f"{code} isn't in my reference (3000+ codes). Double-check the code, "
            "or I can reason about it with my full brain if the API key is on.")


def oil_capacity(args):
    """Oil capacity / type for a vehicle from the starter table."""
    veh = args.get("vehicle", "")
    result = mechanic_data.lookup_oil(veh)
    if result:
        return result
    return (f"I don't have '{veh}' in my starter oil table. "
            "Add it to OIL_SPECS in mechanic_data.py, or my full brain can estimate it. "
            "Always confirm with the owner's manual.")


def spec_lookup(args):
    """Search the verified spec reference (torque specs, fluids) - checked FIRST
    before estimating. Entries carry confidence tags: [FSM] factory manual,
    [CORROB] multiple sources agree, [1-SRC] single source, [CONFIRM] verify first."""
    query = (args.get("query", "") or "").lower()
    if not SPEC_FILE.exists():
        return "Spec reference file missing (axiom/spec_reference.md)."
    text = SPEC_FILE.read_text(encoding="utf-8")
    sections = text.split("\n## ")
    words = [w for w in re.split(r"[^a-z0-9]+", query) if len(w) > 2]
    hits = []
    for s in sections[1:]:
        head = s.split("\n", 1)[0].lower()
        score = sum(1 for w in words if w in head) * 2 + sum(1 for w in words if w in s.lower())
        if score > 0:
            hits.append((score, "## " + s.strip()))
    if not hits:
        return (f"Nothing in the verified spec file for '{query}'. Don't guess a torque/fluid "
                "number from memory - verify against the FSM or a trusted source, and say so.")
    hits.sort(key=lambda x: -x[0])
    return "\n\n".join(h for _, h in hits[:2])


def vin_decode(args):
    """Free NHTSA VIN decode - year/make/model/engine. Needs internet, no key."""
    vin = (args.get("vin", "") or "").strip().upper()
    if len(vin) < 11:
        return "That VIN looks too short - a full VIN is 17 characters."
    try:
        import requests
        r = requests.get(
            f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json",
            timeout=10)
        d = r.json()["Results"][0]
        parts = []
        for label, key in [("Year","ModelYear"),("Make","Make"),("Model","Model"),
                           ("Trim","Trim"),("Engine","DisplacementL"),("Cylinders","EngineCylinders"),
                           ("Fuel","FuelTypePrimary"),("Drive","DriveType"),("Body","BodyClass"),
                           ("Plant","PlantCountry")]:
            v = (d.get(key) or "").strip()
            if v and v.lower() not in ("not applicable", ""):
                parts.append(f"{label}: {v}")
        if not parts:
            return f"NHTSA couldn't decode {vin} - double-check the VIN."
        return f"VIN {vin}:\n  " + "\n  ".join(parts)
    except Exception as e:
        return f"VIN lookup needs internet and it failed ({e}). Try again or decode manually at vpic.nhtsa.dot.gov."


def recall_check(args):
    """Free NHTSA recall lookup by year/make/model. Run before paid repairs."""
    year = str(args.get("year", "")).strip()
    make = (args.get("make", "") or "").strip()
    model = (args.get("model", "") or "").strip()
    if not (year and make and model):
        return "Need year, make, and model for a recall check."
    try:
        import requests
        r = requests.get("https://api.nhtsa.gov/recalls/recallsByVehicle",
                         params={"make": make, "model": model, "modelYear": year}, timeout=10)
        results = r.json().get("results", [])
        if not results:
            return f"No NHTSA recalls found for {year} {make} {model}. (Still worth a VIN-specific check at nhtsa.gov/recalls for completed-repair status.)"
        out = [f"{len(results)} NHTSA recall(s) for {year} {make} {model}:"]
        for rec in results[:8]:
            out.append(f"  - [{rec.get('NHTSACampaignNumber','?')}] {rec.get('Component','?')}: {(rec.get('Summary') or '')[:180]}")
        if len(results) > 8:
            out.append(f"  ...and {len(results)-8} more.")
        out.append("Check the specific VIN at nhtsa.gov/recalls to see if repairs were already done.")
        return "\n".join(out)
    except Exception as e:
        return f"Recall lookup needs internet and it failed ({e}). Check manually at nhtsa.gov/recalls."


def wiring_diagram(args):
    """Wiring diagrams are licensed/copyrighted - point to legitimate sources."""
    veh = args.get("vehicle", "the vehicle")
    system = args.get("system", "the system")
    return (
        f"I can't reproduce copyrighted wiring diagrams for {veh} ({system}), but here's where to get them:\n"
        "  - ALLDATA DIY (alldatadiy.com) - OEM diagrams, subscription\n"
        "  - Mitchell 1 DIY (eautorepair.net) - OEM diagrams, subscription\n"
        "  - Identifix / ProDemand - shop-grade\n"
        "  - Factory service manual (FSM) for the specific year/make/model\n"
        "  - Free: manufacturer TSBs, some forums, Haynes/Chilton for basics\n"
        "Tell me the circuit (e.g. 'headlight', 'fuel pump relay') and I'll explain how it's wired and how to trace it."
    )


REGISTRY = {
    "get_time": get_time,
    "calculate": calculate,
    "lookup_code": lookup_code,
    "oil_capacity": oil_capacity,
    "wiring_diagram": wiring_diagram,
    "spec_lookup": spec_lookup,
    "vin_decode": vin_decode,
    "recall_check": recall_check,
}

SCHEMAS = [
    {"name": "lookup_code",
     "description": "Get the exact definition and common causes of an OBD-II trouble code (e.g. P0420, P0301).",
     "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}},
    {"name": "oil_capacity",
     "description": "Look up engine oil capacity (quarts) and recommended oil type for a vehicle. Pass make/model/engine, e.g. 'Honda Civic 1.5T'.",
     "input_schema": {"type": "object", "properties": {"vehicle": {"type": "string"}}, "required": ["vehicle"]}},
    {"name": "spec_lookup",
     "description": "Search the verified spec reference for torque specs, lug torque, and fluid types/capacities. ALWAYS check here first before quoting any spec. Results carry confidence tags ([FSM]/[CORROB]/[1-SRC]/[CONFIRM]).",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "vin_decode",
     "description": "Decode a VIN via the free NHTSA database - exact year/make/model/engine/trim. Use whenever a VIN is given.",
     "input_schema": {"type": "object", "properties": {"vin": {"type": "string"}}, "required": ["vin"]}},
    {"name": "recall_check",
     "description": "Check NHTSA safety recalls for a year/make/model. ALWAYS run before recommending a paid repair.",
     "input_schema": {"type": "object", "properties": {"year": {"type": "string"}, "make": {"type": "string"}, "model": {"type": "string"}}, "required": ["year", "make", "model"]}},
    {"name": "wiring_diagram",
     "description": "Get guidance/sources for a vehicle wiring diagram for a given electrical system or circuit.",
     "input_schema": {"type": "object",
                      "properties": {"vehicle": {"type": "string"}, "system": {"type": "string"}},
                      "required": ["vehicle"]}},
    {"name": "get_time",
     "description": "Get the current date and time.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "calculate",
     "description": "Evaluate a basic arithmetic expression like '12 * (3 + 4)'.",
     "input_schema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
    {"name": "remember",
     "description": "Save a durable fact (e.g. the customer's vehicle, or a repair preference) for future conversations.",
     "input_schema": {"type": "object", "properties": {"fact": {"type": "string"}}, "required": ["fact"]}},
]


def run_tool(name, args, memory):
    if name == "remember":
        return memory.remember(args.get("fact", ""))
    fn = REGISTRY.get(name)
    if not fn:
        return f"(unknown tool: {name})"
    return fn(args)
