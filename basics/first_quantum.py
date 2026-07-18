from qiskit import QuantumCircuit
from utils.runner import run_circuit

# 1. Create a quantum circuit with 1 qubit and 1 classical bit to store the result
qc = QuantumCircuit(1, 1)

# 2. Apply a Hadamard gate to qubit 0 (creates superposition)
qc.h(0)

# 3. Measure qubit 0 and store the result in classical bit 0
qc.measure(0, 0)

# 4. Run the circuit and display results
run_circuit(qc, shots=1024)