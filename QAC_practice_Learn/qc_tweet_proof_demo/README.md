# Quantum Tweet‑Proof Demo (Qiskit)

This mini-project contains two baseline Quantum Computing demos designed to be **shareable** and **debunk‑resistant**:

1) **Hello Quantum World** — create a superposition using an `H` gate and verify a ~50/50 distribution with many shots.  
2) **Quantum 1 + 1 = 2** — implement a **reversible half‑adder** with quantum gates (**CNOT** for XOR, **Toffoli/CCX** for AND), and verify all 4 inputs.

✅ **Framing:** This does **not** claim quantum advantage.  
It demonstrates correctness + basic quantum behavior using standard quantum primitives.  
Hardware noise is a separate step (add later).

---

## Quick start (VS Code + Codex)

1. Create a virtual environment (optional):
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows PowerShell
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run everything and generate share images:
```bash
python demo.py --shots 4096 --out outputs --thread
```

4. Open the `outputs/` folder for:
- circuit PNGs
- histogram PNGs
- combined **share cards** (circuit + histogram + caption) PNGs

---

## Commands

Run all:
```bash
python demo.py --shots 4096 --out outputs
```

Only hello:
```bash
python demo.py --only hello
```

Only adder for a specific input:
```bash
python demo.py --only adder --a 1 --b 1
```

Only full verification test:
```bash
python demo.py --only test
```

Print tweet-ready thread:
```bash
python demo.py --thread
```

---

## What to post on X/Twitter

Post these images:
- `outputs/hello_share_card.png`
- `outputs/adder_A1_B1_share_card.png`

And screenshot this:
- `outputs/test_report.txt`

Then paste the thread printed by:
```bash
python demo.py --thread
```


### Plotting note
This project saves histograms via the Figure returned by `plot_histogram()` to avoid blank images in some VS Code/Jupyter environments.
