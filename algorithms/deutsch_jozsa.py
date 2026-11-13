"""
Deutsch-Jozsa algorithm: Deutsch's algorithm generalized to n input qubits.

Given a function f: {0,1}^n -> {0,1} that is promised to be either constant
or balanced, decide which one with a single oracle call. Measuring all input
qubits gives 00...0 if f is constant, and anything else if f is balanced.
"""

from qiskit import QuantumCircuit

from utils.runner import run_circuit


def constant_oracle(qc, n, value=0):
    """Constant function: f(x) = value. Input qubits are 0..n-1, ancilla is n."""
    if value:
        qc.x(n)


def balanced_oracle(qc, n, mask=None, flip=False):
    """
    Balanced function: f(x) = (mask . x) mod 2, optionally negated.

    Each set bit in `mask` adds a CNOT from that input qubit to the ancilla.
    The mask must be non-zero, otherwise the function would be constant.
    By default every input qubit is used (mask = 2**n - 1).
    """
    if mask is None:
        mask = (1 << n) - 1
    if mask == 0:
        raise ValueError("mask must be non-zero for a balanced oracle")
    for i in range(n):
        if (mask >> i) & 1:
            qc.cx(i, n)
    if flip:
        qc.x(n)


def build_dj_circuit(n, oracle):
    """
    Build the Deutsch-Jozsa circuit.

    Args:
        n (int): Number of input qubits (n >= 1).
        oracle: Callable oracle(qc, n) that adds the oracle gates.
    """
    if n < 1:
        raise ValueError("n must be at least 1")

    qc = QuantumCircuit(n + 1, n)

    # Ancilla in |1>, then Hadamard everything
    qc.x(n)
    qc.h(range(n + 1))
    qc.barrier()

    oracle(qc, n)
    qc.barrier()

    # Interference + measurement of the input register
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def classify(n, oracle, shots=100, seed=None):
    """Return "constant" or "balanced" for the given oracle."""
    qc = build_dj_circuit(n, oracle)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    return "constant" if counts.get("0" * n, 0) == shots else "balanced"


if __name__ == "__main__":
    n = 3
    oracles = {
        "constant f(x)=0": lambda qc, n: constant_oracle(qc, n, 0),
        "constant f(x)=1": lambda qc, n: constant_oracle(qc, n, 1),
        "balanced (parity of all bits)": balanced_oracle,
        "balanced (only bit 0)": lambda qc, n: balanced_oracle(qc, n, mask=0b001),
    }
    for name, oracle in oracles.items():
        print(f"--- {name} ---")
        print("Verdict:", classify(n, oracle))
