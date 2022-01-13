from qiskit.circuit.library import DraperQFTAdder
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister

from subtractor import DraperQFTSubtractor


def comparator(num_state_qubits):
    qr_a = QuantumRegister(num_state_qubits, name="a")
    qr_b = QuantumRegister(num_state_qubits, name="b")
    c = QuantumRegister(1, "c")

    # add registers
    qc = QuantumCircuit(qr_a, qr_b, c)

    # define register containing the sum and number of qubits for QFT circuit

    # build QFT adder circuit
    qc = qc.compose(DraperQFTSubtractor(num_state_qubits), qubits=range(7))

    qc = qc.compose(DraperQFTAdder(num_state_qubits), qubits=range(6))

    return qc
