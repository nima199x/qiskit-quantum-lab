from qiskit import QuantumCircuit

from utils.runner import run_circuit


def build_superposition_circuit():
    """One qubit in superposition (Hadamard), then measured."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # creates superposition
    qc.measure(0, 0)
    return qc


if __name__ == "__main__":
    run_circuit(build_superposition_circuit(), shots=1024)
