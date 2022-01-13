from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import QFT

from src.artihmetic.increment import control_increment, control_decrement
from src.util.util import run_qc


def count(circuit, q_register, a_register, amount=1, step=1, apply_QFT=True):
    q_l = len(q_register)
    a_l = len(a_register)

    assert a_l % step == 0

    if apply_QFT:
        circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=False, insert_barriers=True, name='qft'))
        circuit.barrier()

    for i in range(int(a_l / step)):
        circuit = control_increment(circuit, q_register, a_register[i * step:(i + 1) * step], amount, apply_QFT=False)

    if apply_QFT:
        circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=True, insert_barriers=True, name='iqft'))
        circuit.barrier()

    return circuit


def mincount(circuit, q_register, a_register, amount=1, step=1, apply_QFT=True):
    q_l = len(q_register)
    a_l = len(a_register)

    assert a_l % step == 0

    if apply_QFT:
        circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=False, insert_barriers=True, name='qft'))
        circuit.barrier()

    for i in range(int(a_l / step)):
        circuit = control_decrement(circuit, q_register, a_register[i * step:(i + 1) * step], amount, apply_QFT=False)

    if apply_QFT:
        circuit.barrier()
        circuit = circuit.compose(QFT(num_qubits=q_l, approximation_degree=0, do_swaps=True,
                                      inverse=True, insert_barriers=True, name='iqft'))
        circuit.barrier()

    return circuit


def test():
    q = QuantumRegister(3)
    a = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q, a, c)

    qc.x(a[0])
    qc.x(q[:])

    qc = mincount(qc, q, a)

    # Should equal 110
    qc.measure(q[:], c[:])

    run_qc(qc)
    qc.draw(output="mpl")


if __name__ == "__main__":
    test()
