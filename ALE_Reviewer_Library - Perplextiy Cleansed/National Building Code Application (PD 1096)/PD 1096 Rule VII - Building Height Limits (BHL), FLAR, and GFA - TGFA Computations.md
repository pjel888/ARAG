# 🏢 Architecture Board Exam (ALE) Mastery: BHL, FLAR, & Area Computations

_Module Focus: Rule VII of the 2004 Revised IRR of PD 1096 — Decoded and Demystified_

---

## 🧠 The "Why It Matters" Scenario (Schema Activation)

Visualize this: You are the lead architect for a high-density office tower in a CBD. The client wants to maximize their profit by building as high and wide as possible. Your job is to thread the needle between **Building Height Limit (BHL)**, **Floor to Lot Area Ratio (FLAR)**, **Gross Floor Area (GFA)**, and **Total Gross Floor Area (TGFA)**.

If you mess up the FLAR, the building loses saleable space. If you confuse TGFA with building volume, the project fails compliance. The board exam tests exactly this: your ability to know which metric controls the _footprint_, which controls the _density_, and which controls the _vertical limit_.

**Reason for this module:** The ALE Area 3 (Architectural Design & Site Planning) carries 40% of the total exam weight. Zoning calculations under Rule VII are the single most common reason candidates fail this area. Mastering the formula chain below is non-negotiable.

---

## 🏗️ Core Concepts (The Foundation)

### 1. Building Height Limit (BHL)

- **Definition (per Revised IRR, Rule VII, Sec. 707):** The maximum height to be allowed for buildings/structures based on their proposed use or occupancy. The BHL is generally determined _after_ the application of other development controls and certain parameters (site conditions, view, etc.).
- **How it is measured:** From the **established grade line** (i.e., the highest adjoining public sidewalk or finished grade, or natural ground surface) to the **topmost portion** of the proposed building/structure. If applicable, the BHL may also be subject to clearance requirements of the Air Transportation Office (ATO).
- **The "3-meter tolerance" rule:** The height measured from the _lowest_ adjoining surface shall not exceed the maximum BHL by more than **3.00 meters**.

**Exemptions (NOT added to BHL):**

Signage, masts, antennas, telecom towers, beacons, and the like — these are permitted projections above the roof and are excluded from BHL measurement.

Additionally, towers, spires, and steeples erected as parts of the building and _not used for habitation or storage_ are limited as to height only by structural design if completely of incombustible materials, or may extend but **not exceed 6.00 meters** above the prescribed BHL if of combustible materials.

> **Reason for the Law:** BHL protects urban light and ventilation corridors, prevents overshading of adjacent properties, and ensures that infrastructure (roads, water, sewage) is not overwhelmed by population density that taller buildings bring.

---

### 2. Floor to Lot Area Ratio (FLAR)

- **Definition (per Revised IRR, Rule VII Guidelines, Table VII.G.1):** A development control (DC) that limits the designated right over the **Gross Floor Area (GFA)** that can be lawfully generated/developed for a given **Total Lot Area (TLA)**. Synonymous with FAR (Floor Area Ratio).
- **Application:** The FLAR shall be the **primary or initial determinant** of building bulk.
- **The Formula:**

```
Allowable Maximum GFA = TLA × FLAR
```

- **Mental Hook:** _FLAR is your area budget. BHL is your height ceiling. They work together — but FLAR almost always bites first._

> **Reason for the Law:** FLAR prevents overdevelopment of land. A small lot in a dense zone without FLAR control could theoretically support a skyscraper with no proportion to its surroundings. FLAR ensures the total habitable floor area remains proportional to the lot size and the zone's carrying capacity.

---

### 3. Gross Floor Area (GFA)

- **Definition (per Revised IRR):** The total floor space within the perimeter of the permanent external building walls, inclusive of the main and auxiliary buildings — such as office areas, residential areas, corridors, lobbies, and mezzanine level(s).
- **Included in GFA:** Building projections that serve as floors or platforms directly connected to/integrated with areas within the building/structure (e.g., balconies of **10.0 sq.m or less**).

**GFA Strictly EXCLUDES the following:**

