import math
import os

from qiskit import execute, BasicAer, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import QFT
from quantuminspire.credentials import get_authentication
from quantuminspire.qiskit import QI
from src.artihmetic.increment import control_increment, control_decrement

QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

authentication = get_authentication()
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')


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

    qi_job = execute(qc, backend=qi_backend, shots=1024)
    qi_result = qi_job.result()
    histogram = qi_result.get_counts(qc)
    print("\nResult from the remote Quantum Inspire backend:\n")
    print('State\tCounts')
    [print('{0}\t{1}'.format(state, counts)) for state, counts in histogram.items()]

    print("\nResult from the local Qiskit simulator backend:\n")
    backend = BasicAer.get_backend("qasm_simulator")
    job = execute(qc, backend=backend, shots=1024)
    result = job.result()
    print(result.get_counts(qc))
    qc.draw(output="mpl")


if __name__ == "__main__":
    test()
