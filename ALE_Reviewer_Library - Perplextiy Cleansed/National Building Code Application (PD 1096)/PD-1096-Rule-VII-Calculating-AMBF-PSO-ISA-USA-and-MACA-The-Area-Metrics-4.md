# Architecture Licensure Examination (ALE) Review: The Area Metrics — AMBF, PSO, ISA, USA, and MACA

**Module Focus:** PD 1096, 2004 Revised IRR — Rule VIII (Sec. 803), Table VIII.1  
**ALE Area:** 3 (Architectural Design and Site Planning)  
**Difficulty:** Intermediate  
**Spaced Repetition:** Return in 3 days. If you can answer the Blitz Quiz cold, move on.

---

## The Scenario — See It Before You Read It

You are standing on a vacant 500 sq.m lot in Quezon City, zoned Basic R-2. Your client hands you a sketch: "I want the biggest building possible, and pave everything else for the cars."

Before you open a single table, you already know three things:

1. The building cannot cover more than **55%** of the lot (no firewall) or **60%** (with firewall).
2. At least **15%** (no firewall) or **10%** (with firewall) must remain as exposed soil and planting — permanently, by law.
3. The total hard surface — building plus paving — cannot exceed **85%** (no firewall) or **90%** (with firewall).

How do you know this instantly? Because you have internalized Table VIII.1. This module teaches you to do exactly that.

---

## PATTERN INTERRUPT — The One Diagram That Explains Everything

Every square meter of the lot belongs to exactly one of three categories. Before reading further, draw this:

```
+--------------------------------------------------+
|                 TLA = 100%                        |
|                                                   |
|  +------------+  +---------------+  +-----------+ |
|  |    PSO     |  |      ISA      |  |    USA    | |
|  |  Building  |  |   Hardscape   |  | Softscape | |
|  |  Footprint |  | (paved open)  |  |(soil/lawn)| |
|  +------------+  +---------------+  +-----------+ |
|                                                   |
|  [--- MACA (PSO + ISA) ------]                    |
|                 [--- TOSL (ISA + USA) ----------] |
+--------------------------------------------------+
```

**Immediate action:** Draw this diagram on paper right now — do not proceed until you have done it. Label PSO (the building), ISA (the paved area outside the building), and USA (the planted / unpaved area). Color them differently if you have pens. This spatial image is your anchor for everything that follows.

---

## The Six Terms — Defined Once, Defined Right

All definitions are drawn from **Section 803 of Rule VIII, 2004 Revised IRR of PD 1096**.

| # | Term | Full Name | What It Is | Unit |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **TLA** | Total Lot Area | The entire area of the lot within property lines | sq.m |
| 2 | **PSO** | Percentage of Site Occupancy | The maximum percentage of the lot that may be covered by an enclosed building at ground floor level. Defined as AMBF / TLA. | % |
| 3 | **AMBF** | Allowable Maximum Building Footprint | The actual buildable area (in sq.m) at ground level — "the true buildable area on which a fully enclosed building or structure can be erected." | sq.m |
| 4 | **ISA** | Impervious Surface Area | The maximum allowable paved, tiled, or hardscaped open surface at ground level, expressed as a percentage of TLA | % |
| 5 | **USA** | Unpaved Surface Area | The minimum required portion of the lot with exposed soil and planting (softscape). Per the IRR: "this is the true open space." | % |
| 6 | **TOSL** | Total Open Space within Lot | All area not occupied by the building: courts, yards, gardens, light wells, uncovered driveways, access roads, and parking spaces. TOSL = ISA + USA. | % |
| 7 | **MACA** | Maximum Allowable Construction Area | Combined total of PSO + ISA — everything "hard" on the lot, including both the building footprint and all paved areas outside it | % |

---

## The Four Governing Equations — Skeleton Keys

Memorize these before the table data. They let you reconstruct any missing value from the others.

| Equation | In Words | Why It Matters |
| :--- | :--- | :--- |
| **PSO + TOSL = 100%** | Building footprint + open space = the entire lot | If one goes up, the other must go down — they are linked |
| **TOSL = ISA + USA** | Open space = hardscape + softscape | TOSL is not just "yard" — it includes paved driveways and parking outside the building |
| **MACA = PSO + ISA** | All hard surfaces = building + paving | The umbrella cap on everything impervious |
| **TLA = MACA + USA** (as percentages) | Hard total + soft total = 100% | Your arithmetic self-check — if numbers do not add to 100%, find the error |

**And the key conversion formula:**

