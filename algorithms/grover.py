"""
Grover's search algorithm for one marked item among N = 2**n items.

The oracle flips the phase of the marked basis state, then the diffuser
reflects all amplitudes about their mean. Repeating this about
(pi/4) * sqrt(N) times makes the marked state very likely to be measured.
"""

import math

from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

from utils.runner import run_circuit


def _multi_controlled_z(qc, n):
    """Apply Z to qubit n-1 controlled on qubits 0..n-2 (phase flip of |1...1>)."""
    qc.h(n - 1)
    # MCXGate lets Qiskit pick the best synthesis; the old qc.mcx() helper
    # builds every implementation up front and triggers deprecation warnings.
    qc.append(MCXGate(n - 1), list(range(n)))  # controls 0..n-2, target n-1
    qc.h(n - 1)


def oracle(qc, n, target):
    """Flip the phase of the basis state `target` (a bitstring like "101")."""
    # Qiskit is little-endian: qubit i corresponds to target[n - 1 - i].
    zeros = [i for i in range(n) if target[n - 1 - i] == "0"]
    for i in zeros:
        qc.x(i)
    _multi_controlled_z(qc, n)
    for i in zeros:
        qc.x(i)


def diffuser(qc, n):
    """Inversion about the mean."""
    qc.h(range(n))
    qc.x(range(n))
    _multi_controlled_z(qc, n)
    qc.x(range(n))
    qc.h(range(n))


def optimal_iterations(n):
    """Number of Grover iterations for a single marked item among 2**n."""
    return max(1, math.floor(math.pi / 4 * math.sqrt(2**n)))


def build_grover_circuit(n, target, iterations=None):
    """Build Grover's circuit for an n-qubit search space and a bitstring target."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if len(target) != n or set(target) - {"0", "1"}:
        raise ValueError(f"target must be a bitstring of length {n}")
    if iterations is None:
        iterations = optimal_iterations(n)

    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # uniform superposition over all 2**n states

    for _ in range(iterations):
        oracle(qc, n, target)
        diffuser(qc, n)

    qc.measure(range(n), range(n))
    return qc


def search(n, target, shots=1000, seed=None):
    """Run Grover's algorithm and return the most frequently measured bitstring."""
    qc = build_grover_circuit(n, target)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    return max(counts, key=counts.get)


if __name__ == "__main__":
    n, target = 3, "101"
    qc = build_grover_circuit(n, target)
    print(f"Searching for {target} among {2**n} items "
          f"({optimal_iterations(n)} iterations)")
    run_circuit(qc, shots=1000)