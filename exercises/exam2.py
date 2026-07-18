from qiskit import QuantumCircuit
from utils.runner import run_circuit

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

run_circuit(qc, shots=1000)