| Exclusion Category        | Specific Items                                                                                                                                                                                                                                                   |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parking & driveways**   | Covered areas used for parking and driveways, services and utilities                                                                                                                                                                                             |
| **Vertical penetrations** | In parking floors where no residential or office units are present                                                                                                                                                                                               |
| **Uncovered areas**       | Helipads, A/C cooling towers, ACCU balconies, overhead water tanks, roof decks, laundry areas and cages, swimming/wading pools, whirlpools or Jacuzzis, terraces, gardens, courts/plazas, **balconies exceeding 10.0 sq.m**, fire escape structures and the like |

> **Reason for the Law:** GFA exclusions incentivize developers to provide parking, open recreational spaces, and fire safety infrastructure without penalizing them against their FLAR allowance. If parking counted toward GFA, developers would minimize parking to maximize saleable area — creating traffic nightmares.

---

### 4. Total Gross Floor Area (TGFA)

- **Definition:** The total floor space within the main and auxiliary buildings, primarily consisting of the **GFA plus all other enclosed and covered areas** (the non-GFA components such as parking, utility rooms, balconies over 10 sq.m, fire escape structures, etc.).
- **The Formula:**

```
TGFA = GFA + Non-GFA Areas
```

|          |                                                                                                  |
| :------- | :----------------------------------------------------------------------------------------------- |
| **TGFA** | = GFA (habitable/saleable floor area)                                                            |
|          | + Non-GFA (parking decks, covered driveways, utility areas, large balconies, fire escapes, etc.) |

### 🚨 CRITICAL: TGFA vs. Building Volume

**Stop. Read this twice.**

- **TGFA** is measured in **square meters** (sq.m). It is the sum of all floor areas.
- **Building Volume / Allowable Maximum Volume of Building (AMVB)** is measured in **cubic meters** (cu.m).
- The formula `AMBF × BHL` yields the **Allowable Maximum Volume of Building (AMVB)** — a _volume_ measure used to establish the building bulk envelope, NOT the TGFA.
- The Revised IRR uses Table VII.1 to derive the **Allowable Maximum TGFA** based on the Allowed **Percentage of Site Occupancy (PSO)** as a percentage of TLA — this is a _separate_ control from FLAR.

> **Reason for the Law:** TGFA captures the _total_ building mass for infrastructure load assessment — parking, utility rooms, and service areas all place load on roads, sewage, and fire systems, even though they do not count toward the saleable/habitable GFA.

---

## 📐 The Master Formula Chain

_This is the exact sequence tested in ALE Area 3. Memorize the order._

**Mnemonic: "TaPa-TAFB" (Tatay, Palengke — Total, Area, Floors, Building)**

```
Step 1:  TLA   (Total Lot Area) — from the title or survey
             ↓
Step 2:  PSO   (Percentage of Site Occupancy) — from zoning table
             ↓
Step 3:  TOSL  = TLA × (1 - PSO)     ← Total Open Space within Lot
             ↓
Step 4:  AMBF  = TLA × PSO            ← Allowable Maximum Building Footprint
             ↓
Step 5:  FLAR  (Floor to Lot Area Ratio) — from Table VII.G.1
             ↓
Step 6:  Max GFA = TLA × FLAR         ← Your "area budget"
             ↓
Step 7:  Max Floors (by area) = Max GFA ÷ AMBF
             ↓
Step 8:  BHL   — cross-check with Table VII.2 (height ceiling)
             ↓
         USE THE MORE RESTRICTIVE between Step 7 and Step 8.
```

> **The key insight:** FLAR and BHL are _two independent controls_. Even if the BHL allows 18 storeys, the FLAR may only generate enough GFA for 10 storeys at full footprint. Conversely, even if FLAR allows massive floor area, you cannot exceed the BHL. Always apply both, then take the more restrictive result.

---

## 📊 The Hard Data Cheat Sheet

_Data strictly based on the 2004 Revised IRR of PD 1096 (published by DPWH, April 2005). Examiners test these exact brackets._

### Table A: FLAR Designations/Rights (from Table VII.G.1)

