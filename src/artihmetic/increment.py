import math

from qiskit.circuit.library.basis_change import QFT
from qiskit.circuit.library.standard_gates import PhaseGate

def increment(circuit, register, amount=1, apply_QFT=True):
    q_reg = register
    num = len(q_reg)
    qc = circuit

    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=num, approximation_degree=0, do_swaps=True,
                            inverse=False, insert_barriers=True, name='qft'))
        qc.barrier()

    for i, qubit in enumerate(q_reg):
        qc.rx(amount * math.pi / 2 ** (num - 1 - i), qubit)

    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=num, approximation_degree=0, do_swaps=True,
                            inverse=True, insert_barriers=True, name='iqft'))
        qc.barrier()

    return qc


def control_increment(circuit, qregister, cregister, amount=1, apply_QFT=True):
    q_reg = qregister
    c_reg = cregister
    numq = len(q_reg)
    numc = len(c_reg)
    qc = circuit
    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=numq, approximation_degree=0, do_swaps=True,
                            inverse=False, insert_barriers=True, name='qft'))
        qc.barrier()
    for i, qubit in enumerate(q_reg):
        qc.rx(amount * math.pi / 2 ** (numq - i - 1),c_reg,qubit)
        

    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=numq, approximation_degree=0, do_swaps=True,
                            inverse=True, insert_barriers=True, name='iqft'))
        qc.barrier()
    return qc


def decrement(circuit, register, amount=1, apply_QFT=True):
    return increment(circuit, register, -amount, apply_QFT)


def control_decrement(circuit, qregister, cregister, amount=1, apply_QFT=True):
    return control_increment(circuit, qregister, cregister, -amount, apply_QFT)
