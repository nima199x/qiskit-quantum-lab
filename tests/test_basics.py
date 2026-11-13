from basics.cnot_bell_state import build_bell_circuit
from basics.first_quantum import build_superposition_circuit
from utils.runner import run_circuit

SHOTS = 2000


def test_superposition_is_roughly_fifty_fifty():
    counts = run_circuit(
        build_superposition_circuit(), shots=SHOTS, show_plot=False, seed=42
    )
    assert set(counts) <= {"0", "1"}
    assert sum(counts.values()) == SHOTS
    # 50/50 within a generous tolerance (seeded, so stable)
    assert abs(counts.get("0", 0) - SHOTS / 2) < 0.1 * SHOTS


def test_bell_state_only_correlated_outcomes():
    counts = run_circuit(build_bell_circuit(), shots=SHOTS, show_plot=False, seed=42)
    assert set(counts) <= {"00", "11"}
    assert sum(counts.values()) == SHOTS


def test_seed_makes_runs_reproducible():
    qc = build_superposition_circuit()
    a = run_circuit(qc, shots=500, show_plot=False, seed=7)
    b = run_circuit(qc, shots=500, show_plot=False, seed=7)
    assert a == b
