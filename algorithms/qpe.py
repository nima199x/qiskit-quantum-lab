"""
Quantum Phase Estimation (QPE).

Given a unitary U and an eigenstate |psi> with U|psi> = exp(2*pi*i*phi)|psi>,
QPE estimates the phase phi in [0, 1) using t "counting" qubits:

  1. Put the counting qubits in uniform superposition.
  2. Counting qubit j controls U^(2**j) (phase kickback writes phi into
     the counting register's phases).
  3. The inverse QFT turns those phases into the binary digits of phi.

If phi is an exact t-bit fraction (k / 2**t) the result is deterministic;
otherwise the best t-bit approximation is measured with probability >= 4/pi^2.

Here U is a phase gate P(2*pi*phi) acting on |1>, so the true phase is known
and the result is easy to verify.
"""

import math

from qiskit import QuantumCircuit

from algorithms.qft import qft_circuit
from utils.runner import run_circuit


def build_qpe_circuit(phi, t):
    """Build the QPE circuit with t counting qubits for U = P(2*pi*phi)."""
    if t < 1:
        raise ValueError("t must be at least 1")
    if not 0 <= phi < 1:
        raise ValueError("phi must be in [0, 1)")

    qc = QuantumCircuit(t + 1, t)
    target = t

    qc.x(target)  # eigenstate |1> of the phase gate
    qc.h(range(t))
    qc.barrier()

    for j in range(t):
        # Controlled-U^(2**j): a controlled phase of 2*pi*phi*2**j
        qc.cp(2 * math.pi * phi * 2**j, j, target)
    qc.barrier()

    qc.compose(qft_circuit(t, inverse=True), qubits=range(t), inplace=True)
    qc.measure(range(t), range(t))
    return qc


def estimate_phase(phi, t, shots=1000, seed=None):
    """Return (estimated phase, counts). The estimate is m / 2**t."""
    qc = build_qpe_circuit(phi, t)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    m = int(max(counts, key=counts.get), 2)
    return m / 2**t, counts


if __name__ == "__main__":
    # The T gate has eigenvalue exp(i*pi/4) = exp(2*pi*i * 1/8) on |1>.
    phi, t = 1 / 8, 3
    print(build_qpe_circuit(phi, t).draw())
    estimate, _ = estimate_phase(phi, t)
    print(f"T gate: true phase {phi}, estimated {estimate}")

    # A phase that is not an exact t-bit fraction: a peak near 1/3 with spread.
    phi, t = 1 / 3, 5
    estimate, _ = estimate_phase(phi, t)
    print(f"phi = 1/3 with {t} qubits: estimated {estimate} (true {phi:.4f})")
    run_circuit(build_qpe_circuit(phi, t), shots=1000)