| Occupancy                       | Classification              | FLAR Value/Range  | Associated BHL              |
| :------------------------------ | :-------------------------- | :---------------- | :-------------------------- |
| **Residential 1 (R-1)**         | Single-family exclusive     | **1.30**          | 3 storeys / 10.00 m         |
| **Residential 2 (R-2) Basic**   | Single-attached / duplex    | **1.50**          | 3 storeys / 10.00 m         |
| **Residential 2 (R-2) Maximum** | Low-rise multi-family       | **2.10 to 3.00**  | 5 storeys / 15.00 m         |
| **Residential 3 (R-3) Basic**   | High-density residential    | **up to 2.10**    | 3 storeys / 10.00 m         |
| **Residential 3 (R-3) Maximum** | High-density residential    | **2.10 to 8.10**  | 12 storeys / 36.00 m        |
| **Residential 4 (R-4)**         | Townhouses (individual lot) | **2.60 to 2.80**  | 3 storeys / 10.00 m         |
| **Residential 5 (R-5)**         | Condominiums                | **5.00 to 10.00** | 18 storeys / 54.00 m        |
| **Commercial 1 (C-1)**          | Light / Neighborhood        | **1.70 to 3.00**  | 3–5 storeys / 10–15.00 m    |
| **Commercial 2 (C-2)**          | Medium Intensity            | **3.60 to 9.00**  | 6 storeys / 18.00 m         |
| **Commercial 3 (C-3)**          | Metropolitan / CBD          | **3.00 to 12.00** | 16–60 storeys / 48–180.00 m |
| **Industrial 1 (I-1)**          | Light                       | **2.50 to 3.00**  | 15.00 m (or zone BHL)       |
| **Industrial 3 (I-3)**          | Heavy                       | **3.00 to 5.00**  | 27.00 m (or zone BHL)       |
| **PUD Inland**                  | Planned Unit Dev.           | **8.00 to 34.00** | 12–60 storeys / 36–180.00 m |

### Table B: Building Height Limit by Occupancy (from Table VII.2)

| Occupancy             | Allowable Storeys | BHL (Meters above Grade)  |
| :-------------------- | :---------------- | :------------------------ |
| **R-1**               | 3                 | 10.00 m                   |
| **R-2 Basic**         | 3                 | 10.00 m                   |
| **R-2 Maximum**       | 5                 | 15.00 m                   |
| **R-3 Basic**         | 3                 | 10.00 m                   |
| **R-3 Maximum**       | 12                | 36.00 m                   |
| **R-4 (Townhouse)**   | 3                 | 10.00 m                   |
| **R-5 (Condominium)** | 12 to 18          | 36.00 to 54.00 m          |
| **C-1**               | 3 to 5            | 10.00 to 15.00 m          |
| **C-2**               | **6**             | **18.00 m**               |
| **C-3**               | **16 to 60**      | **48.00 to 180.00 m**     |
| **I-1**               | —                 | 15.00 m (zone-restricted) |
| **I-2**               | —                 | 21.00 m (zone-restricted) |
| **I-3**               | —                 | 27.00 m (zone-restricted) |
| **Institutional**     | —                 | 15.00 m (or zone BHL)     |
| **Cultural**          | —                 | 30.00 m (or zone BHL)     |

> **RROW Override Rule:** Regardless of occupancy or lot size, BHL is capped if only one RROW services the lot:
>
> - RROW 6.00–7.00 m wide → BHL max **3 storeys / 9.00 m**
> - RROW 4.00–5.00 m wide → BHL max **2.5 storeys / 7.50 m**
> - RROW 3.00 m or less → BHL max **2 storeys / 6.00 m**

---

## ⚠️ High-Yield Exam Traps (Von Restorff Effect)

Your brain naturally seeks shortcuts. Break these bad habits _before_ exam day:

---

### 🚨 TRAP #1: Confusing Area (TGFA) with Volume (AMVB)

|                       | Wrong                   | Right                                                              |
| :-------------------- | :---------------------- | :----------------------------------------------------------------- |
| **Formula**           | `AMBF × BHL = TGFA`     | `AMBF × BHL = AMVB (Volume)`                                       |
| **Unit**              | sq.m (WRONG)            | cu.m (Volume)                                                      |
| **What it gives you** | Nothing useful for TGFA | The Allowable Maximum Volume of Building — a bulk/envelope control |

