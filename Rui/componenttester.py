import os
import sys 
sys.path.append('../')
from getpass import getpass
from coreapi.auth import TokenAuthentication
from qiskit import BasicAer, execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from query import query
from quantuminspire.credentials import get_authentication
from quantuminspire.qiskit import QI
from FCP import FCP

QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')
authentication = TokenAuthentication('40a1a77810b8d0e10428efa64ae124e79f2b6336', scheme='token')
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')


q = QuantumRegister(15, "q")
c = ClassicalRegister(15, "c")
qc = QuantumCircuit(q, c, name="conditional")


qc=qc.compose(FCP(4,2),range(15))

qc.measure(q,c)

qi_job = execute(qc, backend=qi_backend, shots=128)
qi_result = qi_job.result()
histogram = qi_result.get_counts(qc)
print("\nResult from the remote Quantum Inspire backend:\n")
print('State\tCounts')
[print('{0}\t{1}'.format(state, counts)) for state, counts in histogram.items()]

print("\nResult from the local Qiskit simulator backend:\n")
backend = BasicAer.get_backend("qasm_simulator")
job = execute(qc, backend=backend, shots=128)
result = job.result()
print(result.get_counts(qc))
print(qc.draw(output="text"))