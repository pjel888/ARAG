# PD 1096 Rule VII: Building Height Limits (BHL), FLAR, and GFA/TGFA Computations

_An Immersive ALE Review Module (Exam‑Optimized)_

## The Real‑World Scenario (The Hook)

Visualize this:  
You are the lead architect for a **tower office and retail complex** on a **high‑density lot along Ayala Avenue in Makati**. The client wants the **maximum buildable area and height** for the budget, but the **local zoning ordinance** and **PD 1096** must be obeyed. You realize that **Building Height Limit (BHL)**, **Floor to Lot Area Ratio (FLAR)**, **Gross Floor Area (GFA)**, and **Total Gross Floor Area (TGFA)** are **all chained together** like a sequence of conditional equations. If you get **one wrong** (e.g., FLAR, BHL, or AMBF), the **whole volume stack crashes**—your exam will behave the same way.

In this module, you will **learn Rule VII “forward” (how to compute it)** and **“backward” (how exam questions manipulate it)** so that when you see “Given TLA, FLAR, BHL, PSO, and AMBF…”, you **already know the script**.

---

## Core Concepts (With Cognitive “Anchor” Phrases)

### 1. Building Height Limit (BHL)

**Definition**:  
The **maximum height** (in meters or storeys) a building can reach **for its occupancy group**, **after** applying all other development controls (PSO, AMBF, TOSL, setbacks, angular planes, and local zoning).

**What is EXCLUDED from BHL** (so you don’t waste exam points):

- Signage structures.
- Certain parapets.
- Rooftop utility housings or catwalks that meet **material and height exceptions** in the code.

**Mnemonic / Anchor** (create a mental image):

> “**BHL is the ‘ceiling sticker’ posted on the lot. The building can’t spike a pencil above it.**”

**Educational‑psychology strategy**:

- **Chunking + Narrative** – Think of BHL as the **final height cap**, not a magic number you pick first.
- **Elaboration** – Link BHL to **occupancy group** (e.g., C‑3 → high‑rise, C‑2 → low‑rise, R‑4/R‑5 → medium‑rise dwellings).

---

### 2. Floor to Lot Area Ratio (FLAR)

**Definition**:  
FLAR is the **leverage multiplier** that converts **Total Lot Area (TLA)** into **maximum allowable GFA** for a **given occupancy and zoning**.

**Formula**:  
\[
\text{GFA} = \text{TLA} \times \text{FLAR}
\]

**Mnemonic / Anchor**:

> “**FLAR = ‘How many square meters of floor you can print on this lot.’**”

**Key exam‑style idea**:

- FLAR is **NOT** the building height; it is **area density**.
- Higher FLAR = **denser floor stack**, but **BHL** still controls **how tall** that stack can be.
- **Zoning** often **caps** FLAR (e.g., QC vs Metro Manila special district).

---

### 3. Gross Floor Area (GFA)

**Definition**:  
GFA is the **sum of habitable and occupiable floors** inside the building envelope, per level, **excluding** non‑occupiable spaces such as:

- Purely outdoor roof decks.
- Uncovered parking used only for vehicles.
- Some shafts and service rooms (depending on interpretation).

**Mnemonic / Anchor**:

> “**GFA = everything people can walk into, sit on, or sleep in.**”

**Exam‑style boundary**:

- If the examiner says “exclude ordinary roof decks and vehicular parking from GFA,” **obey that**.
- This is where **students lose points**—they add parking or roofs to GFA and blow up the numbers.

---

### 4. Total Gross Floor Area (TGFA)

**Definition**:  
TGFA is the **total enclosed volume** of the building, conceptually:

\[
\text{TGFA} \approx \text{BHL} \times \text{AMBF} \times \text{adjustment factor}
\]

Where:

- **BHL** = height limit (m).
- **AMBF** = Allowable Maximum Building Footprint (m²).
- **Adjustment factor** = Rule‑VIII‑derived correction for setbacks, courts, incremental setbacks, and volume rules.

**Mnemonic / Anchor**:

> “**TGFA = the building’s ‘cube’ (BHL × AMBF), then sliced by the code’s rules.**”

**Crucial behavioral trap alert**:  
Many students say:

> “TGFA = GFA ÷ 1.5”

**This is WRONG.**

- **TGFA → GFA conceptually**, not the reverse.
- **There is NO fixed universal multiplier** (like 1.5) in PD 1096; the **1.5 myth** is a simplification some reviewers use, but the **code** expresses TGFA as a **volume‑based computation**, not a GFA‑ratio hack.

---

## The Hard Data (Cheat Sheet – “Exam‑Filter” Table)

### Rule VII FLAR & BHL “Region Map”

