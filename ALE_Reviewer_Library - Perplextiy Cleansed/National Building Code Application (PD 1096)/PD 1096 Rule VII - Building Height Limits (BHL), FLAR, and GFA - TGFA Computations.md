# 🏢 Architecture Board Exam (ALE) Mastery: BHL, FLAR, & Area Computations

_Module Focus: Rule VII - Decoded and Demystified_

---

## 🧠 The "Why It Matters" Scenario (Schema Activation)

Visualize this: You are the lead architect for a high-density office tower in a CBD. The client wants to maximize their profit by building as high and wide as possible. Your job is to thread the needle between **Building Height Limit (BHL)**, **Floor to Lot Area Ratio (FLAR)**, **Gross Floor Area (GFA)**, and **Total Gross Floor Area (TGFA)**.

If you mess up the FLAR, the building loses saleable space. If you confuse TGFA with building volume, the project fails compliance. The board exam tests exactly this: your ability to know which metric controls the _footprint_, which controls the _density_, and which controls the _vertical limit_.

---

## 🏗️ Core Concepts (The Foundation)

### 1. Building Height Limit (BHL)

- **Definition:** The absolute maximum vertical distance allowed for a building, based on its occupancy and zoning.
- **The Reality Check:** BHL is usually measured from the highest adjoining sidewalk or ground surface to the highest roof point.
- **Exemptions (Do not add to BHL):** Antennas, domes, specific roof structures, and fire walls (if within code limits).

### 2. Floor to Lot Area Ratio (FLAR)

- **Definition:** The multiplier that dictates the **maximum allowable GFA** based on the size of your lot. It restricts the _density_ of the building, not necessarily the height.
- **The Formula:** `GFA = Total Lot Area (TLA) x FLAR`
- **Mental Hook:** _FLAR is your area budget. BHL is your height ceiling._

### 3. Gross Floor Area (GFA)

- **Definition:** The total enclosed, habitable floor space of a building.
- **The "Exam Trap" Exclusions:** GFA _strictly excludes_ covered parking, purely outdoor roof decks, utility shafts, and fire escape structures.

### 4. Total Gross Floor Area (TGFA)

- **Definition:** The grand total of ALL floor areas within the building.
- **The Formula:** `TGFA = GFA + Non-GFA (Parking, balconies, utility rooms, etc.)`
- **CRITICAL ALERT:** TGFA is an **AREA** (measured in sq.m), _not_ a volume! Do not multiply Area by Height to get TGFA.

---

## 📊 The Hard Data Cheat Sheet (Table VII.1 & VII.2)

_Data strictly based on the Revised IRR of PD 1096. Examiners love testing these exact brackets._

| Occupancy Group     | Description         | FLAR Range (Table VII.1) | BHL Max Limit (Table VII.2)              |
| :------------------ | :------------------ | :----------------------- | :--------------------------------------- |
| **Residential R-1** | Basic Single-Family | 1.50 (Max)               | 10.00 meters (3 storeys)                 |
| **Residential R-5** | Very High Density   | 6.00 to 9.00             | 54.00 meters (18 storeys)                |
| **Commercial C-2**  | Medium Intensity    | 3.60 to 9.00             | 36.00 meters (12 storeys)                |
| **Commercial C-3**  | Metropolitan / CBD  | 9.00 to 34.00            | 60.00 to 180.00+ meters (20-60+ storeys) |

---

## ⚠️ High-Yield Exam Traps (Von Restorff Effect)

Your brain naturally seeks shortcuts. Break these bad habits before exam day:

- 🚨 **TRAP #1: Confusing Area with Volume.**
  - _Mistake:_ Using `AMBF x BHL` to find TGFA.
  - _Reality Check:_ Area $\times$ Height = Volume (Cubic Meters). This calculates the **Building Bulk**, NOT the TGFA (Square Meters).
- 🚨 **TRAP #2: The "C-3 FLAR" Hallucination.**
  - _Mistake:_ Assuming C-3 FLAR caps at 9.0.
  - _Reality Check:_ C-3 (Metropolitan Commercial) allows massive density. The FLAR range is **9.00 to 34.00**, allowing up to 60 storeys.
- 🚨 **TRAP #3: Adding Parking to GFA.**
  - _Mistake:_ Calculating the GFA and including the 3 levels of basement parking.
  - _Reality Check:_ Off-street parking is explicitly excluded from GFA. It is, however, included in the _TGFA_.

---

## 🔄 Active Recall Challenge (Test Your Retention)

**Question:** You are designing a Commercial C-2 building on a 1,000 sq.m lot. The local zoning ordinance enforces a maximum FLAR of 4.0. If your proposed design has a total GFA of 5,000 sq.m, what is the regulatory status of your design?

A) It complies, as long as the building is under 36.00 meters (12 storeys).
B) It complies, because 5,000 sq.m is within the standard C-2 code limits.
C) It violates the code because the maximum allowable GFA is 4,000 sq.m.
D) It violates the code because GFA must include parking spaces.

<details>
  <summary><b>👉 Click here to reveal the answer and explanation</b></summary>
  <br>
  <b>Correct Answer: C</b><br><br>
  <b>Why?</b> Step 1: Recall the formula `GFA = TLA x FLAR`. <br>
  Step 2: Calculate the limit: 1,000 sq.m (TLA) x 4.0 (FLAR) = 4,000 sq.m (Maximum Allowable GFA).<br>
  Step 3: Compare. Your design proposes 5,000 sq.m, which exceeds the allowable GFA limit set by the FLAR. Even if the height is fine, the floor area density is illegally high.
</details>

---

## 📚 Verified Source Mapping

- **Rule VII, Sec. 704:** Location on Property
- **Rule VII, Table VII.1:** Allowable Maximum TGFA Based on Allowed Percentage of Site Occupancy (PSO) - _This is where FLAR is dictated._
- **Rule VII, Table VII.2:** Building Height Limit (BHL) by Type of Use or Occupancy
