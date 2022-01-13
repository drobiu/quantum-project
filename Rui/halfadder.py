
import os
import math 

from getpass import getpass
from coreapi.auth import TokenAuthentication
from qiskit import BasicAer, execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from quantuminspire.credentials import get_authentication
from quantuminspire.qiskit import QI
from qiskit.circuit.library import DraperQFTAdder

QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')



authentication = TokenAuthentication('40a1a77810b8d0e10428efa64ae124e79f2b6336', scheme='token')


QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')
a = QuantumRegister(3,"a")
b = QuantumRegister(3,"b")
qc = QuantumCircuit(a,b, name="conditional")
adder= DraperQFTAdder(3)
qc=qc.compose(adder)

print(adder.qubits)
print(qc.draw(output="text"))













  
