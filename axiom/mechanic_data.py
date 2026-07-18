"""Offline mechanic knowledge that must be EXACT and instant.

- OBD_CODES: large OBD-II diagnostic trouble code dictionary (definition + causes).
- OIL_SPECS: starter oil capacity / oil type table for common vehicles.

Bundled so Axiom gives correct code definitions with no internet and no API key.
The list below covers the common generic (SAE) powertrain, chassis, body and
network codes, plus whole code families generated programmatically (misfires,
injectors, O2 sensors, etc.). Expand freely. For full per-VIN factory specs the
LLM brain or a paid data provider fills the gaps. ALWAYS verify against the
owner's manual / factory service info.
"""

# Generic fallback causes used when a code family doesn't have specifics.
_GEN = ["Faulty sensor/component", "Wiring open/short or bad connector", "Related mechanical or control fault"]

# ---- Explicitly authored, high-value codes (definition + common causes) ----
_BASE = {
    # Fuel & Air Metering / Mixture
    "P0100": ("Mass or Volume Air Flow Circuit Malfunction", ["Dirty/faulty MAF sensor", "Air intake leak", "Wiring/connector issue"]),
    "P0101": ("Mass Air Flow Circuit Range/Performance", ["Dirty MAF sensor", "Vacuum/intake leak", "Dirty air filter"]),
    "P0102": ("Mass Air Flow Circuit Low Input", ["Faulty MAF", "Open/short in MAF wiring", "Connector corrosion"]),
    "P0103": ("Mass Air Flow Circuit High Input", ["Faulty MAF", "Short in wiring", "Connector fault"]),
    "P0106": ("MAP/Barometric Pressure Circuit Range/Performance", ["Faulty MAP sensor", "Vacuum leak", "Clogged MAP port"]),
    "P0107": ("MAP/Barometric Pressure Circuit Low Input", ["Faulty MAP sensor", "Open/short wiring", "Vacuum line off"]),
    "P0108": ("MAP/Barometric Pressure Circuit High Input", ["Faulty MAP sensor", "Short to voltage", "Connector fault"]),
    "P0110": ("Intake Air Temp Sensor Circuit Malfunction", ["Faulty IAT sensor", "Wiring", "Connector"]),
    "P0111": ("Intake Air Temp Sensor Range/Performance", ["Faulty IAT sensor", "Air leak", "Aging sensor"]),
    "P0112": ("Intake Air Temp Sensor Circuit Low Input", ["Faulty IAT sensor", "Short to ground", "Connector"]),
    "P0113": ("Intake Air Temp Sensor Circuit High Input", ["Faulty IAT sensor", "Wiring open", "Poor connection"]),
    "P0115": ("Engine Coolant Temp Sensor Circuit Malfunction", ["Faulty ECT sensor", "Wiring", "Connector"]),
    "P0116": ("Engine Coolant Temp Sensor Range/Performance", ["Faulty ECT sensor", "Low coolant", "Stuck thermostat"]),
    "P0117": ("Engine Coolant Temp Sensor Circuit Low Input", ["Faulty ECT sensor", "Short to ground", "Connector"]),
    "P0118": ("Engine Coolant Temp Sensor Circuit High Input", ["Faulty ECT sensor", "Open wiring", "Bad connector"]),
    "P0120": ("Throttle/Pedal Position Sensor A Circuit Malfunction", ["Faulty TPS", "Wiring issue", "Failing throttle body"]),
    "P0121": ("Throttle/Pedal Position Sensor A Range/Performance", ["Faulty TPS", "Dirty throttle body", "Wiring"]),
    "P0122": ("Throttle/Pedal Position Sensor A Circuit Low Input", ["Faulty TPS", "Short to ground", "Connector"]),
    "P0123": ("Throttle/Pedal Position Sensor A Circuit High Input", ["Faulty TPS", "Short to voltage", "Connector"]),
    "P0125": ("Insufficient Coolant Temp for Closed Loop Fuel", ["Stuck-open thermostat", "Faulty ECT sensor", "Low coolant"]),
    "P0128": ("Coolant Thermostat Below Regulating Temperature", ["Stuck-open thermostat", "Faulty ECT sensor", "Low coolant"]),
    "P0171": ("System Too Lean (Bank 1)", ["Vacuum/intake leak", "Dirty MAF", "Weak fuel pump", "Clogged injectors"]),
    "P0172": ("System Too Rich (Bank 1)", ["Leaking injector", "High fuel pressure", "Faulty MAF/O2", "Dirty air filter"]),
    "P0174": ("System Too Lean (Bank 2)", ["Vacuum leak", "Dirty MAF", "Weak fuel delivery"]),
    "P0175": ("System Too Rich (Bank 2)", ["Leaking injector", "High fuel pressure", "Faulty O2 sensor"]),
    # Idle / EGR / Emissions
    "P0400": ("Exhaust Gas Recirculation Flow Malfunction", ["Clogged EGR passages", "Faulty EGR valve", "Vacuum supply"]),
    "P0401": ("EGR Flow Insufficient Detected", ["Clogged EGR passages", "Faulty EGR valve", "Vacuum supply"]),
    "P0402": ("EGR Flow Excessive Detected", ["Stuck-open EGR valve", "Carbon buildup", "EGR control fault"]),
    "P0411": ("Secondary Air Injection Incorrect Flow", ["Faulty air pump", "Clogged passages", "Check valve"]),
    "P0420": ("Catalyst System Efficiency Below Threshold (Bank 1)", ["Failing catalytic converter", "Faulty O2 sensors", "Exhaust leak"]),
    "P0430": ("Catalyst System Efficiency Below Threshold (Bank 2)", ["Failing catalytic converter", "Faulty O2 sensors", "Exhaust leak"]),
    "P0440": ("EVAP System Malfunction", ["Loose/faulty gas cap", "EVAP leak", "Faulty purge valve"]),
    "P0441": ("EVAP Incorrect Purge Flow", ["Faulty purge valve", "Blocked/cracked hose", "Vent valve"]),
    "P0442": ("EVAP System Small Leak Detected", ["Loose gas cap", "Cracked EVAP hose", "Faulty vent/purge valve"]),
    "P0443": ("EVAP Purge Control Valve Circuit", ["Faulty purge solenoid", "Wiring", "Connector"]),
    "P0446": ("EVAP Vent Control Circuit Malfunction", ["Faulty vent valve", "Blocked vent", "Wiring"]),
    "P0455": ("EVAP System Large Leak Detected", ["Missing/loose gas cap", "Large EVAP hose leak", "Faulty purge valve"]),
    "P0456": ("EVAP System Very Small Leak Detected", ["Gas cap seal", "Tiny EVAP leak", "Vent/purge valve"]),
    # Speed / Idle / Aux
    "P0500": ("Vehicle Speed Sensor Malfunction", ["Faulty VSS", "Wiring", "Bad ABS sensor (some vehicles)"]),
    "P0505": ("Idle Air Control System Malfunction", ["Dirty/faulty IAC valve", "Vacuum leak", "Dirty throttle body"]),
    "P0506": ("Idle Control System RPM Lower Than Expected", ["Carbon-clogged throttle body", "Vacuum leak", "IAC fault"]),
    "P0507": ("Idle Control System RPM Higher Than Expected", ["Vacuum leak", "Dirty throttle body", "Faulty IAC/PCV"]),
    # Charging / System voltage
    "P0560": ("System Voltage Malfunction", ["Weak battery", "Charging fault", "Corroded grounds"]),
    "P0562": ("System Voltage Low", ["Failing alternator", "Weak battery", "Corroded grounds/cables"]),
    "P0563": ("System Voltage High", ["Faulty voltage regulator", "Alternator overcharge", "Wiring"]),
    # Ignition / timing
    "P0325": ("Knock Sensor 1 Circuit (Bank 1)", ["Faulty knock sensor", "Wiring", "Actual engine knock"]),
    "P0330": ("Knock Sensor 2 Circuit (Bank 2)", ["Faulty knock sensor", "Wiring", "Actual engine knock"]),
    "P0335": ("Crankshaft Position Sensor A Circuit Malfunction", ["Faulty CKP sensor", "Damaged reluctor ring", "Wiring"]),
    "P0336": ("Crankshaft Position Sensor A Range/Performance", ["Damaged tone ring", "Faulty CKP sensor", "Wiring"]),
    "P0340": ("Camshaft Position Sensor A Circuit (Bank 1)", ["Faulty CMP sensor", "Wiring", "Timing issue"]),
    "P0341": ("Camshaft Position Sensor A Range/Performance (Bank 1)", ["Timing chain stretch", "Faulty CMP", "Reluctor"]),
    "P0420A": ("", []),  # placeholder removed below
    # Transmission
    "P0700": ("Transmission Control System Malfunction", ["TCM fault (companion code present)", "Wiring", "Internal trans issue"]),
    "P0705": ("Transmission Range Sensor Circuit (PRNDL Input)", ["Faulty range/neutral switch", "Misadjustment", "Wiring"]),
    "P0706": ("Transmission Range Sensor Range/Performance", ["Faulty range switch", "Linkage", "Wiring"]),
    "P0711": ("Transmission Fluid Temp Sensor Range/Performance", ["Faulty TFT sensor", "Low/old fluid", "Wiring"]),
    "P0715": ("Input/Turbine Speed Sensor Circuit Malfunction", ["Faulty input speed sensor", "Wiring", "Low fluid"]),
    "P0720": ("Output Speed Sensor Circuit Malfunction", ["Faulty output speed sensor", "Wiring", "Internal damage"]),
    "P0730": ("Incorrect Gear Ratio", ["Low/old trans fluid", "Worn clutches", "Solenoid fault"]),
    "P0740": ("Torque Converter Clutch Circuit Malfunction", ["Faulty TCC solenoid", "Low fluid", "Wiring/valve body"]),
    "P0741": ("Torque Converter Clutch Performance/Stuck Off", ["Faulty TCC solenoid", "Valve body", "Low fluid"]),
    "P0750": ("Shift Solenoid A Malfunction", ["Faulty shift solenoid", "Low fluid", "Valve body/wiring"]),
    "P0755": ("Shift Solenoid B Malfunction", ["Faulty shift solenoid", "Low fluid", "Valve body/wiring"]),
    # Common P2xxx
    "P2096": ("Post Catalyst Fuel Trim System Too Lean (Bank 1)", ["Exhaust leak", "Faulty downstream O2", "Lean condition"]),
    "P2097": ("Post Catalyst Fuel Trim System Too Rich (Bank 1)", ["Faulty O2 sensor", "Rich condition", "Exhaust"]),
    "P2098": ("Post Catalyst Fuel Trim System Too Lean (Bank 2)", ["Exhaust leak", "Faulty downstream O2", "Lean"]),
    "P2101": ("Throttle Actuator Control Motor Circuit Range/Performance", ["Faulty throttle body", "Wiring", "TAC fault"]),
    "P2119": ("Throttle Actuator Control Throttle Body Range/Performance", ["Dirty/faulty throttle body", "Wiring", "Carbon"]),
    "P2135": ("TPS/Pedal Position Sensor A/B Voltage Correlation", ["Faulty TPS", "Connector", "Throttle body"]),
    "P2187": ("System Too Lean at Idle (Bank 1)", ["Vacuum leak", "Dirty MAF", "Weak fuel delivery"]),
    "P2195": ("O2 Sensor Signal Stuck Lean (Bank 1 Sensor 1)", ["Faulty O2 sensor", "Lean condition", "Exhaust leak"]),
    "P2503": ("Charging System Voltage Low", ["Failing alternator", "Wiring", "Battery"]),
    # Diesel-common
    "P0087": ("Fuel Rail/System Pressure Too Low", ["Weak fuel pump", "Clogged filter", "Leaking regulator/injector"]),
    "P0088": ("Fuel Rail/System Pressure Too High", ["Faulty pressure regulator", "Restricted return", "Sensor fault"]),
    "P0299": ("Turbocharger/Supercharger Underboost", ["Boost leak", "Faulty wastegate/actuator", "Clogged intake"]),
    "P2002": ("Diesel Particulate Filter Efficiency Below Threshold (Bank 1)", ["Clogged DPF", "Failed regen", "Pressure sensor"]),
    "P20EE": ("SCR NOx Catalyst Efficiency Below Threshold (Bank 1)", ["DEF quality", "Aged SCR catalyst", "NOx sensor"]),
    # Network / communication
    "U0100": ("Lost Communication With ECM/PCM A", ["CAN bus wiring fault", "Failed module", "Power/ground issue"]),
    "U0101": ("Lost Communication With TCM", ["CAN wiring", "TCM power/ground", "Failed module"]),
    "U0121": ("Lost Communication With ABS Control Module", ["CAN wiring", "ABS module power/ground", "Failed module"]),
    "U0140": ("Lost Communication With Body Control Module", ["CAN wiring", "BCM power/ground", "Failed module"]),
    "U0155": ("Lost Communication With Instrument Cluster", ["CAN wiring", "Cluster power/ground", "Failed cluster"]),
    # Chassis / ABS
    "C0035": ("Left Front Wheel Speed Sensor Circuit", ["Faulty wheel speed sensor", "Damaged tone ring", "Wiring"]),
    "C0040": ("Right Front Wheel Speed Sensor Circuit", ["Faulty wheel speed sensor", "Damaged tone ring", "Wiring"]),
    "C0045": ("Left Rear Wheel Speed Sensor Circuit", ["Faulty wheel speed sensor", "Damaged tone ring", "Wiring"]),
    "C0050": ("Right Rear Wheel Speed Sensor Circuit", ["Faulty wheel speed sensor", "Damaged tone ring", "Wiring"]),
    # Body / SRS
    "B0001": ("Driver Frontal Stage 1 Deployment Control", ["Airbag circuit fault", "Clockspring", "Connector under seat"]),
    "B0004": ("Passenger Frontal Stage 1 Deployment Control", ["Airbag circuit fault", "Connector", "Module"]),
}
# remove the placeholder
_BASE.pop("P0420A", None)


