import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from algorithms.shor import (
    SUPPORTED_A,
    build_period_finding_circuit,
    controlled_mult_mod15,
    factors_from_period,
    find_period,
    shor_factor,
)


def order_mod15(a):
    r = 1
    while pow(a, r, 15) != 1:
        r += 1
    return r


def work_value(qc):
    """Value of the 4 work qubits (qubits 1-4) of a deterministic circuit."""
    probs = Statevector(qc).probabilities_dict()
    assert len(probs) == 1
    key = next(iter(probs))  # little-endian: leftmost char is qubit 4
    return int(key[:4], 2)


@pytest.mark.parametrize("a", SUPPORTED_A)
def test_controlled_multiplication_is_correct(a):
    for y in range(15):
        for control_on in (True, False):
            qc = QuantumCircuit(5)
            if control_on:
                qc.x(0)
            for bit in range(4):
                if (y >> bit) & 1:
                    qc.x(1 + bit)
            controlled_mult_mod15(qc, 0, [1, 2, 3, 4], a)
            expected = (a * y) % 15 if control_on else y
            assert work_value(qc) == expected


@pytest.mark.parametrize("a", SUPPORTED_A)
def test_period_is_found(a):
    r, _ = shor_factor(a, seed=1)
    assert r == order_mod15(a)


@pytest.mark.parametrize("a", [2, 4, 7, 8, 11, 13])
def test_factors_of_15_are_found(a):
    _, factors = shor_factor(a, seed=1)
    assert factors == (3, 5)


def test_unlucky_base_gives_no_factors():
    # 14 = -1 (mod 15): period 2, but 14^1 = -1 so the method fails
    r, factors = shor_factor(14, seed=1)
    assert r == 2
    assert factors is None


def test_base_sharing_a_factor_is_a_classical_shortcut():
    assert shor_factor(3) == (None, (3, 5))
    assert shor_factor(10) == (None, (3, 5))


def test_find_period_from_counts():
    counts = {"0000": 250, "0100": 250, "1000": 250, "1100": 250}
    assert find_period(7, counts) == 4
    assert find_period(4, {"0000": 500, "1000": 500}) == 2
    # Only the zero outcome: no information
    assert find_period(7, {"0000": 1000}) is None


def test_factors_from_period():
    assert factors_from_period(7, 4) == (3, 5)
    assert factors_from_period(11, 2) == (3, 5)
    assert factors_from_period(7, 3) is None  # odd period
    assert factors_from_period(14, 2) is None  # a^(r/2) = -1
    assert factors_from_period(7, None) is None


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        build_period_finding_circuit(5)
    with pytest.raises(ValueError):
        shor_factor(1)
    with pytest.raises(ValueError):
        shor_factor(15)
