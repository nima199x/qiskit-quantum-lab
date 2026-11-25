import pytest

from algorithms.grover import (
    build_grover_circuit,
    normalize_targets,
    optimal_iterations,
    search,
    success_probability,
)


# --- single target ---------------------------------------------------------

@pytest.mark.parametrize("target", ["00", "01", "10", "11"])
def test_two_qubits_finds_target(target):
    assert search(2, target, seed=1) == target


@pytest.mark.parametrize("target", [format(i, "03b") for i in range(8)])
def test_three_qubits_finds_every_target(target):
    assert search(3, target, seed=1) == target


def test_four_qubits_finds_target():
    assert search(4, "1011", seed=1) == "1011"


def test_optimal_iterations_single_target():
    assert optimal_iterations(2) == 1
    assert optimal_iterations(3) == 2
    assert optimal_iterations(4) == 3


# --- several targets -------------------------------------------------------

def test_optimal_iterations_several_targets():
    assert optimal_iterations(3, 2) == 1
    assert optimal_iterations(3, 3) == 1
    assert optimal_iterations(4, 4) == 1
    assert optimal_iterations(2, 2) == 0  # half of all states: nothing to gain


@pytest.mark.parametrize(
    "targets", [("000", "111"), ("010", "101"), ("001", "110")]
)
def test_two_targets_in_three_qubits_are_found_perfectly(targets):
    assert success_probability(3, targets, shots=500, seed=1) == 1.0


def test_four_targets_in_four_qubits_are_found_perfectly():
    targets = ["0000", "0101", "1010", "1111"]
    assert success_probability(4, targets, shots=500, seed=1) == 1.0


def test_three_targets_in_three_qubits():
    targets = ["001", "010", "111"]
    assert success_probability(3, targets, shots=2000, seed=1) > 0.75


def test_half_of_states_marked_is_a_coin_flip():
    p = success_probability(2, ["00", "11"], shots=2000, seed=1)
    assert 0.4 < p < 0.6


def test_search_returns_one_of_the_targets():
    assert search(3, ["010", "101"], seed=1) in {"010", "101"}


def test_duplicate_targets_are_collapsed():
    assert normalize_targets(3, ["101", "101"]) == ["101"]
    assert success_probability(3, ["101", "101"], shots=2000, seed=1) > 0.9


# --- invalid input ---------------------------------------------------------

@pytest.mark.parametrize("n, target", [(1, "1"), (3, "10"), (3, "1a1")])
def test_invalid_input_rejected(n, target):
    with pytest.raises(ValueError):
        build_grover_circuit(n, target)


@pytest.mark.parametrize(
    "target",
    [[], ["101", "10"], ["00", "01", "10", "11"]],
)
def test_invalid_target_lists_rejected(target):
    n = 2 if target and len(target[0]) == 2 else 3
    with pytest.raises(ValueError):
        build_grover_circuit(n, target)


@pytest.mark.parametrize("m", [0, 4, 5])
def test_invalid_number_of_targets_rejected(m):
    with pytest.raises(ValueError):
        optimal_iterations(2, m)