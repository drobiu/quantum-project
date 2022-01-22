from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister, BasicAer, execute
from qiskit.circuit.library import XGate

from src.logic.oracles import oracle_b, oracle_a
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
    qc = oracle_a(qc, c, a, s)
    # qc.barrier()

    # Step 2
    qc.h(b[:])
    # qc.barrier()

    # Step 3
    _build_query(qc, b, c)
    # qc.barrier()

    # Step 4
    qc = oracle_b(qc, c, d, s)
    # qc.barrier()

    # Step 5
    qc.x(e[-1])
    qc = mincount(qc, e, b)
    # qc.barrier()

    # Step 6
    qc = comparator(qc, a, e, f, 3)
    # qc.barrier()

    # Step 7
    qc.x(g)
    qc.x(a[:])
    multiply_controlled_x(qc, a, g)
    qc.x(a[:])
    # qc.barrier()

    # Step 8
    qc.x(d[0], h)
    multiply_controlled_x(qc, [e[0], f, g], h)
    qc.x(f)
    multiply_controlled_x(qc, [e[0], f, g], h)
    multiply_controlled_x(qc, [b[0], f, g], h)
    qc.x(f)
    # qc.barrier()

    # Step 9
    qc.z(h)
    # qc.barrier()

    # Step 10
    qc.x(f)
    multiply_controlled_x(qc, [b[0], f, g], h)
    multiply_controlled_x(qc, [e[0], f, g], h)
    qc.x(f)
    multiply_controlled_x(qc, [e[0], f, g], h)
    qc.cx(d[0], h)
    qc.x(a[:])
    qc.cx(a[:], g)
    qc.x(a[:])
    qc.x(g)
    qc = comparator(qc, a, e, f, 3)
    qc = count(qc, e, b)
    qc.x(e[2])
    qc = oracle_b(qc, c, d, s, True)
    _build_query(qc, b, c)

    #  Step 11
    qc.h(b[:])
    # qc.barrier()

    #  Step 12
    qc.measure(b[:], cl[:])

    qc.draw(output='text')

    print("\nResult from the local Qiskit simulator backend:\n")
    backend = BasicAer.get_backend("qasm_simulator")
    job = execute(qc, backend=backend, shots=1)
    result = job.result()
    print(result.get_counts(qc))

    return qc


def _build_query(circuit, x, q):
    n_x = len(x)
    n_q = len(q)

    amount_colour_bits = n_q // n_x

    binary_list = [bin(x)[2:].zfill(amount_colour_bits) for x in range(n_x)]

    for (i, binary) in enumerate(binary_list):
        for (j, bit) in enumerate(binary[::-1]):
            if bit == '1':  # or '0'?
                circuit.cnot(x[i], q[i * amount_colour_bits + j])
            else:
                pass
                # circuit.i(q[i*amount_colour_bits + j])

    return circuit


def multiply_controlled_x(circuit, control, qubit):
    num_c = len(control)

    cx = XGate().control(num_c)
    circuit.append(cx, [*control, qubit])


if __name__ == "__main__":
    qc = find_used_colours(4, 4, [1, 3, 2, 0])
