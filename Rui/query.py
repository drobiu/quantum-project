import math
import numpy as np
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.library.basis_change import QFT
from quantuminspire.qiskit import QI
from getpass import getpass
from coreapi.auth import TokenAuthentication
from qiskit import BasicAer, execute


def query(numarray=[0, 1, 2, 3], num_state_array=2):
    num_bits = len(numarray) * num_state_array
    i = len(numarray)
    ind = 0
    c = QuantumRegister(i, "c")
    q = QuantumRegister(num_bits, "q")
    qc = QuantumCircuit(c, q)
    for x in numarray:
        if num_state_array == 3:
            if x < 4:
                qc.cx(ind, i)
            i += 1
        if x < 2:
            qc.cx(ind, i)
        i += 1
        if x % 2 == 0:
            qc.cx(ind, i)
        i += 1
        ind += 1
    return qc
# print(query().draw(output="text"))