```
AMBF (sq.m) = TLA (sq.m) x PSO (%)
```

**Chant this three times aloud:** _"PSO plus TOSL is the lot. TOSL is ISA plus USA. MACA is PSO plus ISA."_

---

## Reason for the Law — Why Every Rule Exists

Understanding legislative intent makes the numbers permanent. When you know _why_ the government mandated a control, you will never confuse its direction or forget its threshold.

| Rule | Why the Government Mandates It |
| :--- | :--- |
| **PSO cap** | Prevents wall-to-wall buildings that block light and natural ventilation to adjacent properties. This is a public health protection in dense urban areas — natural cross-ventilation reduces disease transmission and reliance on mechanical systems. |
| **USA minimum** | Mandates surface water percolation into the ground, aquifer recharge, heat absorption, and soil ventilation. Without minimum unpaved area, stormwater runoff overwhelms drainage systems, urban heat island effects intensify, and flood events worsen. |
| **ISA cap** | Limits total impervious surface beyond the building itself. Paved driveways and plazas generate stormwater runoff almost as aggressively as building rooftops — capping ISA controls cumulative runoff at the lot level. |
| **TOSL minimum** | Guarantees a minimum quantum of open sky above the lot for light, cross-ventilation, and emergency access from the sides and rear. Buildings with zero TOSL are inaccessible to fire suppression from the perimeter. |
| **MACA cap** | The umbrella control: even if PSO and ISA are individually within limits, MACA prevents gaming the system by maximizing both simultaneously. It sets a ceiling on all impervious coverage combined. |
| **Firewall allowance (higher PSO)** | When a building uses a firewall on a shared property line, adjacent lot ventilation is not compromised in the same way, and the party wall provides fire separation — both justify allowing a slightly larger building footprint. |

**Emotional anchor:** Every square meter of USA you protect is a square meter where rainwater soaks into the ground instead of surging into a street and flooding a family's ground floor. The USA minimum is not an abstract architectural requirement — it is a direct flood mitigation tool for downstream communities.

---

## PATTERN INTERRUPT — The Critical Correction Most Candidates Get Wrong

### Table VIII.1 Does NOT Distinguish "Inside Lot" vs. "Corner Lot"

This is one of the most common exam misconceptions. Do not carry it into the examination room.

**What Table VIII.1 actually distinguishes:** Firewall status — (e) = without firewall, (f) = with firewall.

**Where the inside-lot vs. corner-lot distinction actually appears:**
- **Table VII.1** — Maximum PSO by occupancy and lot type (inside lot, corner lot, through lot)
- **Table VIII.G.6** — TOSL requirements by lot type

**The correct procedure when given a corner lot:** Check Table VIII.1 for the firewall-based PSO. Check Table VII.1 for the lot-type-based PSO. Check Table VIII.G.6 for the lot-type-based TOSL. Then apply the **most restrictive** value of each metric — per Rule VII, Sec. 704.4.a.

---

## The Hard Data: Table VIII.1 (Verified Values)

**Source:** Table VIII.1 — Reference Table of Maximum Allowable PSO, Maximum Allowable ISA, the MACA, the Minimum USA and the TOSL by Type of Land Use Zoning per Lot — 2004 Revised IRR of PD 1096 (Official Text, 2005 Revised Edition, pp. 114–120), Rule VIII, Sec. 803.4.

### Residential Zones

| Zoning Classification | Firewall | Max PSO | Max ISA | Min USA | Min TOSL | MACA |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Basic R-2** (BHL 10.00 m) | Without (e) | **55%** | 30% | 15% | 45% | 85% |
| **Basic R-2** (BHL 10.00 m) | With (f) | **60%** | 30% | 10% | 40% | 90% |
| **Max R-2** (BHL 15.00 m) | Without (e) | 60% | 30% | 10% | 40% | 90% |
| **Max R-2** (BHL 15.00 m) | With (f) | **70%** | 20% | 10% | 30% | 90% |
| **Basic R-3** (BHL 10.00 m) | Without (e) | **65%** | 20% | 15% | 35% | 85% |
| **Basic R-3** (BHL 10.00 m) | With (f) | **70%** | 20% | 10% | 30% | 90% |
| **Max R-3** (BHL 36.00 m) | Without (e) | 70% | 20% | 10% | 30% | 90% |
| **Max R-3** (BHL 36.00 m) | With (f) | **80%** | 10% | 10% | 20% | 90% |

### Commercial, Industrial, and Institutional Zones

