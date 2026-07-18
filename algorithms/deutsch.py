from qiskit import QuantumCircuit
from utils.runner import run_circuit


def oracle_balanced(qc):
    """Balanced function: f(x) = x, implemented via CNOT."""
    qc.cx(0, 1)


def oracle_constant(qc):
    """Constant function: f(x) = 0 (do nothing)."""
    pass


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

run_circuit(qc, shots=1000)