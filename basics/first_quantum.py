from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Create a quantum circuit with 1 qubit and 1 classical bit to store the result
qc = QuantumCircuit(1, 1)

# 2. Apply a Hadamard gate to qubit 0 (creates superposition)
qc.h(0)

# 3. Measure qubit 0 and store the result in classical bit 0
qc.measure(0, 0)

# 4. Choose the simulator
simulator = AerSimulator()

# 5. Transpile the circuit for the simulator
compiled_circuit = transpile(qc, simulator)

# 6. Run the circuit on the simulator 1024 times (to see the probability distribution)
job = simulator.run(compiled_circuit, shots=1024)

# 7. Get the results
result = job.result()
counts = result.get_counts(qc)

# 8. Print the results (number of 0s and 1s)
print("Counts of 0 and 1:", counts)

# 9. (Optional) Display a histogram of the results
plot_histogram(counts)
plt.show()