from math import pi
from qiskit import *
from qiskit.circuit.library.standard_gates import PhaseGate
from qiskit.circuit.library.basis_change import QFT

def add(circuit,a,b,apply_QFT=True,amount=1):
    #Function adds a to b
    #Original add function build by https://github.com/TimVroomans/Quantum-Mastermind/blob/master/src/mastermind/arithmetic/dradder.py
    number_a=len(a)
    number_b=len(b)
    num=number_b+number_a


    if number_a > number_b:
        raise ValueError("Amount of registers in b must be larger than a")

    # QFT(optional)
    if apply_QFT:
        circuit = circuit.compose(QFT(num_qubits=num, approximation_degree=0, do_swaps=True,
                            inverse=False, insert_barriers=True, name='qft'),[*a,*b])

    # Actual add loop
    for i in range(number_a):
        for j in range(number_b - i):
            circuit.cp(amount * pi / 2 ** (number_b - i - j - 1), a[i], b[j])

    #Inverse QFT (optional)
    if apply_QFT:
        circuit = circuit.compose(QFT(num_qubits=num, approximation_degree=0, do_swaps=True,
                            inverse=True, insert_barriers=True, name='iqft'),[*a,*b])

    return circuit

