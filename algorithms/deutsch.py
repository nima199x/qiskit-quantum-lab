from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Balanced function: f(x) = x
def oracle_balanced(qc):
    qc.cx(0, 1)  # CNOT implements f(x) = x

# Constant function: f(x) = 0
def oracle_constant(qc):
    pass  # Do nothing -> output is always 0

# Build the Deutsch circuit
qc = QuantumCircuit(2, 1)

# Initial state
qc.x(1)          # Set qubit 1 to |1>
qc.h(0)
qc.h(1)

# Choose the oracle
oracle_constant(qc)   # <- switch to oracle_balanced to test the other case

# Rest of the Deutsch circuit
qc.h(0)
qc.measure(0, 0)

# Run the circuit
simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1000).result()
counts = result.get_counts()

print("Result:", counts)
plot_histogram(counts)
plt.show()