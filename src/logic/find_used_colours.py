from qiskit import QuantumRegister, QuantumCircuit
from src.logic.oracles import oracle_b
from src.logic.query import query
from src.artihmetic.counter import mincount

def find_used_colours(n_positions, n_colors, secret_string):
    n = n_positions
    k = n_colors
    s = secret_string

    a = QuantumRegister(3)
    b = QuantumRegister(4)
    c = QuantumRegister(8)
    d = QuantumRegister(3)
    e = QuantumRegister(3)
    f = QuantumRegister(1)
    g = QuantumRegister(1)
    h = QuantumRegister(1)

    qc = QuantumCircuit(a, b, c, d, e, f, g, h)

    qc = oracle_b(qc, c, a, s)
    qc.barrier()

    qc.h(b[:])
    qc.barrier()

    qc = query(qc, b, c)
    qc.barrier()

    qc = oracle_b(qc, c, d)
    qc.barrier()

    qc.x(e[2])
    qc = mincount(qc, e, b)
    qc.barrier()

    return qc

