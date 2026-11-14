import pytest

from algorithms.grover import build_grover_circuit, optimal_iterations, search


@pytest.mark.parametrize("target", ["00", "01", "10", "11"])
def test_two_qubits_finds_target(target):
    assert search(2, target, seed=1) == target


@pytest.mark.parametrize("target", [format(i, "03b") for i in range(8)])
def test_three_qubits_finds_every_target(target):
    assert search(3, target, seed=1) == target


def test_four_qubits_finds_target():
    assert search(4, "1011", seed=1) == "1011"


def test_optimal_iterations():
    assert optimal_iterations(2) == 1
    assert optimal_iterations(3) == 2
    assert optimal_iterations(4) == 3


@pytest.mark.parametrize("n, target", [(1, "1"), (3, "10"), (3, "1a1")])
def test_invalid_input_rejected(n, target):
    with pytest.raises(ValueError):
        build_grover_circuit(n, target)
