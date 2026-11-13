from qiskit import QuantumCircuit

from utils.runner import run_circuit


def oracle_balanced(qc):
    """Balanced function: f(x) = x, implemented via CNOT."""
    qc.cx(0, 1)


def oracle_constant(qc):
    """Constant function: f(x) = 0 (do nothing)."""
    pass


def build_deutsch_circuit(oracle):
    """Build the Deutsch circuit for the given oracle function."""
    qc = QuantumCircuit(2, 1)

    # Initial state
    qc.x(1)  # Set qubit 1 to |1>
    qc.h(0)
    qc.h(1)

    # Oracle
    oracle(qc)

    # Interference + measurement
    qc.h(0)
    qc.measure(0, 0)
    return qc


def classify(oracle, shots=100, seed=None):
    """
    Run Deutsch's algorithm and return "constant" or "balanced".

    Measuring 0 means constant, measuring 1 means balanced. The outcome is
    deterministic, so every shot should agree.
    """
    qc = build_deutsch_circuit(oracle)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    return "constant" if counts.get("0", 0) == shots else "balanced"


if __name__ == "__main__":
    for oracle in (oracle_constant, oracle_balanced):
        qc = build_deutsch_circuit(oracle)
        print(f"--- {oracle.__name__} ---")
        counts = run_circuit(qc, shots=1000)
        print("Verdict:", classify(oracle))
