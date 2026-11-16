import math

import pytest

from algorithms.teleportation import teleport

STATES = [
    (0.0, 0.0),
    (math.pi, 0.0),
    (math.pi / 2, 0.0),
    (math.pi / 3, math.pi / 4),
    (2.1, 5.0),
]


@pytest.mark.parametrize("theta, phi", STATES)
def test_teleportation_is_perfect(theta, phi):
    fidelity, _ = teleport(theta, phi, shots=500, seed=1)
    assert fidelity == 1.0


def test_all_four_measurement_outcomes_occur():
    _, counts = teleport(math.pi / 3, math.pi / 4, shots=2000, seed=1)
    # key format: "out crx crz" -> look at the two classical message bits
    messages = {tuple(key.split()[1:]) for key in counts}
    assert len(messages) == 4


def test_without_corrections_fidelity_is_about_half():
    fidelity, _ = teleport(
        math.pi / 3, math.pi / 4, shots=4000, seed=1, apply_corrections=False
    )
    assert 0.4 < fidelity < 0.6
