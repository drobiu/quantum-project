from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister


def query(circuit, c, q, num_array=[0, 1, 2, 3], num_state_array=2):
    i = 0
    ind = 0

    for x in num_array:
        if num_state_array == 3:
            if x < 4:
                circuit.cx(c[ind], q[i])
            i += 1
        if x < 2:
            circuit.cx(c[ind], q[i])
        i += 1
        if x % 2 == 0:
            circuit.cx(c[ind], q[i])
        i += 1
        ind += 1

    return circuit


def query_cd(c_in=2, d_in=3, num_position_bits=4, num_state_array=2):
    # c_in:          int, represents color c
    # d_in:          int, represents color d
    # Each position qbit corresponds to two or three color bits
    # If a position is 1, the output of query is c in 2 or 3 bits, else d in 2 or 3 bits
    num_bits = num_position_bits * num_state_array
    i = num_position_bits
    c = QuantumRegister(num_position_bits, "c")
    q = QuantumRegister(num_bits, "q")
    qc = QuantumCircuit(c, q)
    for ind in range(num_position_bits):
        # build c in query
        x = c_in
        imark = i
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
        # reverse x, prepare to build d in circuit
        qc.x(ind)
        i = imark
        x = d_in
        # build d in circuit
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
        qc.x(ind)

    return qc
