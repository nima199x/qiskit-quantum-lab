import numpy as np
import pytest
from qiskit.quantum_info import Operator

from algorithms.qft import build_frequency_circuit, detect_frequency, qft_circuit


def dft_matrix(n):
    N = 2**n
    x, y = np.meshgrid(np.arange(N), np.arange(N))
    return np.exp(2j * np.pi * x * y / N) / np.sqrt(N)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_qft_matches_dft_matrix(n):
    assert np.allclose(Operator(qft_circuit(n)).data, dft_matrix(n))


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_inverse_qft_undoes_qft(n):
    qc = qft_circuit(n)
    qc.compose(qft_circuit(n, inverse=True), inplace=True)
    assert np.allclose(Operator(qc).data, np.eye(2**n))


@pytest.mark.parametrize("k", range(8))
def test_detect_frequency_three_qubits(k):
    assert detect_frequency(3, k, seed=1) == k


@pytest.mark.parametrize("k", [0, 1, 7, 12, 15])
def test_detect_frequency_four_qubits(k):
    assert detect_frequency(4, k, seed=1) == k


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        qft_circuit(0)
    with pytest.raises(ValueError):
        build_frequency_circuit(3, 8)
