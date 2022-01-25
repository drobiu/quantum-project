import numpy as np
from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister

from src.logic.find_used_colours import find_used_colours
from src.logic.find_color_positions import FCP
from src.util.util import run_qc

secret_string = [0, 0, 1, 0]

# qc = find_used_colours(4, 4, secret_string)
#
# result = run_qc(qc)

colors = np.zeros(4)

for i in secret_string:
    colors[i] = 1

results = []

colors = list(colors)

if not np.array_equal(np.array(colors), np.ones_like(colors)):
    zero = colors.index(0)
    for i in range(4):
        if colors[i] == 0:
            results.append(np.zeros(4))
            continue
        qy = QuantumRegister(8, name='qy')
        y = QuantumRegister(4, name='y')
        s = QuantumRegister(3)
        c = ClassicalRegister(4)
        qc = QuantumCircuit(y, qy, s, c)

        qc = FCP(qc, y, qy, s, secret_string, c=i, d=zero)

        qc.measure(y[:], c[::-1])

        result = run_qc(qc, with_QI=False, verbose=False)

        curr_result = list(result.get_counts(qc).keys())
        assert len(curr_result) == 1

        results.append(list(map(int, str(curr_result[0]))))

result_string = np.zeros(4)

for i in range(4):
    for j, n in enumerate(results[i]):
        if n == 1:
            result_string[j] = i

print(result_string)
