# PD 1096 Rule VII: Calculating AMBF, PSO, ISA, USA, and MACA (The Area Metrics)

_An Immersive ALE Review Module (Exam‑Optimized)_

## The Real‑World Scenario (The Hook)

Imagine you are designing a **townhouse‑type residential project** on a **typical R‑2 lot in Quezon City**. The local zoning ordinance says “no more than 55% PSO, 30% ISA, 15% USA, and 45% TOSL.”  
Your brain must now **translate** these four percentages into **real‑world lines on the site plan**:

- **Where can you build the house?**
- **How much paving is allowed before you violate ISA?**
- **How much softscaping must you leave as USA?**
- **How deep must the front setback (TOSL) be?**

In this module, you’ll learn to **think in percentages first, then convert to square‑meters** only when you must. Exam questions almost always **test these four metrics together**, so we’ll design this module using **chunking, active recall, and behavioral “habit loops”** so you can **automatically** see the “area map” of the lot.

---

## Core Concepts (With Mental Anchors)

### 1. **AMBF – Allowable Maximum Building Footprint**

**Definition**:  
The **maximum horizontal shadow** (floor plan outline) the building main structure is allowed to cast on the lot, **after** subtracting setbacks, TOSL, fire‑separation lines, and special zoning rules.

**Formula (primary exam form)**:
\[
\text{AMBF} = \text{TLA} \times \text{PSO}
\]

**Mental anchor image**:

> “**AMBF is the largest rectangle you can draw on the lot where the building is allowed to sit.**”

**Educational psychology trick**:

- **Chunking**: Group “AMBF = TLA × PSO” as a single unit in your memory.
- **Dual coding**: Imagine AMBF as a **bold red rectangle** over the lot; everything outside it is **no‑build**.

---

### 2. **PSO – Percentage of Site Occupancy**

**Definition**:  
The **maximum percentage of TLA** that can be covered by **buildings and structures** (the built‑up area).

**Formula**:
\[
\text{PSO} = \frac{\text{AMBF}}{\text{TLA}} \times 100
\]

**Mental anchor**:

> “**PSO = ‘How much of the lot can be built on?’**”

**Exam‑style nuance**:

- PSO is a **percentage**, AMBF is the **square‑meter area** equivalent.
- In exams, you often compute **AMBF = TLA × PSO**, then check:
  - **Is the building outline within that rectangle?**
  - **Is there space for TOSL and ISA/USA?**

---

### 3. **ISA – Impervious Surface Area**

**Definition**:  
All **hard, sealed surfaces** on the lot:

- Driveways, courtyards, pathways, parking, and paved areas.
- But **not** grass, soil, planters, permeable pavers, or open landscaping.

**Formula (percentage and area)**:
\[
\text{ISA} (\%) = \frac{\text{ISA (sq.m)}}{\text{TLA}} \times 100
\]
\[
\text{ISA (sq.m)} = \text{TLA} \times (\text{ISA \%})
\]

**Mental anchor**:

> “**ISA = ‘Everything that rainwater cannot soak into’.**”

**Behavioral fix**:  
When you sketch a plan, **color‑code ISA gray**. If more than 30% is gray, you’re likely violating the code.

---

### 4. **USA – Unpaved Surface Area**

**Definition**:  
The **minimum open / soft area** required on the lot:

- Lawns, plantings, permeable ground surfaces.
- This is what stormwater can **infiltrate** through.

**Formula**:
\[
\text{USA} (\%) = \frac{\text{USA (sq.m)}}{\text{TLA}} \times 100
\]
\[
\text{USA (sq.m)} = \text{TLA} \times (\text{USA \%})
\]

**Mental anchor**:

> “**USA = ‘Green screen saver’ for the lot.**”

---

### 5. **MACA – Maximum Allowable Construction Area**

**Concept**:  
The **maximum percentage of the lot** that can be **built‑up plus paved** (PSO + ISA).  
USA is the **remainder**:

\[
\text{MACA} = \text{PSO} + \text{ISA}
\]
\[
\text{PSO} + \text{ISA} + \text{USA} \leq 100\%
\]

**Formula (percentage)**:
\[
\text{MACA} (\%) \leq 100\% - \text{min. USA} (\%)
\]

**Mental anchor**:

> “**MACA = PSO (built) + ISA (paved). USA is what’s left for drainage and greenery.**”

---

## The Hard Data (Cheat Sheet – “Exam‑Anchor Table”)

### Rule VIII.G Typical R‑2 Values (R‑2 Residential)

