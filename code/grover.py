import os
import math 

from getpass import getpass
from coreapi.auth import BasicAuthentication
from qiskit import BasicAer, execute
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from quantuminspire.credentials import get_authentication
from quantuminspire.qiskit import QI

QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

email = 'k.t.dobiczek@student.tudelft.nl'
password = getpass()

authentication = BasicAuthentication(email, password)
QI.set_authentication(authentication, QI_URL)
qi_backend = QI.get_backend('QX single-node simulator')

q = QuantumRegister(3, "q")
c0 = ClassicalRegister(1, "c0")
c1 = ClassicalRegister(1, "c1")
c2 = ClassicalRegister(1, "c2")
qc = QuantumCircuit(q, c0, c1, c2, name="conditional")

qc.h(q[0:3])

def grover():
    qc.x(q[0])
    qc.h(q[2])

    qc.toffoli(q[0], q[1], q[2])

    qc.x(q[0])

    qc.h(q[0:2])

    qc.x(q[0:3])

    qc.h(q[2])

    qc.toffoli(q[0], q[1], q[2])

    qc.h(q[2])

    qc.x(q[0:3])

    qc.h(q[0:3])
    
for i in range(int(math.pi/4*math.sqrt(8))):
    grover()

qc.measure(q[0], c0)
qc.measure(q[1], c1)
qc.measure(q[2], c2)

qi_job = execute(qc, backend=qi_backend, shots=1024)
qi_result = qi_job.result()
histogram = qi_result.get_counts(qc)
print("\nResult from the remote Quantum Inspire backend:\n")
print('State\tCounts')
[print('{0}\t{1}'.format(state, counts)) for state, counts in histogram.items()]

print("\nResult from the local Qiskit simulator backend:\n")
backend = BasicAer.get_backend("qasm_simulator")
job = execute(qc, backend=backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
qc.draw(output="latex")