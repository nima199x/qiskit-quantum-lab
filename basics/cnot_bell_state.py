from qiskit import QuantumCircuit

from utils.runner import run_circuit


def build_bell_circuit():
    """Bell state (entangled qubits): H on qubit 0, then CNOT(0 -> 1)."""
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Put qubit 0 into superposition
    qc.cx(0, 1)  # CNOT: entangle qubit 0 (control) with qubit 1 (target)
    qc.measure([0, 1], [0, 1])
    return qc


if __name__ == "__main__":
    run_circuit(build_bell_circuit(), shots=1000)
