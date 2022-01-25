from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister


def s_gate(num_array, num_state_array=2):
    num_bits = len(num_array) * num_state_array
    i = 0
    q = QuantumRegister(num_bits, "q")
    qc = QuantumCircuit(q)
    for x in num_array:
        if num_state_array == 3:
            if x < 4:
                qc.x(i)
            i += 1
        if x < 2:
            qc.x(i)
        i += 1
        if x % 2 == 0:
            qc.x(i)
        i += 1
    return qc