def _build():
    codes = {}
    for k, (name, causes) in _BASE.items():
        codes[k] = {"name": name, "causes": causes}

    def add(code, name, causes=None):
        codes.setdefault(code, {"name": name, "causes": causes or _GEN})

    # Misfire family P0301-P0312
    for i in range(1, 13):
        add(f"P03{i:02d}", f"Cylinder {i} Misfire Detected",
            [f"Bad coil/spark plug cyl {i}", f"Injector fault cyl {i}", f"Low compression cyl {i}", "Vacuum leak"])
    # Injector circuit family P0201-P0212
    for i in range(1, 13):
        add(f"P02{i:02d}", f"Injector Circuit/Open - Cylinder {i}",
            [f"Faulty injector cyl {i}", "Wiring open/short", "Connector/driver fault"])
    # Glow plug family P0671-P0678 (diesel, cyl 1-8)
    for i in range(1, 9):
        add(f"P06{70+i:d}", f"Glow Plug/Heater Circuit - Cylinder {i}",
            [f"Faulty glow plug cyl {i}", "Glow plug relay/module", "Wiring"])
    # O2 sensor families - banks 1/2, sensors 1/2, common sub-faults
    o2sub = {
        "0": "Circuit Malfunction", "1": "Low Voltage", "2": "High Voltage",
        "3": "Slow Response", "4": "No Activity Detected", "5": "Heater Circuit Malfunction",
    }
    # Bank 1 Sensor 1 -> P013x ; B1S2 -> P013x(7-9)/P014x ; B2S1 -> P015x ; B2S2 -> P015x/6
    o2_map = {
        ("1", "1"): 130, ("1", "2"): 136, ("2", "1"): 150, ("2", "2"): 156,
    }
    for (bank, sensor), base in o2_map.items():
        for sub, desc in o2sub.items():
            code = "P%04d" % (base + int(sub))
            add(code, f"O2 Sensor {desc} (Bank {bank} Sensor {sensor})",
                ["Faulty O2 sensor", "Exhaust leak", "Wiring/heater fuse", "Fuel mixture fault"])
    # MAF/temp low-high already covered; add a few more generic ranges
    add("P0order", "")  # guard, removed next
    codes.pop("P0order", None)
    return codes


