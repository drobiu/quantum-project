import math

from qiskit.circuit.library import PhaseGate
from qiskit.circuit.library.basis_change import QFT


def increment(circuit, register, amount=1, apply_QFT=True):
    q_reg = register
    num = len(q_reg)
    qc = circuit

    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=num, approximation_degree=0, do_swaps=True,
                            inverse=False, insert_barriers=True, name='qft'),register)
        qc.barrier()

    for i, qubit in enumerate(q_reg):
        qc.rx(amount * math.pi / 2 ** (num - 1 - i), qubit)

    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=num, approximation_degree=0, do_swaps=True,
                            inverse=True, insert_barriers=True, name='iqft'),register)
        qc.barrier()

    return qc


def control_increment(circuit, q_register, control_register, amount=1, apply_QFT=True):
    q_reg = q_register
    c_reg = control_register
    num_q = len(q_reg)
    num_c = len(control_register)
    qc = circuit
    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=num_q, approximation_degree=0, do_swaps=True,
                            inverse=False, insert_barriers=True, name='qft'),[*q_reg])
        qc.barrier()

    for i, qubit in enumerate(q_reg):
        ncp = PhaseGate(amount * math.pi / 2 ** (num_q - i - 1)).control(num_c)
        qc.append(ncp, [*c_reg, qubit])

    if apply_QFT:
        qc.barrier()
        qc = qc.compose(QFT(num_qubits=num_q, approximation_degree=0, do_swaps=True,
                            inverse=True, insert_barriers=True, name='iqft'),[*q_reg])
        qc.barrier()
    return qc


def decrement(circuit, register, amount=1, apply_QFT=True):
    return increment(circuit, register, -amount, apply_QFT)


def control_decrement(circuit, q_register, control_register, amount=1, apply_QFT=True):
    return control_increment(circuit, q_register, control_register, -amount, apply_QFT)

