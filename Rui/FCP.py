import sys
sys.path.append('../')
import numpy as np
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.library.basis_change import QFT
from quantuminspire.qiskit import QI
from getpass import getpass
from coreapi.auth import TokenAuthentication
from qiskit import BasicAer, execute
from query import query
from oracles import oracle_a
from 
def FCP(num_position,num_bits_color):
  q1=QuantumRegister(num_position,"q1")
  q2=QuantumRegister(num_bits_color*num_position,"q2")
  out=QuantumRegister(num_bits_color+1,"o")
  qc=QuantumCircuit(q1,q2,out)
  qc.h(range(num_position))
  qc=qc.compose(query().to_gate(label="query"),[q1,q2])
  qc=oracle_a(qc,q2,out,range(4))
  qc.z(out[0])
  qc.u() #add u dag gate
  return qc
#print(query().draw(output="text"))