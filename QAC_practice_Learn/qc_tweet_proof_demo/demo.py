#!/usr/bin/env python3
"""Quantum Tweet‑Proof Demo (Qiskit)

Includes:
  1) Hello Quantum World (H |0> -> ~50/50)
  2) Quantum 1+1=2 via reversible half‑adder (XOR with CNOT, AND with Toffoli)
  3) Full verification for all 4 input pairs (00,01,10,11)

Outputs:
  - Circuit PNGs
  - Histogram PNGs
  - Combined “share cards” (circuit + histogram + caption) PNGs

Notes:
  - This demo does NOT claim quantum advantage.
  - Simulator only by default (hardware noise is a separate step).

Usage:
  python demo.py --shots 4096 --out outputs
  python demo.py --only hello
  python demo.py --only adder --a 1 --b 1
  python demo.py --only test
  python demo.py --thread

Requirements:
  pip install qiskit matplotlib pillow pandas
"""

import argparse
from pathlib import Path

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


def hello_quantum_world():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def quantum_half_adder(a: int, b: int):
    """Reversible half adder.
    q0=A, q1=B, q2=SUM, q3=CARRY.
    Measures SUM -> c0, CARRY -> c1.
    Output bitstring is 'CARRY SUM' (Qiskit count ordering).
    """
    qc = QuantumCircuit(4, 2)

    if a == 1:
        qc.x(0)
    if b == 1:
        qc.x(1)

    # SUM = A XOR B  (write into q2)
    qc.cx(0, 2)
    qc.cx(1, 2)

    # CARRY = A AND B (write into q3)
    qc.ccx(0, 1, 3)

    qc.measure(2, 0)  # SUM
    qc.measure(3, 1)  # CARRY
    return qc


def run_counts(qc: QuantumCircuit, shots: int):
    backend = Aer.get_backend("qasm_simulator")
    result = execute(qc, backend, shots=shots).result()
    return result.get_counts()


