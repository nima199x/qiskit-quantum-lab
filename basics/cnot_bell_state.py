from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a Bell state (entangled qubits)
qc = QuantumCircuit(2, 2)
qc.h(0)          # Put qubit 0 into superposition
qc.cx(0, 1)       # CNOT: entangle qubit 0 (control) with qubit 1 (target)
qc.measure([0, 1], [0, 1])

simulator = AerSimulator()

compiled_circuit = transpile(qc, simulator)

result = simulator.run(compiled_circuit, shots=1000).result()

counts = result.get_counts()
print("Result:", counts)
plot_histogram(counts)
plt.show()