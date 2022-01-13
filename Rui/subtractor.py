import numpy as np
import os
import math
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.library.basis_change import QFT
from quantuminspire.qiskit import QI
from getpass import getpass
from coreapi.auth import TokenAuthentication
from qiskit import BasicAer, execute
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')



authentication = TokenAuthentication('40a1a77810b8d0e10428efa64ae124e79f2b6336', scheme='token')
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')
def DraperQFTSubtractor(num_state_qubits, kind: str = "fixed"):
    if kind == "full":
            raise ValueError("The DraperQFTAdder only supports 'half' and 'fixed' as ``kind``.")

    if num_state_qubits < 1:
            raise ValueError("The number of qubits must be at least 1.")

    qr_a = QuantumRegister(num_state_qubits, name="a")
    qr_b = QuantumRegister(num_state_qubits, name="b")
    

    
    
    

        # add registers
    qc=QuantumCircuit(qr_a,qr_b)

        # define register containing the sum and number of qubits for QFT circuit
    qr_sum = qr_b[:] if kind == "fixed" else qr_b[:] + qr_z[:]
    num_qubits_qft = num_state_qubits if kind == "fixed" else num_state_qubits + 1

        # build QFT adder circuit
    qc.append(QFT(num_qubits_qft, do_swaps=False).to_gate(), qr_sum[:])

    for j in range(num_state_qubits):
        for k in range(num_state_qubits - j):
            lam = -np.pi / (2 ** k)
            qc.cp(lam, qr_a[j], qr_b[j + k])

    if kind == "half":
        for j in range(num_state_qubits):
            lam = -np.pi / (2 ** (j + 1))
            qc.cp(lam, qr_a[num_state_qubits - j - 1], qr_z[0])

    qc.append(QFT(num_qubits_qft, do_swaps=False).inverse().to_gate(), qr_sum[:])

    return qc

print(DraperQFTSubtractor(3).draw(output="text"))