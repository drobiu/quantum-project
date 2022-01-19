from math import pi
from qiskit import *
from qiskit.circuit.library.standard_gates import PhaseGate
from mastermind.arithmetic.qft import qft, iqft

def add(circuit,a,b,apply_QFT=true,amount=1):
    #Function adds a to b
    #Original add function build by https://github.com/TimVroomans/Quantum-Mastermind/blob/master/src/mastermind/arithmetic/dradder.py
    number_a=len(a)
    number_b=len(b)

    if number_a > number_b:
        raise ValueError("Amount of registers in b must be larger than a")

    # QFT(optional)
    if apply_QFT:
            qft(circuit, b)

    # Actual add loop
    for i in range(number_a):
        for j in range(number_b - i):
            circuit.cp(amount * pi / 2 ** (nb - i - j - 1), a[i], b[j])

    #Inverse QFT (optional)
    if apply_QFT:
        iqft(circuit, b)

    return circuit