| Building Use / Occupancy Group | Typical FLAR Range (Zoning‑Adjusted) | Typical BHL Range (Storeys / m)  | Notes for Exam                                     |
| ------------------------------ | ------------------------------------ | -------------------------------- | -------------------------------------------------- |
| **Residential R‑4 / R‑5**      | 2.5–4.0 (medium‑high density)        | Up to **18 storeys or 54 m**     | Think condo towers, mixed‑use podium.              |
| **Commercial C‑2**             | 2.5–4.0 (low‑intensity)              | Up to **6 storeys or 18 m**      | Think small office buildings, service‑type retail. |
| **Commercial C‑3**             | 4.0–9.0 (high‑intensity)             | **16–60 storeys / up to ~180 m** | High‑rise towers, CBD/central business district.   |

> **Rule**:
>
> - These are **ranges from the 2004 RIRR Tables VII.G.1 and VII.G.2**, **not absolute limits**.
> - **Actual BHL and FLAR** for a lot depend on **zoning, AMBF, setbacks, angular planes, and local ordinances**.

---

### Corridor 1 – Exam‑Ready “Decision Tree”

When you read a question, **scan the flowchart in your mind**:

1. **What is the occupancy group?** → Fix the **BHL bracket** (C‑2 vs C‑3 vs R‑4/R‑5).
2. **What is the zoning / FLAR band?** → Pick **FLAR** (e.g., 4.0 vs 9.0).
3. **What is TLA?** → Compute **GFA = TLA × FLAR**.
4. **What is PSO / AMBF?** → Compute **AMBF = TLA × PSO** (if PSO given).
5. **What is BHL?** → Compute **TGFA ≈ BHL × AMBF × factor**.
6. **Compare GFA to TGFA**:
   - If **GFA ≤ TGFA** → Design is **permissible** (within code volume).
   - If **GFA > TGFA** → Design **exceeds allowable volume**, even if the floors “fit” in plan.

---

### Corridor 2 – “Numbers You Must Remember”

| Idea     | Must‑Know Number / Rule                                              |
| -------- | -------------------------------------------------------------------- |
| **BHL**  | Occupancy‑driven range (e.g., C‑3 → 16–60 st / 180 m max).           |
| **FLAR** | No **universal** value; **Table VII.G.1** per zoning.                |
| **GFA**  | **GFA = TLA × FLAR** (no parking, no roof decks).                    |
| **TGFA** | **TGFA ≈ BHL × AMBF × factor** (no fixed 1.5 divisor from the code). |
| **AMBF** | **AMBF = TLA × PSO** (PSO from zoning Table VIII.G).                 |

---

## Step‑by‑Step Computation (Exam‑Style, “Brain‑Friendly” Flow)

### Example 1 – GFA from FLAR (Open‑Plan Office, C‑3, TLA = 800 sq.m)

**Given**:

- TLA = 800 sq.m (high‑density urban lot, **C‑3 occupancy**).
- FLAR = **9.0** (zoning‑allowed maximum for this site).

**Step 1 – Compute GFA**:
\[
\text{GFA} = \text{TLA} \times \text{FLAR} = 800 \, \text{sq.m} \times 9.0 = 7200 \, \text{sq.m}
\]

**Interpretation**:

- This is the **maximum floor area** you can design **before** checking height and volume.
- Higher FLAR = **more floor area per lot**, but **not more height** by itself.

---

### Example 2 – TGFA from BHL, AMBF, and PSO (High‑Rise Logic)

**Given**:  
Same lot (800 sq.m, C‑3, FLAR = 9.0).  
Additional data (often in exams):

- **PSO** = 60% (zoning‑allowable site occupancy).
- **AMBF** = TLA × PSO = 800 × 0.60 = **480 sq.m**.
- **BHL** = 120 m (allowed for C‑3, mixed‑use podium‑type project).
- **Adjustment factor** (simplified exam setting) ≈ 1.0 (no extra setbacks).

**Step 1 – Compute TGFA**:
\[
\text{TGFA} \approx \text{BHL} \times \text{AMBF} = 120 \, \text{m} \times 480 \, \text{sq.m} = 57,600 \, \text{cu.m}
\]

**Step 2 – Link GFA to TGFA**:

- GFA = **7200 sq.m** (flat‑area sum).
- **Total usable volume** (TGFA) = **57,600 cu.m**.
- **Average floor height** = \( \text{TGFA} / \text{GFA} \):  
  \[
  \text{Average floor height} = \frac{57,600}{7200} = 8.0 \, \text{m per floor}
  \]
  → This is **too high** for normal office floors (typical 3.5–5.0 m).

**Exam‑style interpretation**:

- The **exam** will **not** ask for average height, but it will **ask** if the **proposed scheme violates BHL or FLAR**.
- Your job is to:
  1. **Check GFA vs TLA × FLAR**.
  2. **Check BHL vs zoning‑allowed BHL**.
  3. **Verify PSO vs zoning‑PSO**.
  - If all three are within limits, the scheme is **permissible in volume** (subject to fire‑safety, egress, etc., covered in other rules).

---

### Example 3 – “Trap” Variant (FLAR vs BHL Mismatch)

**Scenario**:

- A student assumes **C‑3 FLAR = 9.0 ⇒ BHL = 180 m** automatically.
- Answer: “C) 16–60 storeys, up to 180 m.”

**Nuance (exam‑style twist)**:

