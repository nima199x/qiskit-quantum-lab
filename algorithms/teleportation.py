"""
Quantum teleportation: send the state of one qubit (Alice's) to another
qubit (Bob's) using an entangled pair and two classical bits.

Qubits:  q0 = state to send, q1 = Alice's half of the Bell pair,
         q2 = Bob's half of the Bell pair (receives the state).

Steps:
  1. Prepare an arbitrary state on q0.
  2. Share a Bell pair between q1 and q2.
  3. Alice does a Bell-basis measurement on q0 and q1 -> two classical bits.
  4. Bob fixes his qubit: X if the q1 bit is 1, Z if the q0 bit is 1.
  5. Check: undo the state preparation on q2 and measure. If the state
     arrived intact, the result is always 0.
"""

import math

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from utils.runner import run_circuit


def build_teleportation_circuit(theta, phi, apply_corrections=True):
    """
    Build the teleportation circuit for the state
    cos(theta/2)|0> + e^(i*phi) sin(theta/2)|1>.

    Set apply_corrections=False to see what happens without Bob's
    classically controlled X/Z fixes (a useful negative control).
    """
    q = QuantumRegister(3, "q")
    crz = ClassicalRegister(1, "crz")  # Alice's q0 result -> Z correction
    crx = ClassicalRegister(1, "crx")  # Alice's q1 result -> X correction
    out = ClassicalRegister(1, "out")  # verification result on Bob's qubit
    qc = QuantumCircuit(q, crz, crx, out)

    # 1. State to teleport
    qc.ry(theta, 0)
    qc.p(phi, 0)
    qc.barrier()

    # 2. Bell pair between Alice (q1) and Bob (q2)
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # 3. Alice's Bell measurement
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, crz[0])
    qc.measure(1, crx[0])
    qc.barrier()

    # 4. Bob's corrections, controlled by the classical bits
    if apply_corrections:
        with qc.if_test((crx, 1)):
            qc.x(2)
        with qc.if_test((crz, 1)):
            qc.z(2)
    qc.barrier()

    # 5. Verification: undo the preparation on Bob's qubit
    qc.p(-phi, 2)
    qc.ry(-theta, 2)
    qc.measure(2, out[0])
    return qc


def teleport(theta, phi, shots=1000, seed=None, apply_corrections=True):
    """
    Run teleportation and return (fidelity, counts).

    fidelity is the fraction of shots where Bob's qubit matched the state
    Alice sent (1.0 means perfect teleportation).
    """
    qc = build_teleportation_circuit(theta, phi, apply_corrections)
    counts = run_circuit(qc, shots=shots, show_plot=False, seed=seed)
    # Keys look like "out crx crz"; the leftmost bit is the verification bit.
    ok = sum(c for key, c in counts.items() if key.replace(" ", "")[0] == "0")
    return ok / shots, counts


if __name__ == "__main__":
    theta, phi = math.pi / 3, math.pi / 4
    qc = build_teleportation_circuit(theta, phi)
    print(qc.draw())
    fidelity, _ = teleport(theta, phi)
    print(f"Fidelity with corrections: {fidelity:.3f}")
    fidelity, _ = teleport(theta, phi, apply_corrections=False)
    print(f"Fidelity without corrections: {fidelity:.3f} (expected ~0.5)")
    run_circuit(qc, shots=1000)