OBD_CODES = _build()


# ---- Oil capacity table (US quarts WITH filter). VERIFY with owner's manual. ----
OIL_SPECS = {
    "honda civic 1.5t":   {"capacity_qts": 3.7,  "oil_type": "0W-20 synthetic"},
    "honda civic 2.0":    {"capacity_qts": 4.4,  "oil_type": "0W-20 synthetic"},
    "honda accord 1.5t":  {"capacity_qts": 3.7,  "oil_type": "0W-20 synthetic"},
    "toyota camry 2.5":   {"capacity_qts": 4.8,  "oil_type": "0W-20 synthetic"},
    "toyota corolla 1.8": {"capacity_qts": 4.4,  "oil_type": "0W-20 synthetic"},
    "toyota tacoma 3.5":  {"capacity_qts": 6.2,  "oil_type": "0W-20 synthetic"},
    "ford f-150 5.0":     {"capacity_qts": 8.8,  "oil_type": "5W-20 synthetic blend"},
    "ford f-150 3.5 ecoboost": {"capacity_qts": 6.0, "oil_type": "5W-30 synthetic"},
    "chevrolet silverado 5.3": {"capacity_qts": 8.0, "oil_type": "0W-20 dexos1"},
    "chevrolet equinox 1.5t":  {"capacity_qts": 4.5, "oil_type": "0W-20 dexos1"},
    "jeep wrangler 3.6":  {"capacity_qts": 6.0,  "oil_type": "0W-20 synthetic"},
    "nissan altima 2.5":  {"capacity_qts": 4.9,  "oil_type": "0W-20 synthetic"},
    "subaru outback 2.5": {"capacity_qts": 5.1,  "oil_type": "0W-20 synthetic"},
    "ram 1500 5.7 hemi":  {"capacity_qts": 7.0,  "oil_type": "5W-20 synthetic"},
}


def lookup_obd(code: str):
    code = (code or "").strip().upper()
    info = OBD_CODES.get(code)
    if not info:
        return None
    causes = "\n".join(f"   - {c}" for c in info["causes"])
    return f"{code}: {info['name']}\n  Common causes:\n{causes}"


def lookup_oil(vehicle: str):
    key = (vehicle or "").strip().lower()
    if key in OIL_SPECS:
        s = OIL_SPECS[key]
        return f"{vehicle.title()}: ~{s['capacity_qts']} qts ({s['oil_type']}) with filter. Verify with owner's manual."
    for k, s in OIL_SPECS.items():
        if k in key or key in k:
            return f"{k.title()}: ~{s['capacity_qts']} qts ({s['oil_type']}) with filter. Verify with owner's manual."
    return None
