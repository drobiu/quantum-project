import sys

from qiskit import ClassicalRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
import numpy as np
from src.logic.oracles import oracle_a
from src.logic.query import query_cd
from src.util.util import run_qc
from src.arithmetic.add import add
from src.arithmetic.counter import count, mincount
from src.arithmetic.increment import decrement, increment

sys.path.extend('../')


def FCPA(circuit, y_register, qy_register, s_register, memory, k, secret_string, c):
    # k is number of available colours
    # init
    # q1 = QuantumRegister(num_position, "q1")
    # q2 = QuantumRegister(num_bits_color * num_position)
    # out = QuantumRegister(num_bits_color + 1, "o")

    # step 1: apply H gate
    circuit.h(y_register[:])
    circuit.barrier()

    # step 2: section that repeat k times

    for d in range(k):
        # Query
        circuit = circuit.compose(query_cd(c, d), [*y_register, *qy_register])
        circuit.barrier()
        # Apply oracle A
        circuit = oracle_a(circuit, qy_register, s_register, secret_string)
        circuit.barrier()
        # add in memory qubits
        circuit = add(circuit, s_register, memory)
        circuit.barrier()
        # Apply inverse Oracle A
        circuit = oracle_a(circuit, qy_register, s_register, secret_string, do_inverse=True)
        circuit.barrier()
        # Apply inverse Query
        circuit = circuit.compose(query_cd(c, d), [*y_register, *qy_register])
        circuit.barrier()

    # step 3: count
    circuit = count(circuit, memory, y_register)
    circuit.barrier()

    # step 4:ignore
    # First logk lsb memory registers must be ignored.
    # For visualizing Idendity gate will be applied
    # Defining logk
    logk = int(np.ceil(np.log2(k)))

    for i in range(logk):
        circuit.i(memory[i])
    circuit.barrier()

    # step 5: decrement
    # Decrement
    circuit = decrement(circuit, memory[logk::])
    circuit.barrier()

    # step 6: z gate to the now remaining LSB memory
    circuit.z(memory[logk])
    circuit.barrier()

    # step 7: undo step 2:5
    # undo decrement
    circuit = increment(circuit, memory[logk::])
    circuit.barrier()
    # undo count
    circuit = mincount(circuit, memory, y_register)
    circuit.barrier()
    # undo the loop
    for d in range(k):
        print(d)
        # Query
        circuit = circuit.compose(query_cd(c, d), [*y_register, *qy_register])
        circuit.barrier()
        # Oracle A
        circuit = oracle_a(circuit, qy_register, s_register, secret_string)
        circuit.barrier()
        # Substractor
        circuit = add(circuit, s_register, memory, amount=-1)
        circuit.barrier()
        # Apply inverse Oracle A
        circuit = oracle_a(circuit, qy_register, s_register, secret_string, do_inverse=True)
        circuit.barrier()
        # Apply inverse Query
        circuit = circuit.compose(query_cd(c, d), [*y_register, *qy_register])
        circuit.barrier()

    # step 8: Hadamard
    circuit.h(y_register[:])
    circuit.barrier()

    return circuit


# Test
if __name__ == "__main__":
    qy = QuantumRegister(8, name='qy')
    y = QuantumRegister(4, name='y')
    s = QuantumRegister(3)
    c2 = ClassicalRegister(4)
    memory = QuantumRegister(5)
    qc = QuantumCircuit(y, qy, s, memory, c2)
    # k is number of available colours
    k = 4

    # qc.x(qy[0])
    qc = FCPA(qc, y, qy, s, memory, k, [1, 0, 2, 3], 0)
    qc.barrier()

    qc.measure(y[:], c2[::-1])

    run_qc(qc, with_QI=False)
    # print(qc.draw(output="text"))
