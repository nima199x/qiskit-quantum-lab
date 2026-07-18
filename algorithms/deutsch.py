from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# تابع متغیر: f(x) = x (می‌خوایم تست کنیم)
def oracle_balanced(qc):
    qc.cx(0, 1)  # CNOT: پیاده‌سازی f(x) = x

# تابع ثابت: f(x) = 0
def oracle_constant(qc):
    pass  # هیچ کاری نمی‌کنیم → همیشه خروجی 0

# ساخت مدار Deutsch
qc = QuantumCircuit(2, 1)

# حالت اولیه
qc.x(1)         # حالت |1⟩ برای qubit دوم
qc.h(0)
qc.h(1)

# انتخاب اوراکل (oracle)
oracle_constant(qc)   # ← اینو می‌تونی تغییر بدی به oracle_constant

# ادامه مدار Deutsch
qc.h(0)
qc.measure(0, 0)

# اجرای مدار
simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1000).result()
counts = result.get_counts()

print("Result:", counts)
plot_histogram(counts)
plt.show()