| Zoning Classification | Firewall | Max PSO | Max ISA | Min USA | Min TOSL | MACA |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Com-1** | Without (e) | 70% | 20% | 10% | 30% | 90% |
| **Com-1** | With (f) | 80% | 10% | 10% | 20% | 90% |
| **Com-2** | Without (e) | **75%** | 20% | 5% | 25% | 95% |
| **Com-2** | With (f) | 85% | 10% | 5% | 15% | 95% |
| **Com-3** | Without (e) | 80% | 15% | 5% | 20% | 95% |
| **Com-3** | With (f) | **90%** | 5% | 5% | 10% | 95% |
| **Ind-1** | Without (e) | 70% | 20% | 10% | 30% | 90% |
| **Ind-1** | With (f) | 80% | 10% | 10% | 20% | 90% |
| **Institutional** | Without (e) | **50%** | 20% | **30%** | 50% | 70% |
| **Institutional** | With (f) | 60% | 20% | 20% | 40% | 80% |

### Arithmetic Verification (Built-in Self-Checks)

For every row: PSO + ISA = MACA, and ISA + USA = TOSL, and PSO + TOSL = 100%.

Spot-check: Basic R-2, no firewall: 55 + 30 = 85 (MACA); 30 + 15 = 45 (TOSL); 55 + 45 = 100. Confirmed.

---

## Pattern Recognition — Lock the Table in Memory

Stop trying to memorize every cell. Recognize the structural patterns instead:

- **PSO + TOSL always = 100%.** Knowing one gives you the other.
- **PSO + ISA = MACA always.** No exception.
- **ISA + USA = TOSL always.** No exception.
- **Adding a firewall increases PSO** (you can build bigger against the shared wall) but **decreases or maintains USA** (you must still provide minimum greenery).
- **Institutional has the lowest PSO (50%)** and the **highest USA (30%)** — hospitals and schools require the most open space for evacuation, play areas, and access.
- **Com-3 with firewall has the highest PSO (90%)** — CBD lots can be built almost wall-to-wall. Only 5% of the lot must remain unpaved.
- **MACA is always 85% or 90% for residential** and **90% or 95% for commercial/industrial** — these are the only two MACA values for these categories.

**Immediate action:** Cover the table above. From memory, write the Basic R-2 (without firewall) row: PSO ___, ISA ___, USA ___, TOSL ___, MACA ___. Check your answer: 55 — 30 — 15 — 45 — 85. Repeat until you produce these numbers without looking.

---

## High-Yield Exam Traps

These are errors that cost passing candidates their license. Read each one aloud.

---

### TRAP 1 — "Table VIII.1 distinguishes inside lot vs. corner lot"

**The mistake:** Assuming that Table VIII.1 gives different PSO values based on whether the lot is an inside lot or a corner lot.

**The truth:** Table VIII.1 distinguishes by **firewall status** (with or without), not by lot position. Lot-type distinctions are in **Table VII.1** (PSO by occupancy and lot type) and **Table VIII.G.6** (TOSL by lot type).

**Procedure:** When the exam gives you a corner lot, check all three tables and apply the most restrictive value of each metric.

---

### TRAP 2 — "TOSL = Front Setback Only"

**The mistake:** Treating TOSL as if it refers only to the front yard or a single setback.

**The truth:** Per Sec. 803.3.b, TOSL includes "courts, yards, gardens, light wells, uncovered driveways, access roads and parking spaces" — the complete area outside the building footprint on all sides.

**Why it matters:** An exam question may describe a building with a generous front setback but minimal side and rear yards. The total open space must still meet or exceed the TOSL minimum percentage of TLA. You cannot satisfy TOSL with only one yard.

---

### TRAP 3 — Confusing MACA with AMBF

**The mistake:** Treating MACA as the building footprint.

**The truth:** AMBF is the building footprint in sq.m. MACA = PSO + ISA in percent — it includes the building and all paved areas outside it. MACA is always larger than or equal to PSO.

**Mnemonic:** MACA = More than just the building. AMBF = only the Actual building footprint.

**Example:** Basic R-2, no firewall. PSO = 55% (AMBF = 55% of TLA). MACA = 85% (building plus paving = 85% of TLA). The 30% gap between them is the ISA — the paved driveway and parking outside the building.

---

### TRAP 4 — Mixing Percentages with Square Meters

**The mistake:** Writing "PSO = 275 sq.m" on an exam answer.

**The truth:** PSO, ISA, USA, TOSL, and MACA are all percentages (%). AMBF is an area in square meters (sq.m). The conversion is explicit:

```
AMBF (sq.m) = TLA (sq.m) x PSO (%)
```

