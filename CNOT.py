from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


qc= QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.measure([0,1],[0,1])

simulator= AerSimulator()

compiled_circuit= transpile(qc, simulator)

result = simulator.run(compiled_circuit, shots=1000).result()

counts = result.get_counts()
print("Result:", counts)
plot_histogram(counts)
plt.show()



