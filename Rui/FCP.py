import os
import sys

from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from Rui.query import query_cd
from src.logic.oracles import oracle_a

sys.path.extend('../')


def FCP(num_position, num_bits_color, secret_string):
    # init
    q1 = QuantumRegister(num_position, "q1")
    q2 = QuantumRegister(num_bits_color * num_position)
    out = QuantumRegister(num_bits_color + 1, "o")
    qc = QuantumCircuit(q1, q2, out)

    # step 1: apply H gate
    qc.h(range(num_position))

    # step 2: query
    qc = qc.compose(query_cd(), range(12))

    # step 3: ask oracle
    # TODO: fix oracle

    qc = oracle_a(qc, q2, out, secret_string)

    # step 4: apply Z to LSB
    qc.z(out[0])

    # step 5: undo step 2 and 3
    qc = qc.compose(query_cd(), range(12))
    qc = oracle_a(qc, q2, out, secret_string, do_inverse=True)

    # step 6: apply H gate
    qc.h(range(num_position))

    return qc


if __name__ == "__main__":
    print(FCP(4, 2, [0, 1, 2, 3]).draw(output="text"))
