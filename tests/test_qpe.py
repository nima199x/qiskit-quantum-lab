import pytest

from algorithms.qpe import build_qpe_circuit, estimate_phase


@pytest.mark.parametrize("phi, t", [(0.0, 3), (0.25, 3), (0.625, 3), (1 / 8, 3), (11 / 16, 4)])
def test_exact_phase_is_found_deterministically(phi, t):
    estimate, counts = estimate_phase(phi, t, shots=200, seed=1)
    assert estimate == phi
    assert len(counts) == 1  # a single outcome, no spread


@pytest.mark.parametrize("t", [4, 5, 6])
def test_inexact_phase_is_within_one_step(t):
    phi = 1 / 3
    estimate, _ = estimate_phase(phi, t, shots=1000, seed=1)
    assert abs(estimate - phi) <= 1 / 2**t


def test_more_counting_qubits_give_better_precision():
    phi = 1 / 3
    coarse, _ = estimate_phase(phi, 3, shots=1000, seed=1)
    fine, _ = estimate_phase(phi, 6, shots=1000, seed=1)
    assert abs(fine - phi) < abs(coarse - phi)


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        build_qpe_circuit(0.5, 0)
    with pytest.raises(ValueError):
        build_qpe_circuit(1.0, 3)
    with pytest.raises(ValueError):
        build_qpe_circuit(-0.1, 3)
