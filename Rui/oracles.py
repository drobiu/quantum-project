import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

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
    q_len = len(q)

    values = np.unique(s)
    for i in range(len(values)):
        circuit = circuit.compose(c_gate(i, int(q_len/2)))

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