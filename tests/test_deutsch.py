from algorithms.deutsch import classify, oracle_balanced, oracle_constant


def test_constant_oracle_detected():
    assert classify(oracle_constant, seed=1) == "constant"


def test_balanced_oracle_detected():
    assert classify(oracle_balanced, seed=1) == "balanced"
