"""
Shor's algorithm, demonstrated by factoring N = 15.

Factoring N reduces to finding the period r of f(x) = a^x mod N:
  * Quantum part: phase estimation (see qpe.py) on the operator
    U|y> = |a*y mod N>. Its eigenphases are s/r, so the measured phase
    reveals r.
  * Classical part: turn the measured phase into r with continued
    fractions, then take gcd(a^(r/2) +- 1, N).

For N = 15, multiplication by a modulo 15 is just a few (controlled) swaps
and X gates on 4 qubits, so the circuit stays small. Every period divides 4,
so 4 counting qubits give exact phases.
"""

from fractions import Fraction
from math import gcd

from qiskit import QuantumCircuit

from algorithms.qft import qft_circuit
from utils.runner import run_circuit

N = 15
SUPPORTED_A = (2, 4, 7, 8, 11, 13, 14)  # residues coprime to 15 (except 1)


def controlled_mult_mod15(qc, control, work, a):
    """
    Apply |y> -> |a*y mod 15> to the 4 qubits `work` if `control` is 1.

    Multiplying by 2 rotates the 4 bits left, by 8 rotates them right and by
    4 rotates by two. Multiplying by -1 flips every bit (15 - y = ~y), which
    gives 7 = -8, 11 = -4, 13 = -2 and 14 = -1.
    """
    a %= N
    if a == 1:
        return
    if a not in SUPPORTED_A:
        raise ValueError(f"a must be one of {SUPPORTED_A} (or 1)")

    if a in (2, 13):
        qc.cswap(control, work[2], work[3])
        qc.cswap(control, work[1], work[2])
        qc.cswap(control, work[0], work[1])
    if a in (7, 8):
        qc.cswap(control, work[0], work[1])
        qc.cswap(control, work[1], work[2])
        qc.cswap(control, work[2], work[3])
    if a in (4, 11):
        qc.cswap(control, work[1], work[3])
        qc.cswap(control, work[0], work[2])
    if a in (7, 11, 13, 14):
        for q in work:
            qc.cx(control, q)


def build_period_finding_circuit(a, n_count=4):
    """Phase estimation of U|y> = |a*y mod 15> starting from |1>."""
    if a not in SUPPORTED_A:
        raise ValueError(f"a must be one of {SUPPORTED_A}")

    work = list(range(n_count, n_count + 4))
    qc = QuantumCircuit(n_count + 4, n_count)

    qc.x(work[0])  # work register starts in |1>
    qc.h(range(n_count))
    qc.barrier()

    for j in range(n_count):
        # Counting qubit j controls U^(2**j), i.e. multiplication by a^(2**j)
        controlled_mult_mod15(qc, j, work, pow(a, 2**j, N))
    qc.barrier()

    qc.compose(qft_circuit(n_count, inverse=True), qubits=range(n_count), inplace=True)
    qc.measure(range(n_count), range(n_count))
    return qc


def find_period(a, counts, n_count=4, n=N):
    """
    Classical post-processing: recover the period r from measured phases.

    Each outcome m gives a phase m / 2**n_count ~ s/r. Continued fractions
    give a candidate denominator d (a divisor of r); we then try its
    multiples until a^r = 1 (mod n). Outcome 0 carries no information.
    """
    for key, _ in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
        m = int(key, 2)
        if m == 0:
            continue
        d = Fraction(m, 2**n_count).limit_denominator(n).denominator
        if d == 1:
            continue
        for k in range(1, n + 1):
            r = d * k
            if pow(a, r, n) == 1:
                return r
    return None


def factors_from_period(a, r, n=N):
    """Return a nontrivial factor pair of n from the period r, or None."""
    if r is None or r % 2:
        return None
    x = pow(a, r // 2, n)
    if x == n - 1:  # a^(r/2) = -1 (mod n): this choice of a fails
        return None
    candidates = {gcd(x - 1, n), gcd(x + 1, n)} - {1, n}
    if not candidates:
        return None
    p = min(candidates)
    return tuple(sorted((p, n // p)))


def shor_factor(a, n_count=4, shots=1000, seed=None):
    """
    Try to factor 15 with base a. Returns (period, factors); factors is
    None if this a does not work (e.g. a = 14 has an odd "half period").
    """
    if not 2 <= a < N:
        raise ValueError(f"a must be in [2, {N - 1}]")

    g = gcd(a, N)
    if g > 1:  # lucky guess: a already shares a factor with 15
        return None, tuple(sorted((g, N // g)))

    qc = build_period_finding_circuit(a, n_count)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    r = find_period(a, counts, n_count)
    return r, factors_from_period(a, r)


if __name__ == "__main__":
    print(build_period_finding_circuit(7).draw(fold=120))
    for a in SUPPORTED_A:
        r, factors = shor_factor(a)
        print(f"a = {a:2d}: period = {r}, factors = {factors}")
    run_circuit(build_period_finding_circuit(7), shots=1000)