**Why it matters:** Exam distractors frequently include both "55%" and "275 sq.m" (for a 500 sq.m lot with PSO = 55%) as answer choices. They are testing whether you know which term uses which unit. Assigning an area value to PSO, or a percentage value to AMBF, is an immediate wrong answer.

---

### TRAP 5 — Using Only Table VIII.1 to Determine PSO

**The mistake:** Looking up Table VIII.1, finding the PSO, and stopping there.

**The truth:** Per Rule VII, Sec. 704.4.a — when values from Table VIII.1, Tables VIII.2 and VIII.3 (setbacks), Table VII.1 (occupancy and lot-type PSO), and the Fire Code conflict, **the more stringent but applicable regulation shall be observed.**

**Example:** Table VIII.1 says Basic R-2 (with firewall) PSO = 60%. But Table VII.1 says the inside-lot PSO for that building height is 55%. The answer is 55% — the more restrictive value governs.

---

## Worked Example — Full Calculation Chain

**Problem:** A single-family dwelling is proposed on a Basic R-2 lot. TLA = 500 sq.m. No firewall. Calculate all area metrics.

| Step | Metric | Source / Formula | Calculation | Result |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Max PSO | Table VIII.1 (Basic R-2, no firewall) | — | **55%** |
| 2 | AMBF | TLA x PSO | 500 x 0.55 | **275 sq.m** |
| 3 | Min TOSL (%) | 100% - PSO | 100% - 55% | **45%** |
| 4 | TOSL (sq.m) | TLA x TOSL% | 500 x 0.45 | **225 sq.m** |
| 5 | Max ISA (%) | Table VIII.1 (Basic R-2, no firewall) | — | **30%** |
| 6 | ISA (sq.m) | TLA x ISA% | 500 x 0.30 | **150 sq.m** |
| 7 | Min USA (%) | Table VIII.1 (Basic R-2, no firewall) | — | **15%** |
| 8 | USA (sq.m) | TLA x USA% | 500 x 0.15 | **75 sq.m** |
| 9 | MACA (%) | PSO + ISA | 55% + 30% | **85%** |
| 10 | MACA (sq.m) | TLA x MACA% | 500 x 0.85 | **425 sq.m** |

**Self-check:** AMBF (275) + ISA area (150) + USA area (75) = 500. Equals TLA. Confirmed.

**Second check:** PSO (55%) + ISA (30%) + USA (15%) = 100%. Confirmed.

---

## Active Recall — Question Set

### Question 1 (Unit Recognition)

An architect states: "The PSO of this R-2 lot is 275 square meters." Which of the following is the correct interpretation?

A) The PSO is correctly stated as 275 sq.m.  
B) The architect has confused PSO (a percentage) with AMBF (an area).  
C) PSO can be expressed in sq.m when the lot is smaller than 1,000 sq.m.  
D) PSO = 275 sq.m is correct for a 500 sq.m lot at 55%.

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: B</b><br><br>
  PSO is always a percentage. The area corresponding to that PSO percentage is the AMBF.<br>
  For a 500 sq.m lot with PSO = 55%: AMBF = 500 x 0.55 = 275 sq.m.<br>
  So "275 sq.m" is the AMBF, not the PSO. The PSO is 55%. Choices A and D conflate the two terms.<br>
  Choice C is fabricated — there is no lot-size exception to PSO units.
</details>

---

### Question 2 (Table VIII.1 — Firewall vs. Lot Type)

An architect is designing a Basic R-2 project on a corner lot without a firewall. Which table provides the inside-lot vs. corner-lot PSO distinction?

A) Table VIII.1  
B) Table VIII.G.6  
C) Table VII.1  
D) Table VII.G.1

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: C</b><br><br>
  Table VIII.1 distinguishes by firewall status (with or without), not by lot type.<br>
  Table VII.1 provides the PSO caps organized by occupancy type and lot type (inside lot, corner lot, through lot).<br>
  Table VIII.G.6 provides TOSL requirements by lot type — useful but separate from PSO.<br>
  Table VII.G.1 is the FLAR table — not relevant to PSO or lot-type distinctions.
</details>

---

### Question 3 (Full Calculation)

An architect is designing a single-family residential project on a 1,000 sq.m Basic R-2 lot without a firewall. If the architect maximizes the building footprint and also maximizes the allowed paved driveways and walkways (ISA), what is the minimum area that must be dedicated strictly to soil, lawns, or planting (USA)?

