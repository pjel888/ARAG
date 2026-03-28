# 📐 Architecture Board Exam (ALE) Mastery: The Area Metrics (AMBF, PSO, ISA, USA, TOSL, MACA)

_Module Focus: PD 1096 Rule VIII - Lot Occupancy and Open Space Equations_

---

## 🧠 The "Why It Matters" Scenario (Schema Activation)

Imagine you are designing a medium-density townhouse on a 1,000 sq.m inside lot in Quezon City. The client wants to pave the entire front and back yards for parking. As the architect, you must stop them. If you pave too much, you violate the **ISA (Impervious Surface Area)**. If your building is too wide, you violate the **PSO (Percentage of Site Occupancy)**.

The board exam will not just ask for definitions; it will test if you understand how these areas _interact_. If you increase the building footprint, the open space shrinks. This module trains you to see these metrics not as isolated numbers, but as a **single, interconnected puzzle**.

---

## 🏗️ Core Concepts (The "Equation Triangle")

To master this topic, you must stop thinking of these as six different rules and start seeing them as two main categories: **The Built** and **The Open**.

### Group 1: The Total Lot Breakdown

Every single square meter of your lot belongs to one of two categories.

- **TLA (Total Lot Area) = 100%**
- **TLA = PSO + TOSL**

**1. PSO (Percentage of Site Occupancy):** The percentage of the lot covered by the building itself.

- _The Area Equivalent:_ **AMBF (Allowable Maximum Building Footprint)**.
- _Formula:_ `AMBF = TLA x PSO`
- _Mental Hook:_ Imagine the AMBF as a solid **RED** block on the site plan.

**2. TOSL (Total Open Space within Lot):** The percentage of the lot NOT covered by the building.

- _Exam Trap Alert:_ TOSL is **NOT** just the front setback! It is the _sum_ of all setbacks, yards, and courts.
- _Formula:_ `TOSL = TLA - AMBF`

### Group 2: The Open Space Breakdown

Now, we take the TOSL (the open space) and divide it by what the rain can penetrate.

- **TOSL = ISA + USA**

**3. ISA (Impervious Surface Area):** The "Hardscape." Walkways, driveways, uncovered parking. Rain cannot soak through it.

- _Mental Hook:_ Color this **GRAY**.

**4. USA (Unpaved Surface Area):** The "Softscape." Lawns, gardens, exposed soil. Rain soaks naturally into the ground.

- _Mental Hook:_ Color this **GREEN**.

### Group 3: The Code Enforcement Metric

**5. MACA (Maximum Allowable Construction Area):** This is the total area of the lot that you are allowed to "disturb" with hard materials (both the building and the paving).

- _Formula:_ `MACA = PSO + ISA`
- _Ultimate Shortcut:_ `TLA = MACA + USA`

---

## 📊 The Hard Data Cheat Sheet (Table VIII.1)

_Data strictly based on the Revised IRR of PD 1096 (Table VIII.1). Examiners frequently test the "Basic R-2 Inside Lot" baseline._

| Zoning / Lot Type          | Max PSO (Red) | Max ISA (Gray) | Min USA (Green) | Min TOSL |
| :------------------------- | :------------ | :------------- | :-------------- | :------- |
| **Basic R-2 (Inside Lot)** | 60%           | 30%            | 10%             | 40%      |
| **Basic R-2 (Corner Lot)** | 70%           | 20%            | 10%             | 30%      |
| **Basic R-3 (Inside Lot)** | 70%           | 20%            | 10%             | 30%      |
| **Comm. C-2 (Inside Lot)** | 75%           | 20%            | 5%              | 25%      |

_Pattern Recognition (Chunking): Notice how `USA + ISA` ALWAYS equals `TOSL`, and `PSO + TOSL` ALWAYS equals `100%`._

---

## ⚠️ High-Yield Exam Traps (Von Restorff Effect)

- 🚨 **TRAP #1: The "TOSL = Front Setback" Hallucination.**
  - _Mistake:_ Thinking TOSL only refers to the front yard.
  - _Reality Check:_ TOSL means _Total_ Open Space. It includes the front, rear, sides, and any interior open courts.
- 🚨 **TRAP #2: Confusing MACA with AMBF.**
  - _Mistake:_ Thinking MACA is just the building footprint.
  - _Reality Check:_ MACA includes the building (PSO) **PLUS** all paved surfaces outside (ISA). `MACA = PSO + ISA`.
- 🚨 **TRAP #3: Mixing Percentages with Square Meters.**
  - _Mistake:_ Writing "PSO = 600 sq.m."
  - _Reality Check:_ PSO, ISA, USA, and TOSL are _Percentages_. AMBF is the physical _Area_ (sq.m). Read the exam question carefully to see if they are asking for the % or the sq.m.

---

## 🔄 Active Recall Challenge (Test Your Retention)

**Question:** An architect is designing a residential project on a 1,000 sq.m Basic R-2 inside lot. If the architect maximizes the building footprint (AMBF) and also maximizes the allowed paved driveways and walkways (ISA), what is the exact square meter area that MUST be dedicated strictly to soil, lawns, or planting (USA)?

A) 100 sq.m
B) 150 sq.m
C) 300 sq.m
D) 400 sq.m

<details>
  <summary><b>👉 Click here to reveal the answer and explanation</b></summary>
  <br>
  <b>Correct Answer: A) 100 sq.m</b><br><br>
  <b>Why?</b> <br>
  Step 1: Recall the Basic R-2 Inside Lot metrics from Table VIII.1 (PSO 60%, ISA 30%, USA 10%).<br>
  Step 2: The question asks for the USA in square meters.<br>
  Step 3: Calculate: 1,000 sq.m (TLA) x 10% (USA minimum) = 100 sq.m. <br><br>
  <i>Alternative shortcut using MACA:</i> MACA = 60% (PSO) + 30% (ISA) = 90%. Therefore, 10% of the lot must remain unpaved (USA). 10% of 1,000 = 100 sq.m.
</details>

---

## 📚 Verified Source Mapping

_If you need to verify these formulas and metrics in the code, look here:_

- **Rule VIII, Sec. 803:** Percentage of Site Occupancy (PSO)
- **Rule VIII, Table VIII.1:** Reference Table of Minimum TOSL Requirements by Lot Type/Location
- **Rule VIII, Sec. 804:** Sizes and Dimensions of Courts (Details on USA/ISA)
