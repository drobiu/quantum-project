import os
import sys

from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from Rui.query import query_cd
from src.logic.oracles import oracle_a

sys.path.extend('../')


def FCP(circuit, y_register, qy_register, s_register, secret_string):
    # init
    # q1 = QuantumRegister(num_position, "q1")
    # q2 = QuantumRegister(num_bits_color * num_position)
    # out = QuantumRegister(num_bits_color + 1, "o")

    # step 1: apply H gate
    circuit.h(range(len(y_register)))

    # step 2: query
    circuit = circuit.compose(query_cd(), range(12))

    # step 3: ask oracle
    circuit = oracle_a(circuit, qy_register, s_register, secret_string)

    # step 4: apply Z to LSB
    circuit.z(s_register[0])

    # step 5: undo step 2 and 3
    circuit = circuit.compose(query_cd(), range(12))
    circuit = oracle_a(circuit, qy_register, s_register, secret_string, do_inverse=True)

    # step 6: apply H gate
    circuit.h(range(len(y_register)))

    return circuit


if __name__ == "__main__":
    print(FCP(4, 2, [0, 1, 2, 3]).draw(output="text"))