A) 100 sq.m  
B) 150 sq.m  
C) 300 sq.m  
D) 450 sq.m

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: B — 150 sq.m</b><br><br>
  Step 1: Identify the zone → Basic R-2, no firewall.<br>
  Step 2: From Table VIII.1 → PSO = 55%, ISA = 30%, USA = 15%.<br>
  Step 3: USA in sq.m = 1,000 x 15% = <b>150 sq.m</b>.<br><br>
  Cross-check: MACA = 55% + 30% = 85%. Therefore 15% (= 150 sq.m) must remain unpaved.<br><br>
  <b>Why not 100 sq.m?</b> 100 sq.m corresponds to 10% — the USA for Basic R-2 <i>with firewall</i>. That choice is a deliberate distractor exploiting confusion between the firewall and non-firewall rows of Table VIII.1.
</details>

---

### Question 4 (Most Restrictive Rule)

Table VIII.1 gives a PSO of 70% for Max R-2 with firewall. Table VII.1 gives a PSO of 65% for the same lot type and height. Which value governs?

A) 70% — Table VIII.1 is the primary zoning table  
B) 65% — the more restrictive value governs per Sec. 704.4.a  
C) The architect may choose which table to apply  
D) 70% — the firewall entitlement overrides Table VII.1

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: B</b><br><br>
  Per Rule VII, Sec. 704.4.a: when values from different applicable tables conflict, the more stringent but applicable regulation shall be observed.<br>
  65% is more restrictive than 70% (it limits the building to a smaller footprint).<br>
  Neither table "trumps" the other — the most restrictive applicable value always governs. The architect has no discretion to choose between them.
</details>

---

## 60-Second Blitz Quiz (Active Recall)

Answer aloud. Time yourself. No peeking.

1. PSO + TOSL = ___%
2. TOSL = ___ + ___
3. MACA = ___ + ___
4. Basic R-2, no firewall: PSO = ___%
5. Basic R-2, no firewall: USA = ___%
6. Which table distinguishes inside lot vs. corner lot for PSO — Table VIII.1 or Table VII.1?
7. True or false: USA is "the true open space" per the IRR.
8. If PSO = 55% and ISA = 30%, what is MACA?
9. What is the formula to convert PSO percentage to AMBF in square meters?
10. Com-3 with firewall: PSO = ___%

<details>
<summary><b>Reveal Answers</b></summary>
<br>
1. <b>100%</b><br>
2. <b>ISA + USA</b><br>
3. <b>PSO + ISA</b><br>
4. <b>55%</b><br>
5. <b>15%</b><br>
6. <b>Table VII.1</b> (NOT Table VIII.1)<br>
7. <b>True</b> — per Rule VIII, Sec. 803.3.b.ii, USA "is the true open space"<br>
8. <b>85%</b><br>
9. <b>AMBF = TLA x PSO</b><br>
10. <b>90%</b>
</details>

---

## Verified Source Mapping

| Concept | Exact Citation in 2004 Revised IRR of PD 1096 |
| :--- | :--- |
| PSO definition | Rule VIII, Section 803.3 |
| AMBF definition and formula | Rule VIII, Section 803.3 (cross-referenced with Rule VII, Sec. 704.4.a) |
| ISA definition | Rule VIII, Section 803.3.b.i |
| USA definition (the "true open space") | Rule VIII, Section 803.3.b.ii |
| TOSL definition and components | Rule VIII, Section 803.3.b |
| MACA definition | Rule VIII, Section 803.3 (note c of Table VIII.1) |
| Table VIII.1 (all PSO, ISA, USA, TOSL, MACA values) | Rule VIII, Section 803.4 |
| Table VIII.1 firewall (e)/(f) distinction | Rule VIII, Table VIII.1 column headers |
| "Most restrictive" rule (when tables conflict) | Rule VII, Section 704.4.a |
| Inside lot vs. corner lot PSO | Rule VII, Table VII.1 |
| TOSL requirements by lot type | Rule VIII, Table VIII.G.6 |
| Setback tables (residential; commercial/industrial/institutional) | Rule VIII, Tables VIII.2 and VIII.3 |
| Size and dimensions of courts | Rule VIII, Section 804 |

> **Critical note:** Table VIII.1 and Table VII.1 both provide PSO values, but they organize them differently. Table VIII.1 organizes by zone and firewall status. Table VII.1 organizes by zone and lot type. Neither supersedes the other — when they give different values, the lower (more restrictive) PSO governs. This is a frequent source of exam errors.

---

_Return to this module in 3 days. If you can answer the Blitz questions cold without hesitation, proceed to the next module._
