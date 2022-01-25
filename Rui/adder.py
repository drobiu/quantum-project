import os

from coreapi.auth import TokenAuthentication
from qiskit.circuit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library import DraperQFTAdder
from quantuminspire.qiskit import QI

QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

authentication = TokenAuthentication('40a1a77810b8d0e10428efa64ae124e79f2b6336', scheme='token')

QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')
a = QuantumRegister(3, "a")
b = QuantumRegister(3, "b")
qc = QuantumCircuit(a, b, name="conditional")
adder = DraperQFTAdder(3)
qc = qc.compose(adder.to_gate(label="adder"))

print(adder.qubits)
print(qc.draw(output="text"))
