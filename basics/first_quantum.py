from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer # تغییر این خط
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. ساخت مدار کوانتومی با 1 کیوبیت و 1 بیت کلاسیک برای ذخیره نتیجه
qc = QuantumCircuit(1, 1)

# 2. اعمال گیت هادامارد روی کیوبیت 0 (اولین کیوبیت)
qc.h(0) 

# 3. اندازه‌گیری کیوبیت 0 و ذخیره نتیجه در بیت کلاسیک 0
qc.measure(0, 0)

# 4. انتخاب شبیه‌ساز (قوی‌ترین شبیه‌ساز کوانتومی)
simulator = Aer.get_backend('qasm_simulator')

# 5. آماده‌سازی مدار برای اجرا روی شبیه‌ساز
compiled_circuit = transpile(qc, simulator)

# 6. اجرای مدار روی شبیه‌ساز 1024 بار (برای دیدن احتمالات)
job = simulator.run(compiled_circuit, shots=1024)

# 7. گرفتن نتایج
result = job.result()
counts = result.get_counts(qc)

# 8. نمایش نتایج (تعداد دفعات 0 و 1)
print("\ number of result 0 , 1 :", counts) 

# 9. (اختیاری) نمایش هیستوگرام نتایج
plot_histogram(counts)
plt.show()