- FLAR **controls floor area density**.
- BHL **controls height**.
- Some zoning areas **cap BHL below the code maximum** (e.g., 100 m instead of 180 m).
- So **FLAR 9.0 + C‑3 = high‑floor‑area + high‑rise**, but **maximum BHL still depends on zoning**.

---

## ALE Exam Traps and Behavioral “Enemy List”

### 1. **Mistaking FLAR for Height**

**Trap**:  
“Higher FLAR = automatically taller building.”

**Cognitive correction**:

- FLAR = **floor area multiplier**.
- BHL = **height cap**.
- Create mental image:
  - FLAR = **how thin you slice the loaf** (more floors).
  - BHL = **how tall the loaf stand is**.

**Exam‑safe habit**:

- Always answer: “FLAR sets **GFA**, BHL sets **height**; both must be within zoning limits.”

---

### 2. **TGFA = GFA ÷ 1.5 Myth**

**Trap**:

- Students memorize:
  \[
  \text{TGFA} = \frac{\text{GFA}}{1.5}
  \]
  and **blindly apply it**.

**Reality**:

- **No such formula exists** in PD 1096.
- TGFA is **volume‑based**:
  \[
  \text{TGFA} \approx \text{BHL} \times \text{AMBF} \times \text{factor}
  \]
- GFA is **a portion of** that TGFA (after removing non‑occupiable spaces).

**Behavioral fix**:

- Use **conceptual framing**:
  - “TGFA is the building’s **total volume box**; GFA is **how tightly packed** people are inside that box.”

---

### 3. **Ignoring Local Zoning**

**Trap**:  
Students fix on **code‑maximum** FLAR and BHL (e.g., 9.0, 180 m) and forget that:

- **Zoning may cap**:
  - FLAR lower (e.g., 6.0).
  - BHL lower (e.g., 100 m).

**Exam‑style phrase to watch for**:  
“Assuming the city zoning ordinance limits BHL to 100 m and FLAR to 6.0…”

**Behavioral strategy**:

- **Underline** “zoning ordinance” when you see it.
- Re‑compute **GFA = TLA × zoning‑FLAR**, not code‑maximum FLAR.
- Use **BHL = zoning‑BHL**, not generic “180 m”.

---

### 4. **Mixing Up GFA and TGFA Roles**

**Trap**:

- Students try to **derive GFA from TGFA** using a fixed multiplier.
- They invert the **conceptual flow** (TGFA → GFA vs GFA → TGFA).

**Cognitive hack**:

- Remember the **chain of dependence**:
  - **TLA** → **GFA** (via FLAR).
  - **AMBF + BHL** → **TGFA** (volume).
  - **Then**: GFA ≤ TGFA (code‑logically).

---

## Active Recall Question (Exam‑Style, With Deep‑Thinking Hints)

**Question**:  
Which statement best describes the maximum Building Height Limit (BHL) for a **Commercial C‑3 building with an FLAR of 9.0**, assuming **high‑density zoning that allows maximum code‑BHL**?

A) Up to 18 storeys or 54 m  
B) Up to 6 storeys or 18 m  
C) 16–60 storeys, up to about 180 m

> **Answer: C) 16–60 storeys, up to about 180 m**

> **Explanation (with behavior‑based reinforcement)**:
>
> - **Commercial C‑3** is a **high‑intensity occupancy** with **higher FLAR rights** (up to about 9.0) and **higher BHL ranges** (16–60 storeys, up to about 180 m), **when zoning allows**.
> - **FLAR** sets **GFA = TLA × FLAR = dense floor stack**.
> - **BHL** sets **how tall** that stack can be.
> - Always check local **zoning BHL caps**; if the ordinance says “max BHL = 100 m”, even FLAR 9.0 **must fit within 100 m**.
> - **Wrong choice logic**:
>   - A → too low (typical C‑2 or R‑4).
>   - B → typical low‑intensity C‑2.

**Deep‑thinking prompt (for brain‑retention)**:  
On your scratch paper, sketch a **simple 2‑column table**:

1. **Left column**: Uses (C‑2, C‑3, R‑4/R‑5).
2. **Right column**: Typical FLAR + BHL brackets.  
   Fill it once, **close your notes**, and test yourself **3–5 times** over 2 weeks.

---

## Verified Sources (Exam‑Style Reference)

1. **PD 1096 2004 Revised IRR (DPWH Official)** –
   - **Rule VII**, **Table VII.G.1** (FLAR rights per occupancy / zoning).
   - **Rule VII, Table VII.G.2** (TGFA‑related BHL framework and adjustment factors).
   - **Pages ≈ 362–367** (GFA, TGFA, BHL, FLAR volume relationships).

2. **Architecture‑Board Edition of PD 1096 2004 RIRR** –
   - **Pages ≈ 91** (FLAR and BHL summary tables).
   - Often republished in reviewer guides; useful for **visual memory** of the tables.

---

## Additional Details (Deep‑Structure, Long‑Term Retention)

### 1. Behavioural Psychology Angle – “Repeat‑to‑Retain” Patterns

- \*\*Sp