def save_circuit_png(qc: QuantumCircuit, path: Path):
    fig = qc.draw(output="mpl")
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_hist_png(counts: dict, path: Path, title: str):
    fig = plot_histogram(counts)
    plt.title(title)
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def make_share_card(circuit_png: Path, hist_png: Path, caption: str, out_path: Path):
    """Combine circuit + histogram into a single tweet‑friendly image."""
    circ = Image.open(circuit_png).convert("RGB")
    hist = Image.open(hist_png).convert("RGB")

    target_w = max(circ.width, hist.width)

    def pad_to_width(img, w):
        if img.width == w:
            return img
        padded = Image.new("RGB", (w, img.height), "white")
        padded.paste(img, ((w - img.width) // 2, 0))
        return padded

    circ = pad_to_width(circ, target_w)
    hist = pad_to_width(hist, target_w)

    cap_h = 120
    card = Image.new("RGB", (target_w, circ.height + hist.height + cap_h), "white")
    draw = ImageDraw.Draw(card)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
        font_b = ImageFont.truetype("DejaVuSans.ttf", 32)
    except Exception:
        font = ImageFont.load_default()
        font_b = font

    y = 0
    card.paste(circ, (0, y)); y += circ.height
    card.paste(hist, (0, y)); y += hist.height

    draw.rectangle([0, y, target_w, y + cap_h], fill=(245, 245, 245))

    wrap = []
    line = ""
    for word in caption.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=font) <= target_w - 40:
            line = test
        else:
            wrap.append(line)
            line = word
    if line:
        wrap.append(line)
    wrap = wrap[:3]

    ty = y + 18
    for i, ln in enumerate(wrap):
        draw.text((20, ty), ln, fill="black", font=(font_b if i == 0 else font))
        ty += 34

    card.save(out_path)


def do_hello(shots: int, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    qc = hello_quantum_world()
    counts = run_counts(qc, shots)

    circ_path = out_dir / "hello_circuit.png"
    hist_path = out_dir / "hello_hist.png"
    card_path = out_dir / "hello_share_card.png"

    save_circuit_png(qc, circ_path)
    save_hist_png(counts, hist_path, f"Hello Quantum World (shots={shots})")
    make_share_card(circ_path, hist_path,
                    "Hello Quantum World: apply H to |0> → ~50/50 on measurement.",
                    card_path)
    return counts, circ_path, hist_path, card_path


def do_adder(a: int, b: int, shots: int, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    qc = quantum_half_adder(a, b)
    counts = run_counts(qc, shots)

    circ_path = out_dir / f"adder_A{a}_B{b}_circuit.png"
    hist_path = out_dir / f"adder_A{a}_B{b}_hist.png"
    card_path = out_dir / f"adder_A{a}_B{b}_share_card.png"

    save_circuit_png(qc, circ_path)
    save_hist_png(counts, hist_path, f"Half Adder A={a}, B={b} (shots={shots})")
    make_share_card(circ_path, hist_path,
                    f"Quantum half‑adder: A={a}, B={b} → output bitstring (CARRY SUM).",
                    card_path)
    return counts, circ_path, hist_path, card_path


def do_test(shots: int, out_dir: Path):
    expected = {
        (0, 0): "00",
        (0, 1): "01",
        (1, 0): "01",
        (1, 1): "10",
    }

    summary = []
    for a in [0, 1]:
        for b in [0, 1]:
            qc = quantum_half_adder(a, b)
            counts = run_counts(qc, shots)
            best = max(counts, key=counts.get)
            exp = expected[(a, b)]
            passed = (best == exp)
            summary.append((a, b, best, exp, passed, counts))

    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / "test_report.txt"
    with report.open("w", encoding="utf-8") as f:
        f.write(f"Half‑Adder Full Verification (shots={shots})\n\n")
        for a, b, best, exp, passed, counts in summary:
            f.write(f"A={a} B={b}  best={best}  expected={exp}  PASS={passed}  counts={counts}\n")
    return summary, report


def print_tweet_thread():
    tweets = [
        "Classic computing started with ‘Hello World’ and ‘1+1=2’. Here’s the Quantum Computing equivalent using Qiskit: (1) Hello Quantum World (superposition) (2) Quantum 1+1=2 (reversible half‑adder). Verified with many shots.",
        "Hello Quantum World: apply a Hadamard (H) to |0⟩ to create superposition, then measure. Expected ≈50/50 distribution across many shots.",
        "Quantum 1+1=2: implement a reversible half‑adder. SUM = XOR (CNOT). CARRY = AND (Toffoli/CCX). For A=1,B=1 → (CARRY,SUM)=10₂ → 2₁₀.",
        "Anti ‘hardcoded demo’: verify all 4 inputs (00,01,10,11) match expected outputs. Counts confirm deterministic behavior in the simulator.",
        "Note: This does not claim quantum advantage. It’s a baseline correctness + behavior demo. Hardware noise is a separate step.",
    ]
    for i, t in enumerate(tweets, 1):
        print(f"\n--- Tweet {i} ---\n{t}\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--shots", type=int, default=4096, help="Number of shots (repetitions)")
    p.add_argument("--out", type=str, default="outputs", help="Output folder")
    p.add_argument("--only", type=str, default="all", choices=["all", "hello", "adder", "test"], help="Run only one part")
    p.add_argument("--a", type=int, default=1, help="Input A for half adder (0/1)")
    p.add_argument("--b", type=int, default=1, help="Input B for half adder (0/1)")
    p.add_argument("--thread", action="store_true", help="Print tweet-ready thread text")
    args = p.parse_args()

    out_dir = Path(args.out)

    if args.thread:
        print_tweet_thread()

    if args.only in ("all", "hello"):
        counts, circ, hist, card = do_hello(args.shots, out_dir)
        print("\n[Hello Quantum World]\nCounts:", counts)
        print("Saved:", circ, hist, card)

    if args.only in ("all", "adder"):
        counts, circ, hist, card = do_adder(args.a, args.b, args.shots, out_dir)
        print(f"\n[Half Adder A={args.a} B={args.b}]\nCounts:", counts)
        print("Saved:", circ, hist, card)

    if args.only in ("all", "test"):
        summary, report = do_test(args.shots, out_dir)
        print("\n[Full Verification Test]")
        for a, b, best, exp, passed, counts in summary:
            print(f"A={a} B={b} best={best} expected={exp} PASS={passed} counts={counts}")
        print("Saved report:", report)


if __name__ == "__main__":
    main()
