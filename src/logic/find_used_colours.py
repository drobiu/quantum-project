from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from src.logic.oracles import oracle_b
from src.logic.query import query
from src.arithmetic.counter import mincount, count
from src.arithmetic.comparator import comparator
from src.util.util import run_qc


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
    cl = ClassicalRegister(4)

    qc = QuantumCircuit(a, b, c, d, e, f, g, h, cl)

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
    qc = oracle_b(qc, c, d, s)
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
    qc.cx([e[0], f[0], g[0]], h)
    qc.x(f)
    qc.cx([e[0], f[0], g[0]], h)
    qc.cx([b[0], f[0], g[0]], h)
    qc.x(f)
    qc.barrier()

    # Step 9
    qc.z(h)
    qc.barrier()

    # Step 10
    qc.x(f)
    qc.cx([b[0], f[0], g[0]], h)
    qc.cx([e[0], f[0], g[0]], h)
    qc.x(f)
    qc.cx([e[0], f[0], g[0]], h)
    qc.cx(d[0], h)
    qc.x(a[:])
    qc.cx(a[:], g)
    qc.x(a[:])
    qc.x(g)
    qc = comparator(qc, a, e, f, 3)
    qc = count(qc, e, b)
    qc.x(e[2])
    qc = oracle_b(qc, c, d, s, True)
    qc = query(qc, b, c)

    #  Step 11
    qc.h(b[:])
    qc.barrier()

    #  Step 12
    qc.measure(b[:], cl[:])

    return qc


if __name__ == "__main__":
    qc = find_used_colours(4, 4, [0, 0, 0, 0])

    run_qc(qc, with_QI=False)
    qc.draw(output="text")