| Land Use Zoning             | Use / Group   | PSO % (Max.) | ISA % (Max.) | USA % (Min.) | TOSL % |
| --------------------------- | ------------- | ------------ | ------------ | ------------ | ------ |
| **R‑2** (Residential Basic) | Residential 2 | 55%          | 30%          | 15%          | 45%    |

> **Rule of thumb for memorization**:
>
> - **R‑2 = 55‑30‑15‑45** (PSO‑ISA‑USA‑TOSL).
> - Remember: **5 + 5 = 10; 3 + 1 = 4; 1 + 5 = 6; 4 + 5 = 9** – arbitrary, but it helps **link numbers**.

**Key exam‑style idea**:

- **PSO + ISA ≤ 85%** (100% − 15%).
- **TOSL = 45%** front open space (often treated as **part of USA**, unpaved / minimally paved).

---

## Step‑by‑Step Computation (Brain‑Friendly Flow)

### Example 1 – R‑2 Lot (TLA = 600 sq.m)

**Given**:

- TLA = 600 sq.m (R‑2 zoning).
- PSO = 55%, ISA = 30%, USA = 15%.

**Step 1 – AMBF (maximum building footprint)**  
\[
\text{AMBF} = \text{TLA} \times \text{PSO} = 600 \times 0.55 = 330 \, \text{sq.m}
\]

**Visual check**:

- The house main blocks must fit within 330 sq.m total footprint (sum of ground‑floor plan area of the house, not including detached garages if not counted as GFA).

---

### Step 2 – Maximum ISA (paved area)\*\*

\[
\text{ISA} = 600 \times 0.30 = 180 \, \text{sq.m}
\]

**Behavioral check**:

- If your **drive‑in, parking, courtyards, and side‑paving** total more than 180 sq.m, you’re violating ISA.

---

### Step 3 – Minimum USA (green / unpaved)\*\*

\[
\text{USA} = 600 \times 0.15 = 90 \, \text{sq.m}
\]

**Rule of thumb**:

- **USA must be ≥ 90 sq.m** (e.g., front lawn, side plantings, rear yard).

---

### Step 4 – MACA (max built‑up + paved)\*\*

\[
\text{MACA} = \text{PSO} + \text{ISA} = 55\% + 30\% = 85\%
\]
\[
\text{MACA (sq.m)} = 600 \times 0.85 = 510 \, \text{sq.m}
\]

**Quick check**:

- AMBF + ISA = 330 + 180 = 510 sq.m → **exactly** MACA.
- If your **built‑up plus paved** exceeds 510 sq.m, you’ve exceeded MACA.

---

### Step 5 – TOSL (front setback)\*\*

- TOSL = 45% of TLA = 600 × 0.45 = **270 sq.m**.
- This is the **minimum open front area** facing the RROW.
- It is usually **counted within the USA** (unpaved or minimally paved).

**Visual cue**:

- Draw a **270 sq.m** rectangle along the front; inside it:
  - No main building mass.
  - No heavy parking.
  - Mostly lawn, landscaping, or light paving.

---

## ALE Exam Traps and “Enemy List” (Behavioral Antidote)

### 1. **Confusing PSO and AMBF**

**Trap**:

- Using “PSO = 55%” and saying “the building can be 55 sq.m” (confusing percentage with area).

**Fix**:

- **Chunk PSO and AMBF together**:
  - “**PSO % → AMBF area = TLA × PSO.**”
- **Say it out loud while solving**: “First percentage, then multiply for area.”

---

### 2. **Swapping ISA and USA**

**Trap**:

- Thinking “ISA = unpaved” or “USA = paved.”

**Memory hack**:

- **Acronym reminders**:
  - **ISA = Impervious (water‑resistant) / Surface / Area**.
  - **USA = Unpaved / Soft / Area**.
- **Color coding**:
  - **ISA = gray**.
  - **USA = green**.

---

### 3. **Adding USA into MACA**

**Trap**:

- Writing “**MACA = PSO + ISA + USA**” or trying to include USA in the 85%.

**Rule that sticks**:

> “**MACA is the PART of the lot that is built‑on OR paved. USA is the REMAINDER.**”

**Mnemonic**:

> “**PSO + ISA = MACA; USA = 100 − MACA.**”

---

### 4. **Ignoring TOSL as a Separate Check**

**Trap**:

- Students focus on PSO, ISA, USA, but forget that **TOSL is a separate front‑open‑space requirement** that may eat into USA.

**Exam‑style note**:

- If TOSL is 45%, and you already used the whole 15% USA for side‑yard landscaping, you may **violate TOSL**.
- **TOSL must be preserved along the front**, separate from internal “greens.”

---

### 5. **Thinking AMBF = Actual Building Footprint**

**Trap**:

- Assuming the **AMBF** computed is the **exact building footprint** you must fill.

