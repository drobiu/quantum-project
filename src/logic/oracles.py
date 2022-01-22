from itertools import combinations

import numpy as np
import sys

from qiskit.circuit.library import QFT

from src.arithmetic.increment import control_increment, control_decrement
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from scipy.special import binom

from src.logic.s_gate import s_gate
from src.arithmetic.counter import count, mincount
from src.util.util import run_qc

sys.path.extend("../")


def oracle_a(circuit, q, a, s, do_inverse=False):
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
        circuit = mincount(circuit, a, q, step=2)

    circuit = circuit.compose(s_gate(s).to_gate(label="s"), qubits=q)

    return circuit


def c_gate(k, length=4):
    s = np.ones(length) * k

    return s_gate(s, length / 2)


def oracle_b(circuit, q, b, s, do_inverse=False):
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

        if not do_inverse:
            circuit = count(circuit, b, q, step=2, apply_QFT=False)
        else:
            circuit = mincount(circuit, b, q, step=2, apply_QFT=False)

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
                print('gate')
                if not do_inverse:
                    circuit = control_increment(circuit, b, temp_qubits, amount=comp, apply_QFT=False)
                else:
                    circuit = control_decrement(circuit, b, temp_qubits, amount=comp, apply_QFT=False)
        circuit = circuit.compose(c_gate(color))

    circuit = circuit.compose(QFT(num_qubits=b_l, approximation_degree=0, do_swaps=True,
                                  inverse=True, insert_barriers=True, name='iqft'), qubits=b)

    return circuit


def build_mastermind_b_circuit_v2(circuit, q, b, c, d, s, do_inverse=False):
    '''
    Counts b_s(q): the number of correct colours in query q (compared to s).
    Parameters
    ----------
    circuit : QuantumCircuit
        Quantum circuit to perform counting on.
    q : QuantumRegister, length n*ceil(log(k))
        Query register.
    b : QuantumRegister, length ceil(log(n))+1
        Register which stores amount of correct colours.
    c : QuantumRegister, length ceil(log(n))+1
        Ancilla register which stores the differences abs(n_s(q)-n_c(q)).
    d : QuantumRegister, length 1
        Ancilla register which stores the sign sgn(n_s(q)-n_c(q)).
    s : Int list, length n
        Secret string.
    do_inverse : bool (default: False)
        Whether to perform the inverse of the circuit.
    Returns
    -------
    circuit : QuantumCircuit
        Quantum circuit appended with b-oracle.

    '''

    # Extract basic system parameters (n = # of pins, k = # of colours, logk = # of bits for k)
    n = len(s)
    logk = len(q) // n

    # How often which colour occurs in the list
    secret_sequence_colours_amount = [list(s).count(i) for i in range(2 ** logk)]  # rather k, but that's annoying

    # Check if valid secret string
    if sum(secret_sequence_colours_amount) != n:
        raise ValueError("Secret string contains illegal values")

    # Put QFT on reg b outside loop for efficiency
    qft(circuit, b)

    # Add n to reg b (equivalent to adding n_c for each c; more efficient)
    increment(circuit, b, amount=n, do_qft=False)

    # Flip sign bit d
    circuit.x(d)
    # Loop over colours (and how often they're used)
    for (clr, nc) in enumerate(secret_sequence_colours_amount):
        # Only start counting process is colour is used at all
        if nc != 0:

            # Write colour clr in n*binary...
            binary_list = [bin(clr)[2:].zfill(logk)] * n
            # ... to CNOT with query (so if matches, then |11>)
            binary_to_x_gates(circuit, q, binary_list)

            if not do_inverse:

                # Add n_c(s) to reg c...
                increment(circuit, c, amount=nc, do_qft=True)

                # ... and subtract n_c(q) from that value (with sign bit d)
                icount(circuit, q, [*c, d], step=logk, do_qft=True)

                # If sign bit d has not flipped (i.e. is True, i.e n_c(q)<n_c(s)):
                #  subtract difference n_c(s)-n_c(q)
                csub(circuit, a=c, b=b, c=d, do_qft=False)

                # Undo step 1 & 2
                count(circuit, q, [*c, d], step=logk, do_qft=True)
                decrement(circuit, c, amount=nc, do_qft=True)

            else:

                # Inverse of steps above
                increment(circuit, c, amount=nc, do_qft=True)
                icount(circuit, q, [*c, d], step=logk, do_qft=True)
                cadd(circuit, a=c, b=b, c=d, do_qft=False)
                decrement(circuit, b, amount=nc, do_qft=False)
                count(circuit, q, [*c, d], step=logk, do_qft=True)
                decrement(circuit, c, amount=nc, do_qft=True)

            # Undo query CNOT
            binary_to_x_gates(circuit, q, binary_list)
            circuit.barrier()

    # Flip sign bit d
    circuit.x(d)

    # Finish sum procedure with iQFT on reg b
    iqft(circuit, b)

    return circuit


def binary_to_x_gates(circuit, q, s_bin):
    '''
    Places an x gate for each 0 of an element of s_bin
    Parameters
    ----------
    circuit : QuantumCircuit
        Circuit to add x gates to.
    q : QuantumRegister, length n*ceil(log(k))
        Register to add x gates to.
    s_bin : str list, length n (and strings of length ceil(log(k)))
        list containing binary strings.
    Returns
    -------
    circuit : QuantumCircuit
        Circuit appended with x gates according to secret_binary.

    '''

    # Amount of colour bits
    logk = len(s_bin[0])

    for (i, binary) in enumerate(s_bin):
        for (j, bit) in enumerate(binary[::-1]):
            if bit == '0':
                # add an X gate for a 0
                circuit.x(q[i * logk + j])
            else:
                # and otherwise an identity for clarity
                circuit.i(q[i * logk + j])

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
