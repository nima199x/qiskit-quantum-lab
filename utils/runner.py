"""
Shared utility functions for running Qiskit circuits and displaying results.
"""

from qiskit.compiler import transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def run_circuit(qc, shots=1000, show_plot=True, save_path=None):
    """
    Transpile and run a quantum circuit on the AerSimulator, then print
    and optionally display/save a histogram of the results.

    Args:
        qc: The QuantumCircuit to run.
        shots (int): Number of times to run the circuit. Default 1000.
        show_plot (bool): Whether to display the histogram window. Default True.
        save_path (str): If provided, save the histogram to this file path
                          instead of (or in addition to) showing it.

    Returns:
        dict: The measurement counts.
    """
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)

    result = simulator.run(compiled_circuit, shots=shots).result()
    counts = result.get_counts()

    print("Result:", counts)

    if save_path or show_plot:
        plot_histogram(counts)
        if save_path:
            plt.savefig(save_path)
        if show_plot:
            plt.show()
        plt.close()

    return counts