**Fix:** TGFA is derived from the PSO table (Table VII.1), NOT from multiplying footprint by height. If you see "AMBF × BHL" on the exam, that answer is about _volume_, not _area_.

---

### 🚨 TRAP #2: The "C-2 BHL" Hallucination

|              | Wrong (Original Material) | Right (per Table VII.2)      |
| :----------- | :------------------------ | :--------------------------- |
| **C-2 BHL**  | 36.00 meters / 12 storeys | **18.00 meters / 6 storeys** |
| **C-2 FLAR** | 3.60 to 9.00 (correct)    | 3.60 to 9.00 (correct)       |

**Why this matters:** C-2 has a high FLAR range (up to 9.0) but a LOW BHL (only 6 storeys). This is a deliberate regulatory design — the code allows dense floor area but caps the height for medium-intensity commercial zones. Many students assume high FLAR = high BHL. Wrong. They are independent controls.

---

### 🚨 TRAP #3: The "C-3 FLAR" Overestimate

|              | Wrong (Common Assumption) | Right (per Table VII.G.1)             |
| :----------- | :------------------------ | :------------------------------------ |
| **C-3 FLAR** | 9.00 to 34.00             | **3.00 to 12.00**                     |
| **C-3 BHL**  | 60.00 to 180.00+ m        | **48.00 to 180.00 m** (16–60 storeys) |

**Why this matters:** The FLAR of 34.00 belongs to **PUD at an inland area** (Planned Unit Development), NOT to C-3. C-3 is capped at FLAR 12.00. Confusing PUD values with C-3 values is a classic exam trap because both share the 60-storey/180 m BHL ceiling.

---

### 🚨 TRAP #4: Adding Parking to GFA

|                   | Wrong                                     | Right                                               |
| :---------------- | :---------------------------------------- | :-------------------------------------------------- |
| **What you did**  | Included 3 basement parking levels in GFA | Covered parking is **explicitly excluded** from GFA |
| **Where it goes** | (nowhere, you wasted saleable area)       | Parking is included in TGFA, but NOT in GFA         |

**Why this matters:** GFA drives your FLAR calculation. If you add parking to GFA, your "used" GFA will appear to exceed the FLAR allowance when in reality it does not. This costs you the entire FLAR computation on the exam.

---

### 🚨 TRAP #5: Balcony Threshold

|             | Counted in GFA        | Excluded from GFA       |
| :---------- | :-------------------- | :---------------------- |
| **Balcony** | 10.0 sq.m **or less** | **Exceeding** 10.0 sq.m |

**Why this matters:** A question may describe a unit with a 12 sq.m balcony. That balcony is excluded from GFA. If it were 9 sq.m, it would be included. The threshold is exactly **10.0 sq.m** — memorize it.

---

## 🔄 Active Recall Challenge

### Question 1 (FLAR Compliance)

You are designing a Commercial C-2 building on a 1,000 sq.m lot. The local zoning ordinance enforces a maximum FLAR of 4.0. Your proposed design has a total GFA of 5,000 sq.m. What is the regulatory status of your design?

A) It complies, as long as the building is under 18.00 meters (6 storeys).
B) It complies, because 5,000 sq.m is within the standard C-2 code limits.
C) It violates the code because the maximum allowable GFA is 4,000 sq.m.
D) It violates the code because GFA must include parking spaces.

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: C</b><br><br>
  <b>Why?</b><br>
  Step 1: Recall the formula — <code>Max GFA = TLA × FLAR</code>.<br>
  Step 2: Calculate — 1,000 sq.m × 4.0 = 4,000 sq.m (Maximum Allowable GFA).<br>
  Step 3: Compare — Your design proposes 5,000 sq.m GFA, which exceeds the limit by 1,000 sq.m.<br>
  Step 4: Even if the building height is within BHL, the floor area density exceeds the FLAR allowance. Both controls must be satisfied independently.<br><br>
  <b>Why the other answers are wrong:</b><br>
  A — Height compliance alone does not satisfy FLAR.<br>
  B — The standard C-2 FLAR range is 3.60 to 9.00, but the local zoning ordinance has set a more restrictive 4.0, which governs.<br>
  D — Parking is excluded from GFA, not included.
</details>

---

### Question 2 (BHL Application)

