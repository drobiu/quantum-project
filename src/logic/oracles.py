from itertools import combinations

import numpy as np
import sys

from qiskit.circuit.library import QFT

from src.arithmetic.increment import control_increment

sys.path.extend("../")
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from scipy.special import binom

from src.logic.s_gate import s_gate
from src.arithmetic.counter import count
from src.util.util import run_qc


def oracle_a(circuit, q, a, s,do_inverse=False):
    """
    circuit:    the circuit to which to append the oracle.
    q:          quantum registers, color inputs.
    a:          quantum registers, count of correct colors at correct places.
    s:          array of integer. The input of s_gate, which represents the secret string.
    """
    circuit = circuit.compose(s_gate(s).to_gate(label="s"), qubits=q)
    if not do_inverse:
     circuit = count(circuit, a, q, step=2)

    if do_inverse:
     circuit=count(circuit,a,q,amount=-1,step=2)

    circuit = circuit.compose(s_gate(s).to_gate(label="s"), qubits=q)

    return circuit


def c_gate(k, length=4):
    s = np.ones(length) * k

    return s_gate(s, length / 2)


def oracle_b(circuit, q, b, s):
    q_l = len(q)
    b_l = len(b)
    n = len(s)
    log_k = q_l / n

    circuit = circuit.compose(QFT(num_qubits=b_l, approximation_degree=0, do_swaps=True,
                                  inverse=True, insert_barriers=True, name='qft'), qubits=b)

    # Hardcoded for now
    n_colors = 4

    color_count = [s.count(i) for i in range(n_colors)]

    for color, c_n in enumerate(color_count):
        if c_n == 0:
            continue

        contrib = [1] + (c_n - 1) * [0]

        for i in range(c_n + 1, n_colors + 1):
            curr_cont = c_n
            for j in range(1, i):
                curr_cont -= binom(i, j) * contrib[j - 1]
            contrib.append(curr_cont)

        circuit = circuit.compose(c_gate(color))

        print(color, c_n, contrib)

        circuit = count(circuit, b, q, step=2, apply_QFT=False)

        for i in range(c_n, n):
            comp = contrib[i]

            if comp == 0:
                continue

            # Heavily inspired by
            # https://github.com/TimVroomans/Quantum-Mastermind/blob/master/src/mastermind/game/algorithms/Mastermind_Oracle.py

            for combination in list(combinations(range(n), i + 1)):
                qubit_combinations = [q[int(log_k * color): int(log_k * (color + 1))] for color in combination]

                temp_qubits = []
                for qb in qubit_combinations:
                    temp_qubits += qb

                circuit = control_increment(circuit, b, temp_qubits, amount=comp, apply_QFT=False)
        circuit = circuit.compose(c_gate(color))

    circuit = circuit.compose(QFT(num_qubits=b_l, approximation_degree=0, do_swaps=True,
                                  inverse=True, insert_barriers=True, name='iqft'), qubits=b)

    return circuit


def test():
    q = QuantumRegister(8)
    b = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q, b, c)

    # 01, 11, 11, 11

    qc.x(q[0])
    qc.x(q[2:8])
    qc.barrier()

    # [0, 0, 0, 1] = 11, 11, 11, 10

    qc = oracle_b(qc, q, b, [0, 0, 0, 1])

    # Should equal 110
    qc.measure(b[:], c[:])

    run_qc(qc, with_QI=False)
    qc.draw(output="text")


if __name__ == "__main__":
    test()
