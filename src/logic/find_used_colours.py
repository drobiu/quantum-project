from qiskit import QuantumRegister, QuantumCircuit
from src.logic.oracles import oracle_b
from src.logic.query import query
from src.arithmetic.counter import mincount
from src.arithmetic.comparator import comparator


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

    # Step 1
    qc = oracle_b(qc, c, a, s)
    qc.barrier()

    # Step 2
    qc.h(b[:])
    qc.barrier()

    # Step 3
    qc = query(qc, b, c)
    qc.barrier()

    # Step 4
    qc = oracle_b(qc, c, d)
    qc.barrier()

    # Step 5
    qc.x(e[2])
    qc = mincount(qc, e, b)
    qc.barrier()

    # Step 6
    qc = comparator(qc, a, e, f, 3)
    qc.barrier()

    # Step 7
    qc.x(g)
    qc.x(a[:])
    qc.cx(a[:], g)
    qc.x(a[:])
    qc.barrier()

    # Step 8
    qc.cx(d[0], h)
    qc.cx([e[0]].append(f).append(g), h)
    qc.x(f)
    qc.cx([a[0]].append(f).append(g), h)
    qc.cx([b[0]].append(f).append(g), h)
    qc.x(f)
    qc.barrier()

    # Step 9
    qc.z(h)
    qc.barrier()

    # TODO: Step 10, 11, 12

    return qc