A C-2 commercial lot fronts a single RROW that is 5.00 meters wide. Per Table VII.2, the C-2 BHL is 18.00 meters / 6 storeys. What is the actual maximum BHL for this building?

A) 18.00 meters (6 storeys)
B) 15.00 meters (5 storeys)
C) 9.00 meters (3 storeys)
D) 7.50 meters (2.5 storeys)

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: D</b><br><br>
  <b>Why?</b><br>
  The RROW override rule states: If only one RROW services a lot and it is only 4.00 to 5.00 meters wide, a BHL equivalent to <b>2.5 storeys (or 7.50 meters maximum)</b> shall be observed — <b>regardless of use or occupancy, lot size, or lot dimensions</b>.<br><br>
  The C-2 occupancy BHL of 18.00 m is overridden by the more restrictive RROW-based BHL.
</details>

---

### Question 3 (GFA Exclusion)

A residential condominium (R-5) has the following on its 8th floor: 800 sq.m of residential units, a 50 sq.m lobby/corridor, a 200 sq.m covered parking area, and twenty 12 sq.m balconies (one per unit). What is the GFA of this floor?

A) 1,290 sq.m
B) 1,050 sq.m
C) 850 sq.m
D) 1,090 sq.m

<details>
  <summary><b>Click to reveal the answer</b></summary>
  <br>
  <b>Correct Answer: C</b><br><br>
  <b>Why?</b><br>
  - Residential units: 800 sq.m → <b>Included</b> in GFA<br>
  - Lobby/corridor: 50 sq.m → <b>Included</b> in GFA<br>
  - Covered parking: 200 sq.m → <b>Excluded</b> from GFA<br>
  - Twenty 12 sq.m balconies: Each exceeds 10.0 sq.m → <b>Excluded</b> from GFA<br><br>
  GFA = 800 + 50 = <b>850 sq.m</b><br><br>
  The 200 sq.m parking and 240 sq.m of balconies (20 × 12) are part of the TGFA, but not the GFA.
</details>

---

## 📝 60-Second Blitz (Say Aloud, No Peeking)

1. What is the FLAR for R-1? → \_\_\_
2. What is the BHL for C-2? → **_ storeys / _** meters
3. Balconies exceeding \_\_\_ sq.m are excluded from GFA.
4. `AMBF × BHL` gives you \_\_\_ (Volume/Area)?
5. If only one RROW of 3.00 m services your lot, the BHL is capped at **_ storeys / _** meters.

<details>
  <summary><b>Answers</b></summary>
  <br>
  1. <b>1.30</b><br>
  2. <b>6 storeys / 18.00 meters</b><br>
  3. <b>10.0</b> sq.m<br>
  4. <b>Volume</b> (AMVB, in cubic meters)<br>
  5. <b>2 storeys / 6.00 meters</b>
</details>

---

## 📚 Verified Source Mapping

| Section                      | Governing Provision                                         |
| :--------------------------- | :---------------------------------------------------------- |
| BHL Definition & Measurement | Rule VII, Sec. 707; Table VII.2                             |
| FLAR Designations/Rights     | Rule VII Guidelines, Table VII.G.1                          |
| GFA Definition & Exclusions  | Rule VII, Sec. 704 (as supplemented by Rule VII Guidelines) |
| TGFA Definition              | Rule VII, Sec. 704 (TGFA = GFA + Non-GFA areas)             |
| Allowable Max TGFA by PSO    | Rule VII, Table VII.1                                       |
| RROW Override on BHL         | Rule VII, Sec. 707 (end notes to Table VII.2)               |
| Building Volume (AMVB)       | Rule VII Guidelines, Sec. B                                 |
| PSO / TOSL / AMBF formulas   | Rule VII Guidelines, Sec. A                                 |
| Occupancy Classification     | Rule VII, Sec. 701 (10 Groups, 25 Divisions)                |

> **Important:** Table VII.1 establishes the **Allowable Maximum TGFA** based on PSO (as a percentage of TLA). Table VII.G.1 establishes the **FLAR** (which limits GFA). These are two different tables controlling two different metrics. Do not confuse them.

---

_Return to this module in 3 days. If you can answer the Blitz questions cold, move to the next module._
