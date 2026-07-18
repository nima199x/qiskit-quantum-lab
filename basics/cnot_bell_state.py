from qiskit import QuantumCircuit
from utils.runner import run_circuit

# Create a Bell state (entangled qubits)
qc = QuantumCircuit(2, 2)
qc.h(0)          # Put qubit 0 into superposition
qc.cx(0, 1)       # CNOT: entangle qubit 0 (control) with qubit 1 (target)
qc.measure([0, 1], [0, 1])

run_circuit(qc, shots=1000)