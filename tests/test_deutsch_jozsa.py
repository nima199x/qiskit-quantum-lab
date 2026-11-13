import pytest

from algorithms.deutsch_jozsa import (
    balanced_oracle,
    build_dj_circuit,
    classify,
    constant_oracle,
)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
@pytest.mark.parametrize("value", [0, 1])
def test_constant_oracles(n, value):
    oracle = lambda qc, n_: constant_oracle(qc, n_, value)
    assert classify(n, oracle, seed=1) == "constant"


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_balanced_parity_oracle(n):
    assert classify(n, balanced_oracle, seed=1) == "balanced"


@pytest.mark.parametrize("n", [2, 3, 4])
def test_balanced_single_bit_and_flipped(n):
    single = lambda qc, n_: balanced_oracle(qc, n_, mask=0b1)
    flipped = lambda qc, n_: balanced_oracle(qc, n_, mask=0b1, flip=True)
    assert classify(n, single, seed=1) == "balanced"
    assert classify(n, flipped, seed=1) == "balanced"


def test_zero_mask_is_rejected():
    with pytest.raises(ValueError):
        balanced_oracle(build_dj_circuit(2, constant_oracle), 2, mask=0)


def test_invalid_n_is_rejected():
    with pytest.raises(ValueError):
        build_dj_circuit(0, constant_oracle)
