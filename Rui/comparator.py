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
from subtractor import DraperQFTSubtractor
from qiskit.circuit.library import DraperQFTAdder
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')
authentication = TokenAuthentication('40a1a77810b8d0e10428efa64ae124e79f2b6336', scheme='token')
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')
def comparator(num_state_qubits):


    qr_a = QuantumRegister(num_state_qubits, name="a")
    qr_b = QuantumRegister(num_state_qubits, name="b")
    c=QuantumRegister(1,"c")
  
    

        # add registers
    qc=QuantumCircuit(qr_a,qr_b,c)

        # define register containing the sum and number of qubits for QFT circuit

        # build QFT adder circuit
    qc=qc.compose(DraperQFTSubtractor(num_state_qubits),qubits=range(2*num_state_qubits+1))

    qc=qc.compose(DraperQFTAdder(num_state_qubits),qubits=range(2*num_state_qubits))

    return qc