**Code‑reality**:

- AMBF is the **maximum allowed**.
- You can design a **smaller building** (e.g., 280 sq.m instead of 330) and still be compliant.
- **Actual footprint** can be **less than or equal to AMBF**.

**Behavioral fix**:

- Treat **AMBF as a cap**, not a target.
- On the exam, if the question asks “What is the AMBF?”, give **TLA × PSO**, even if the building shown is smaller.

---

## Active Recall Question (With Deep‑Thinking Cues)

**Question**:  
What does the acronym **PSO** stand for according to PD 1096 Rule VII?

A) Percentage of Space Occupied  
B) Percentage of Site Occupancy  
C) Planned Site Occupancy

<details>  
<summary>Answer and Explanation (With Mental‑Retention Hooks)</summary>

**Answer: B) Percentage of Site Occupancy**

**Explanation**:

- In **PD 1096 Rule VII**, **PSO** is defined as **“Percentage of Site Occupancy”**, meaning the **maximum percentage of the Total Lot Area (TLA)** that may be occupied by **buildings and structures**.
- To help you remember:
  - **PSO = ‘how much of the lot the building can occupy’.**
  - **PSO % → AMBF area = TLA × PSO.**
- **Why A and C are wrong**:
  - A, “Space” is vague; “**Site**” is the **lot area**.
  - C, “Planned” suggests it’s a design choice rather than a **code‑limit**.

**Exam‑style mental drill**:

- After reading this, close your eyes and **recite**:
  - “PSO = Percentage of Site Occupancy.”
  - “It means the building can occupy up to X% of the lot, and AMBF = TLA × X%.”
- Do this **3 times tonight** to anchor it in long‑term memory.

</details>

---

## Verified Sources (Exam‑Energy Mapping)

1. **PD 1096 2004 Revised IRR (DPWH Official)** –
   - **Rule VII** (AMBF, PSO, BHL, FLAR).
   - **Rule VIII, Table VIII.G** (PSO, ISA, USA, TOSL for **R‑2, R‑3, R‑4, C‑2, C‑3, D, E, F, G, H**).
   - **Pages ≈ 356 and 84** (site‑coverage and zoning‑based PSO/ISA/USA tables).

2. **PD 1096 2004 Revised IRR (Architecture Board Edition)** –
   - **Rule VIII, Table VIII.G** (R‑2 and other zoning classes).
   - Often used in reviewers; good for **visual pattern recognition** of the tables.

---

## Additional Details (Deep‑Structure Retention)

### 1. Mental “Flow Diagram” for Any Lot

For **any lot** you see in the exam, **run this 5‑step mental script**:

1. **Identify zoning (R‑2, R‑3, C‑2, C‑3, etc.)** → get **PSO, ISA, USA, TOSL** from Table VIII.G.
2. **Compute PSO → AMBF = TLA × PSO**.
3. **Compute ISA (max) = TLA × ISA %**.
4. **Compute USA (min) = TLA × USA %**.
5. **Check MACA = PSO + ISA ≤ 100% − USA** and **TOSL front area ≥ required %**.

---

### 2. Picture‑Based Mnemonics (Educational Psychology)

- **AMBF** = **red building outline** on the lot.
- **ISA** = **gray paved areas**.
- **USA** = **green lawn areas**.
- **TOSL** = **wide green rectangle** at the front.

When you’re anxious in the exam, **visualize the color map** before you write numbers.

---

### 3. Spaced‑Repetition Questions (Behavioral “Practice Loop”)

After studying this once, ask yourself:

1. “What is the formula linking PSO and AMBF?”
2. “If PSO = 55%, ISA = 30%, USA = 15%, what is MACA in %?”
3. “If TLA = 400 sq.m and PSO = 70%, what is AMBF?”
4. “If AMBF = 200 sq.m and TLA = 500 sq.m, what is PSO?”

**Schedule**:

- **1st recall**: Right after reading.
- **2nd**: Before bed.
- **3rd**: 2 days later.
- **4th**: 1 week later.

This **spaced‑repetition** pattern is known to boost **exam‑performance recall** across educational psychology studies.

---

### 4. Error‑Prevention “Cheat‑Glance”

When you’re in the exam and you’re about to start a lot‑plan computation, **scan this box**:

> **“PSO % → AMBF area = TLA × PSO.”**  
> **“ISA = paved; USA = unpaved; MACA = PSO + ISA; USA = 100 − MACA.”**  
> **“TOSL is the front open space, usually minimally paved.”**

Keep this 3‑line mantra mentally bookmarked. It’s **code‑accurate, exam‑safe, and brain‑friendly**.
