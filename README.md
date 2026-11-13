# Qiskit Quantum Lab

[![CI](https://github.com/nima199x/qiskit-quantum-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/nima199x/qiskit-quantum-lab/actions/workflows/ci.yml)

A hands-on learning project exploring quantum computing concepts and algorithms using [Qiskit](https://www.ibm.com/quantum/qiskit) and its Aer simulator.

This repository is a work in progress, growing week by week as I learn and implement new quantum computing concepts.

## Project Structure

```
qiskit-quantum-lab/
├── basics/               # Foundational examples (superposition, entanglement, gates)
│   ├── first_quantum.py
│   └── cnot_bell_state.py
├── algorithms/           # Quantum algorithms
│   ├── deutsch.py
│   └── deutsch_jozsa.py
├── exercises/            # Practice exercises
│   ├── exam1.py
│   └── exam2.py
├── utils/                # Shared helper functions
│   └── runner.py
├── tests/                # pytest test suite
├── .github/workflows/    # GitHub Actions CI
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## What's Implemented

| File | Concept | Description |
|---|---|---|
| `basics/first_quantum.py` | Superposition | Applies a Hadamard gate to a single qubit and measures the resulting 50/50 distribution. |
| `basics/cnot_bell_state.py` | Entanglement | Builds a Bell state using H + CNOT, producing correlated `00`/`11` outcomes. |
| `algorithms/deutsch.py` | Deutsch's Algorithm | Determines whether a function is constant or balanced using a single circuit evaluation. |
| `algorithms/deutsch_jozsa.py` | Deutsch-Jozsa Algorithm | Generalizes Deutsch to n input qubits, with constant and balanced oracles. |
| `exercises/exam1.py` | Circuit inspection | Builds a simple circuit and prints its structure without running it. |
| `exercises/exam2.py` | Superposition | Basic single-qubit measurement exercise. |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nima199x/qiskit-quantum-lab.git
cd qiskit-quantum-lab
```

### 2. Set up a virtual environment

```bash
python -m venv q_env
q_env\Scripts\activate      # Windows
source q_env/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt        # to run the examples
pip install -r requirements-dev.txt    # to also run the tests
```

### 4. Run an example

Run scripts as modules from the project root, since they import from `utils/`:

```bash
python -m basics.first_quantum
python -m basics.cnot_bell_state
python -m algorithms.deutsch
python -m algorithms.deutsch_jozsa
python -m exercises.exam2
```

### 5. Run the tests

```bash
pytest
```

`run_circuit(..., seed=...)` makes simulator runs reproducible, and tests pass `show_plot=False` so they run without opening any windows. The same tests run automatically on every push and pull request via GitHub Actions (Python 3.10-3.12).

## Roadmap

- [x] Set up project structure and shared utilities
- [x] Basic gates and superposition
- [x] Entanglement (Bell state)
- [x] Deutsch's Algorithm
- [x] Deutsch-Jozsa Algorithm (generalized to n qubits)
- [x] Unit tests with pytest
- [x] GitHub Actions for automated testing
- [ ] Grover's Algorithm
- [ ] Quantum Teleportation
- [ ] Quantum Fourier Transform / Shor's Algorithm (stretch goal)

## License

This project is for personal learning purposes.
