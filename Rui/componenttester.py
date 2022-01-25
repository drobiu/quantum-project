import os
import sys
sys.path.extend('../')

from coreapi.auth import TokenAuthentication
from qiskit import BasicAer, execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from quantuminspire.qiskit import QI

from src.logic.find_color_positions import FCP


QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')
authentication = TokenAuthentication('40a1a77810b8d0e10428efa64ae124e79f2b6336', scheme='token')
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')

q = QuantumRegister(15, "q")
c = ClassicalRegister(4, "c")
qc = QuantumCircuit(q, c, name="conditional")

qc = FCP(qc,q[0:4],q[4:12],q[12:15], [0, 1, 1 , 3],1,3)

qc.measure([0,1,2,3], [0,1,2,3])

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
