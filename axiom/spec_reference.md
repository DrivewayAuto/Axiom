# Vehicle Spec Reference — DIPSTICK Knowledge Base

Verified torque specs, lug torques, and fluid types for the platforms Bobby sees most. This is a **knowledge-base file** — upload it to the project alongside the OBD files. DIPSTICK is told to check here FIRST before searching the web, so anything in here comes back instantly.

**This is a seed, not a complete manual.** Add to it as you confirm specs on real jobs — same as you'd extend the OBD enrichment file. Keep the confidence tags honest.

## Confidence legend
- **[FSM]** — factory service manual / OEM figure. Trust it.
- **[CORROB]** — two or more independent sources agree. Solid for shop use.
- **[1-SRC]** — single source. Use it, but verify on anything safety-critical.
- **[CONFIRM]** — not pinned down; fetch live or check the FSM before relying on it.

Torque given in ft-lbs with in-lbs / N·m where useful. Always use a calibrated wrench on clean threads; re-torque lugs after a short drive.

---

## RAM 1500 — 1999 (2nd gen) — Brake hydraulics
*Source: Ram FSM figures posted on two Ram forums, agree. [CORROB]*
- Brake booster mounting nuts — **21 ft-lb** (28 N·m)
- Master cylinder mounting nuts — **160 in-lb** (~13 ft-lb, 18 N·m) — light, don't gorilla it
- Brake line fittings at master cylinder — **14 ft-lb** (170 in-lb, 19 N·m)
- Brake line fittings at junction block — **14 ft-lb** (170 in-lb)
- Front caliper brake line banjo bolt — **20 ft-lb** (27 N·m)
- Booster output pushrod clearance — **[CONFIRM]** no clean published number; preset/checked with a comparator gauge — pull from FSM, do not eyeball

## RAM 1500 — 4th gen (2009–2017) — Brakes
*Source: brake trade publication. [1-SRC], consistent with FSM-style values*
- Front caliper bracket, light-duty (1500) — **130 ft-lb**
- Rear caliper bracket, light-duty — **120 ft-lb**
- Caliper guide pins (front & rear) — **32 ft-lb**
- Lug nuts — **~130 ft-lb** [CONFIRM by year/wheel]
- HD (2500/3500) front caliper bracket — **275 ft-lb**; rear caliper bracket upper **163 ft-lb** / lower **190 ft-lb**

## RAM ProMaster — 2014–on (Fiat Ducato platform)
*Also sold as Fiat Ducato / Peugeot Boxer / Citroën Jumper*
- Lug nut torque — **145 ft-lb** per owner's manual [1-SRC]. Many techs run 100–120 by preference; spec is 145. Use pilot/guide pins to hang the wheel.
- Front caliper adapter/bracket bolt — **~125 ft-lb** (2015 1500 3.6) [1-SRC, CONFIRM by year]
- Caliper guide-pin bolts — **[CONFIRM]** not pinned; verify in service info
- *Expand: tighttorque.com has a fuller ProMaster table to confirm against*

## FORD F-150 — 2015–2020 (aluminum body) — Brakes & wheels
*Source: Ford owner's manual figure + multiple F-150 references. [CORROB] on lug; [1-SRC] on bracket*
- Lug nut torque — **150 ft-lb** (M14×1.5 studs); Ford specifies re-torque after ~100 miles
  - Older F-150s with **12 mm studs — 100 ft-lb**. Confirm which stud you have.
- Front caliper bracket bolts — **~184 ft-lb** (high; often one-time-use — replace) [CONFIRM exact by sub-model]
- Caliper guide/slide bolts — **~27 ft-lb**
- Front hub mounting bolts — **129 ft-lb**
- Outer tie rod nut — **85 ft-lb**; inner tie rod — **70 ft-lb**

## KIA — passenger cars & SUVs (KGIS factory source; VARIES by model)
*Source: KGIS/kiatechinfo figures posted across Kia forums. [CORROB] on the ranges below. Kia specs vary a lot by model/year — confirm in KGIS for the exact car.*
- Lug nut torque — **65–80 ft-lb** (use star pattern; many models land at ~80)
- Caliper guide-pin / slide bolts — **16–23 ft-lb** (consistent across models)
- Front caliper bracket bolts — model-specific: Forte **58–72 ft-lb**; older Sorento higher (**~129 ft-lb**) — **[CONFIRM by model]**
- Caliper-to-bracket bolts, Sorento 3.3 (BL) — **47–54 ft-lb**
- *Note: KGIS often lists a wide range; use the upper end.*

---

## FLUID TYPES — get the SPEC right; fetch CAPACITY per engine
Using the wrong ATF or coolant does real damage. Types below are stable and well-sourced; **exact fill capacity varies by engine/year — fetch that live per vehicle.** [CORROB]

- **Stellantis / Mopar (Ram, Chrysler, ProMaster gas) auto trans** — **ATF+4** (Chrysler MS-9602). Do NOT substitute generic Dexron/Mercon. ATF+4 was never superseded — still current. Back-compatible with ATF+, +2, +3.
- **Ford auto trans** — **Mercon** family: Mercon V (older) or Mercon LV (newer) — match the application, they're not interchangeable. Never Type F except pre-1977.
- **Kia / Hyundai auto trans** — **SP-III** or **SP-IV** (SP-IV is the modern spec). Some early-2000s Kias used Dexron II/III. Confirm by model — these have specific friction additives, don't run generic ATF.
- **Brake fluid** — **DOT 3** is typical for the older Mopar/this era; confirm against the reservoir cap marking (some applications spec DOT 4).
- **Coolant** — **[CONFIRM]** varies (Mopar OAT vs HOAT/G-05 by year; Ford and Kia have their own) — fetch per vehicle, wrong coolant gums up systems.

---

## FLUID CAPACITIES — common ones (confirm ENGINE; oil = with filter unless noted)
*Capacity is engine-specific and changes with filter (oil) and dry-fill-vs-service-refill (trans). [CORROB] unless tagged.*

**RAM 1500 — engine oil (with filter):**
- 3.6L Pentastar V6 — **~5.9–6.0 qt** (0W-20, MS-6395)
- 5.7L HEMI V8 — **7.0 qt** (5W-20; 0W-20 on 2022+; MS-6395)
- 3.0L EcoDiesel — Gen 2 (2014–19) **10.5 qt** (MS-10902) / Gen 3 (2020–23) **8.5 qt** (MS-12991) — **don't cross the oil spec between gens**

**RAM 1500 — 8-speed ZF auto (8HP70/8HP75, 2013–on):**
- Total / dry fill — **~8.7–8.8 qt**
- Pan-drop service refill — **~5–6 qt** (rest stays in the torque converter)
- Drain-and-fill — **~4.7 qt**
- Fluid — **Mopar ZF 8&9 Speed ATF / ZF Lifeguard 8** — NOT ATF+4. Pan and filter are one piece; fill/check with trans warm and running.

## HOW TO EXPAND THIS FILE
When you confirm a spec on a real job, add it under the right make/model with a confidence tag and a one-word source ("FSM," "AllData," "KGIS"). Highest-value additions to chase next: engine specs (head bolt sequence/torque-to-yield, spark plug, oil drain plug), more suspension (ball joints, control arms, axle nuts) by generation, and ProMaster/Stellantis EPB-related specs. Keep generation labels exact — torque specs change across model years.
