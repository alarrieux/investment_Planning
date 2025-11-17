# Mathematical Formulations

This document provides detailed mathematical formulations for all optimization models in the Investment Planning package.

## Table of Contents

1. [Bank Loan Portfolio Optimization](#bank-loan-portfolio-optimization)
2. [Multi-Period Production-Inventory Model](#multi-period-production-inventory-model)
3. [Crude Oil Refining and Gasoline Blending](#crude-oil-refining-and-gasoline-blending)

---

## Bank Loan Portfolio Optimization

### Problem Description

A bank must allocate funds across multiple loan types to maximize net returns while satisfying business and regulatory constraints.

### Decision Variables

Let $x_i$ represent the amount (in dollars) allocated to loan type $i$:

- $x_1$ = Personal loans
- $x_2$ = Car loans
- $x_3$ = Home loans
- $x_4$ = Farm loans
- $x_5$ = Commercial loans

### Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| $r_i$ | Interest rate for loan type $i$ | 14%, 13%, 12%, 12.5%, 10% |
| $b_i$ | Bad debt ratio for loan type $i$ | 10%, 7%, 3%, 5%, 2% |
| $B$ | Total funds available | $12,000,000 |

### Objective Function

Maximize net return = Interest revenue - Bad debt losses

$$
\text{Maximize } Z = \sum_{i=1}^{5} [r_i(1-b_i) - b_i] x_i
$$

Expanded:
$$
\text{Maximize } Z = 0.026x_1 + 0.0509x_2 + 0.0864x_3 + 0.06875x_4 + 0.078x_5
$$

### Constraints

1. **Total funds constraint:**
   $$
   \sum_{i=1}^{5} x_i \leq B = 12,000,000
   $$

2. **Farm and commercial loans minimum (40% of total):**
   $$
   x_4 + x_5 \geq 0.4(x_1 + x_2 + x_3 + x_4 + x_5)
   $$

   Rearranged:
   $$
   0.4x_1 + 0.4x_2 + 0.4x_3 - 0.6x_4 - 0.6x_5 \leq 0
   $$

3. **Home loans minimum (50% of personal + car + home):**
   $$
   x_3 \geq 0.5(x_1 + x_2 + x_3)
   $$

   Rearranged:
   $$
   0.5x_1 + 0.5x_2 - 0.5x_3 \leq 0
   $$

4. **Bad debt limit (maximum 4% of total):**
   $$
   \sum_{i=1}^{5} b_i x_i \leq 0.04 \sum_{i=1}^{5} x_i
   $$

   Rearranged:
   $$
   0.06x_1 + 0.03x_2 - 0.01x_3 + 0.01x_4 - 0.02x_5 \leq 0
   $$

5. **Non-negativity:**
   $$
   x_i \geq 0, \quad i = 1, 2, 3, 4, 5
   $$

### Optimal Solution

The optimal allocation is:

- $x_1^* = 0$ (Personal loans)
- $x_2^* = 0$ (Car loans)
- $x_3^* = 7,200,000$ (Home loans)
- $x_4^* = 0$ (Farm loans)
- $x_5^* = 4,800,000$ (Commercial loans)

**Net Return:** $996,480
**ROI:** 8.34%

---

## Multi-Period Production-Inventory Model

### Problem Description

A manufacturer must determine production quantities over multiple periods to minimize total costs while meeting demand requirements.

### Decision Variables

For $t = 1, 2, \ldots, T$ periods:

- $x_t$ = Units produced in period $t$
- $I_t$ = Inventory level at end of period $t$

### Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| $c_t$ | Production cost per unit in period $t$ | $50, $45, $55, $48, $52, $50 |
| $h$ | Storage cost per unit per period | $8 |
| $d_t$ | Demand in period $t$ | 100, 250, 190, 140, 220, 110 |

### Objective Function

Minimize total production and storage costs:

$$
\text{Minimize } Z = \sum_{t=1}^{T} c_t x_t + \sum_{t=1}^{T} h I_t
$$

For $T = 6$:
$$
\text{Minimize } Z = 50x_1 + 45x_2 + 55x_3 + 48x_4 + 52x_5 + 50x_6 + 8(I_1 + I_2 + I_3 + I_4 + I_5 + I_6)
$$

### Constraints

**Inventory balance equations:**

Period 1:
$$
x_1 - I_1 = d_1
$$

Periods $t = 2, \ldots, T$:
$$
I_{t-1} + x_t - I_t = d_t
$$

**Non-negativity:**
$$
x_t, I_t \geq 0, \quad t = 1, 2, \ldots, T
$$

### Matrix Form

$$
\begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0
\end{bmatrix}
\begin{bmatrix}
x_1 \\ x_2 \\ x_3 \\ x_4 \\ x_5 \\ x_6 \\ I_1 \\ I_2 \\ I_3 \\ I_4 \\ I_5 \\ I_6
\end{bmatrix}
=
\begin{bmatrix}
100 \\ 250 \\ 190 \\ 140 \\ 220 \\ 110
\end{bmatrix}
$$

### Optimal Solution

| Period | Production | Inventory | Demand |
|--------|-----------|-----------|--------|
| 1 | 100 | 0 | 100 |
| 2 | 440 | 190 | 250 |
| 3 | 0 | 0 | 190 |
| 4 | 140 | 0 | 140 |
| 5 | 220 | 0 | 220 |
| 6 | 110 | 0 | 110 |

**Total Cost:** $49,980

---

## Crude Oil Refining and Gasoline Blending

### Problem Description

An oil refinery must determine the optimal production mix of gasoline products to maximize profit while satisfying capacity and quality constraints.

### Decision Variables

Let $x_{ij}$ represent barrels per day of gasoline type $j$ from source $i$:

**Sources:** $i \in \{f, c\}$ (feedstock, cracker)
**Products:** $j \in \{r, p, s\}$ (regular, premium, super)

- $x_{fr}$ = Regular gasoline from feedstock
- $x_{fp}$ = Premium gasoline from feedstock
- $x_{fs}$ = Super gasoline from feedstock
- $x_{cr}$ = Regular gasoline from cracker
- $x_{cp}$ = Premium gasoline from cracker
- $x_{cs}$ = Super gasoline from cracker

### Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| $C_{crude}$ | Crude oil capacity | 1,500,000 bbl/day |
| $C_{crack}$ | Cracker capacity | 200,000 bbl/day |
| $ON_f$ | Feedstock octane number | 82 |
| $ON_c$ | Cracker octane number | 98 |
| $ON_r$ | Regular octane requirement | 87 |
| $ON_p$ | Premium octane requirement | 89 |
| $ON_s$ | Super octane requirement | 92 |
| $D_r$ | Regular demand limit | 50,000 bbl/day |
| $D_p$ | Premium demand limit | 30,000 bbl/day |
| $D_s$ | Super demand limit | 40,000 bbl/day |
| $p_r$ | Regular profit margin | $6.70/bbl |
| $p_p$ | Premium profit margin | $7.20/bbl |
| $p_s$ | Super profit margin | $8.10/bbl |

### Objective Function

Maximize total profit:

$$
\text{Maximize } Z = \sum_{j \in \{r,p,s\}} p_j (x_{fj} + x_{cj})
$$

Expanded:
$$
\text{Maximize } Z = 6.70(x_{fr} + x_{cr}) + 7.20(x_{fp} + x_{cp}) + 8.10(x_{fs} + x_{cs})
$$

### Constraints

1. **Crude oil capacity:**
   $$
   5(x_{fr} + x_{fp} + x_{fs}) + 10(x_{cr} + x_{cp} + x_{cs}) \leq C_{crude}
   $$

2. **Cracker capacity:**
   $$
   2(x_{cr} + x_{cp} + x_{cs}) \leq C_{crack}
   $$

3. **Demand limits:**
   $$
   x_{fr} + x_{cr} \leq D_r
   $$
   $$
   x_{fp} + x_{cp} \leq D_p
   $$
   $$
   x_{fs} + x_{cs} \leq D_s
   $$

4. **Octane requirements:**

   Regular ($ON_r = 87$):
   $$
   82x_{fr} + 98x_{cr} \geq 87(x_{fr} + x_{cr})
   $$

   Rearranged:
   $$
   -5x_{fr} + 11x_{cr} \geq 0
   $$

   Premium ($ON_p = 89$):
   $$
   -7x_{fp} + 9x_{cp} \geq 0
   $$

   Super ($ON_s = 92$):
   $$
   -10x_{fs} + 6x_{cs} \geq 0
   $$

5. **Non-negativity:**
   $$
   x_{ij} \geq 0, \quad \forall i, j
   $$

### Optimal Solution

| Product | Feedstock | Cracker | Total |
|---------|-----------|---------|-------|
| Regular | 34,375 | 15,625 | 50,000 |
| Premium | 16,875 | 13,125 | 30,000 |
| Super | 15,000 | 25,000 | 40,000 |

**Daily Profit:** $875,000
**Annual Profit:** $319,375,000

---

## References

1. Taha, Hamdy A. *Operations Research: An Introduction*. 10th Edition. Pearson, 2017.
2. Winston, Wayne L. *Operations Research: Applications and Algorithms*. Brooks/Cole, 2003.
3. Hillier, F.S., and Lieberman, G.J. *Introduction to Operations Research*. McGraw-Hill, 2015.

---

*Last updated: 2024*
