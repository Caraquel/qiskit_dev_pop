# 🚀 Shor's Algorithm in Practice --- From Simulator to IBM Quantum Hardware

## Author

**DokectIS**\
*Data Engineer · Qiskit Developer · Quantum Algorithms Practitioner*

------------------------------------------------------------------------

## 📌 Overview

This project presents a **full, end-to-end implementation of Shor's
Algorithm**, developed and executed using **Qiskit**.\
Unlike simplified demos, this work focuses on **realistic execution
paths**, progressing from classical analysis and simulation to
**execution on real IBM Quantum hardware**, while explicitly addressing
the limitations of current NISQ devices.

The notebook demonstrates not only *how* Shor's algorithm works, but
also *why* certain design choices are required in practice.

------------------------------------------------------------------------

## 🧠 What This Project Demonstrates

✔️ Clear separation of **classical** and **quantum** components\
✔️ Construction of a **quantum order-finding subroutine** using
**Quantum Phase Estimation (QPE)**\
✔️ Practical implementation of **modular multiplication as a unitary
operator**\
✔️ Interpretation of quantum measurements using **continued fractions**\
✔️ Execution on **IBM Quantum hardware** using **SamplerV2 (job mode)**\
✔️ Debugging and adapting to **real hardware constraints** (noise,
depth, plan limits)

------------------------------------------------------------------------

## 🧩 Algorithmic Flow

1.  **Problem Definition**\
    Factor a composite integer (N) using Shor's algorithm.

2.  **Classical Pre-processing**

    -   Choose coprime integer (a)\
    -   Handle trivial factors using `gcd`

3.  **Quantum Subroutine (Order Finding)**

    -   Prepare phase and work registers\
    -   Apply controlled modular exponentiation\
    -   Use **Inverse QFT** to extract periodicity

4.  **Measurement & Post-processing**

    -   Convert measured phase → rational approximation\
    -   Recover order (r) via continued fractions\
    -   Validate using modular arithmetic

5.  **Factor Recovery**

    -   Compute `gcd(a^(r/2) ± 1, N)`\
    -   Extract non-trivial factors

------------------------------------------------------------------------

## 🧪 Experimental Setup

### Simulation

-   **Backend**: `AerSimulator`\
-   **Purpose**: Validate algorithmic correctness\
-   **Outcome**: Reliable recovery of order and correct factorization

### IBM Quantum Hardware

-   **Execution Mode**: `SamplerV2` (Job Mode --- Open Plan compatible)\
-   **Backends**: Dynamically selected via `least_busy`\
-   **Constraints Addressed**:
    -   Limited qubit count\
    -   Circuit depth and noise\
    -   No session access in Open Plan\
-   **Outcome**: Observable periodic structure and successful recovery
    of the order in selected runs

------------------------------------------------------------------------

## 📊 Results (N = 15)

  Parameter                Value
  ------------------------ ------------------------------
  Composite Number         15
  Coprime (a)              2 (also tested: 7, 11, 13)
  True Order (r)           4
  Factors Recovered        (3, 5)
  Execution Environments   Aer Simulator & IBM Hardware

------------------------------------------------------------------------

## ⚠️ Important Design Decisions

-   **Compiled modular multiplication (permutation unitaries)** was used
    to ensure clarity and correctness over scalability.
-   This approach is **intentionally non-scalable**, highlighting the
    gap between theoretical algorithms and practical NISQ execution.
-   Circuit parameters (`t`, shots, optimization level) were tuned
    dynamically to balance **precision vs hardware survivability**.

------------------------------------------------------------------------

## 🧑‍💻 Skills & Technologies Demonstrated

-   **Quantum Algorithms**: Shor, QPE, iQFT\
-   **Qiskit**: Circuit construction, transpilation, Aer, Runtime
    primitives\
-   **IBM Quantum Platform**: Backend selection, job execution, result
    parsing\
-   **Classical Post-Processing**: Number theory, continued fractions,
    validation logic\
-   **Engineering Practice**: Debugging, performance trade-offs,
    reproducibility

------------------------------------------------------------------------

## 📂 Repository Structure

    ├── notebooks/
    │   ├── shor_simulator.ipynb
    │   └── shor_ibm_hardware.ipynb
    ├── utils/
    │   ├── classical_postprocess.py
    │   └── order_recovery.py
    └── README.md

------------------------------------------------------------------------

## 🎯 Why This Project Matters

Most Shor demonstrations stop at toy examples or hide critical steps.\
This project explicitly exposes:

-   Where **quantum advantage actually comes from**
-   Why **hardware noise dominates current performance**
-   How to **adapt algorithms to real quantum systems**

It reflects a **practitioner's mindset**, not just academic familiarity.

------------------------------------------------------------------------

## 🔮 Next Directions

-   Iterative / semiclassical phase estimation\
-   Hardware-optimized reversible modular arithmetic\
-   Comparative analysis with Grover's algorithm\
-   Scaling studies using noise models

------------------------------------------------------------------------

## 📬 Contact

If you're interested in **quantum algorithm engineering**, **hybrid
quantum-classical workflows**, or **Qiskit development**, feel free to
connect.
