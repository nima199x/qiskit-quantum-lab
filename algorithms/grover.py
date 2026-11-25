"""
Grover's search algorithm for one or more marked items among N = 2**n items.

The oracle flips the phase of every marked basis state, then the diffuser
reflects all amplitudes about their mean. With M marked items, each round
rotates the state by an angle 2*theta, where sin(theta) = sqrt(M / N), so
about (pi/4) * sqrt(N / M) rounds are best. Too many rounds make the
success probability go down again, so the iteration count matters.
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


def normalize_targets(n, target):
    """
    Accept one bitstring or an iterable of bitstrings and return a sorted
    list of unique, validated targets.
    """
    targets = [target] if isinstance(target, str) else list(target)
    if not targets:
        raise ValueError("at least one target is required")
    for t in targets:
        if not isinstance(t, str) or len(t) != n or set(t) - {"0", "1"}:
            raise ValueError(f"each target must be a bitstring of length {n}")
    unique = sorted(set(targets))
    if len(unique) == 2**n:
        raise ValueError("targets must not include every possible state")
    return unique


def optimal_iterations(n, num_targets=1):
    """
    Number of Grover iterations that maximizes the success probability
    sin^2((2k + 1) * theta), with sin(theta) = sqrt(num_targets / 2**n).

    Only the first peak is considered (later peaks need more iterations),
    and the smallest best k is returned. If half of all states are marked,
    no iterations are needed (0 and 1 give the same probability).
    """
    N = 2**n
    if not 1 <= num_targets < N:
        raise ValueError(f"num_targets must be between 1 and {N - 1}")

    theta = math.asin(math.sqrt(num_targets / N))
    best_k, best_p = 0, math.sin(theta) ** 2
    for k in range(1, math.ceil(math.pi / (4 * theta)) + 1):  # up to the first peak
        p = math.sin((2 * k + 1) * theta) ** 2
        if p > best_p + 1e-9:
            best_k, best_p = k, p
    return best_k


def build_grover_circuit(n, target, iterations=None):
    """
    Build Grover's circuit for an n-qubit search space.

    `target` is a bitstring like "101" or an iterable of bitstrings.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    targets = normalize_targets(n, target)
    if iterations is None:
        iterations = optimal_iterations(n, len(targets))

    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # uniform superposition over all 2**n states

    for _ in range(iterations):
        for t in targets:
            oracle(qc, n, t)
        diffuser(qc, n)

    qc.measure(range(n), range(n))
    return qc


def search(n, target, shots=1000, seed=None):
    """Run Grover's algorithm and return the most frequently measured bitstring."""
    qc = build_grover_circuit(n, target)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    return max(counts, key=counts.get)


def success_probability(n, target, shots=1000, seed=None):
    """Fraction of shots in which a marked state was measured."""
    targets = set(normalize_targets(n, target))
    qc = build_grover_circuit(n, target)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    return sum(c for key, c in counts.items() if key in targets) / shots


if __name__ == "__main__":
    n, targets = 3, ["101", "010"]
    qc = build_grover_circuit(n, targets)
    print(f"Searching for {targets} among {2**n} items "
          f"({optimal_iterations(n, len(targets))} iterations)")
    print(f"Success probability: {success_probability(n, targets):.3f}")
    run_circuit(qc, shots=1000)