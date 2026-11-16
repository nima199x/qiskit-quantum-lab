"""
Quantum Fourier Transform (QFT).

On n qubits the QFT maps the basis state |k> to
    (1 / sqrt(N)) * sum_y exp(2*pi*i*k*y / N) |y>,   N = 2**n,
which is the discrete Fourier transform acting on the amplitudes.

Demo: a state whose phase "oscillates" with frequency k is turned back into
the basis state |k> by the inverse QFT, so measuring reveals k.
"""

import math

from qiskit import QuantumCircuit

from utils.runner import run_circuit


def qft_circuit(n, do_swaps=True, inverse=False):
    """Build the n-qubit QFT (or its inverse) as a circuit."""
    if n < 1:
        raise ValueError("n must be at least 1")

    qc = QuantumCircuit(n, name="QFT")
    for j in reversed(range(n)):
        qc.h(j)
        for k in range(j):
            # Controlled phase rotation by pi / 2**(j - k)
            qc.cp(math.pi / 2 ** (j - k), k, j)
    if do_swaps:
        for i in range(n // 2):
            qc.swap(i, n - 1 - i)

    return qc.inverse() if inverse else qc


def build_frequency_circuit(n, k):
    """
    Prepare the state (1/sqrt(N)) * sum_x exp(2*pi*i*k*x/N) |x>, apply the
    inverse QFT and measure. The outcome is k with certainty.
    """
    if not 0 <= k < 2**n:
        raise ValueError(f"k must be in [0, {2**n - 1}]")

    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    # exp(2*pi*i*k*x/N) factors into one phase per qubit (x = sum x_i * 2**i)
    for i in range(n):
        qc.p(2 * math.pi * k * 2**i / 2**n, i)
    qc.barrier()
    qc.compose(qft_circuit(n, inverse=True), inplace=True)
    qc.measure(range(n), range(n))
    return qc


def detect_frequency(n, k, shots=100, seed=None):
    """Return the frequency k recovered by the inverse QFT."""
    qc = build_frequency_circuit(n, k)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    return int(max(counts, key=counts.get), 2)


if __name__ == "__main__":
    n, k = 3, 5
    print(qft_circuit(n).draw())
    qc = build_frequency_circuit(n, k)
    print(f"Hidden frequency: {k} -> measured: {detect_frequency(n, k)}")
    run_circuit(qc, shots=1000)
