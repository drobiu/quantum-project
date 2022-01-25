from qiskit.circuit.library import DraperQFTAdder
from src.arithmetic.subtractor import DraperQFTSubtractor


def comparator(circuit, a, b, c, num_state_qubits):

    circuit = circuit.compose(DraperQFTSubtractor(num_state_qubits), qubits=[*a[:], *b[:], *c[:]])

    circuit = circuit.compose(DraperQFTAdder(num_state_qubits), qubits=[*a[:], *b[:]])

    return circuit
