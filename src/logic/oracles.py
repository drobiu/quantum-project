import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import QFT
from scipy.special import binom

from Rui.sgate.sgate import sgate
from src.artihmetic.counter import count
from src.util.util import run_qc


def oracle_a(circuit, q, a, s):
    circuit = circuit.compose(sgate(s).to_gate(label="s"), qubits=a)

    circuit = count(circuit, q, a, step=2)

    circuit = circuit.compose(sgate(s).to_gate(label="s"), qubits=a)

    return circuit


def c_gate(k, length=4):
    s = np.ones(length) * k

    return sgate(s, length/2)


def oracle_b(circuit, q, b, s):
    q_l = len(q)

    # circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
    #                               inverse=True, insert_barriers=True, name='qft'))
    #
    #
    #
    # circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
    #                               inverse=True, insert_barriers=True, name='iqft'))

    # Hardcoded for now
    n_colors = 4

    color_count = [s.count(i) for i in range(n_colors)]

    for color, c_n in enumerate(color_count):
        if c_n == 0:
            continue

        contrib = []
        contrib[0] = 1

        for i in range(q_l):
            if 0 < i < n_colors:
                contrib[i] = 0
            else:
                curr_cont = c_n - i
                for j in range(c_n, i-1):
                    curr_cont -= binom(i, j) * contrib[j]

        circuit = circuit.compose(c_gate(color))

        circuit = count(circuit, q, b, step=2)

        for i in range(c_n, q_l):
            # add combinations
            comp = contrib[i]





def test():
    q = QuantumRegister(8)
    a = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q, a, c)

    qc.x(a[0])
    qc.x(q[:])

    qc = oracle_a(qc, q, a, [0, 1, 0, 0])

    # Should equal 110
    qc.measure(a[:], c[:])

    run_qc(qc)
    qc.draw(output="mpl")


if __name__ == "__main__":
    test()