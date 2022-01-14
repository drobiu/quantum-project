import numpy as np
from qiskit.circuit.library.basis_change import QFT
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.quantumregister import QuantumRegister


def DraperQFTSubtractor(num_state_qubits, kind: str = "fixed"):
    if kind == "full":
        raise ValueError("The DraperQFTAdder only supports 'half' and 'fixed' as ``kind``.")

    if num_state_qubits < 1:
        raise ValueError("The number of qubits must be at least 1.")

    qr_a = QuantumRegister(num_state_qubits, name="a")
    qr_b = QuantumRegister(num_state_qubits + 1, name="b")

    # add registers
    qc = QuantumCircuit(qr_a, qr_b)

    # define register containing the sum and number of qubits for QFT circuit

    # build QFT adder circuit
    qc.append(QFT(num_state_qubits + 1, do_swaps=False).to_gate(), qr_b)

    for j in range(num_state_qubits):
        for k in range(num_state_qubits + 1 - j):
            lam = -np.pi / (2 ** k)
            qc.cp(lam, qr_a[j], qr_b[j + k])

    qc.append(QFT(num_state_qubits + 1, do_swaps=False).inverse().to_gate(), qr_b)

    return qc


# print(DraperQFTSubtractor(3).draw(output="text"))
"""
a_0: ─────────■───────■─────────■─────────────────■───────────────────────────────────────────────────────
              │       │         │                 │
a_1: ─────────┼───────┼─────────┼─────────■───────┼─────────■─────────■───────────────────────────────────
              │       │         │         │       │         │         │
a_2: ─────────┼───────┼─────────┼─────────┼───────┼─────────┼─────────┼─────────■───────■─────────────────
     ┌──────┐ │P(-π)  │         │         │       │         │         │         │       │        ┌───────┐
b_0: ┤0     ├─■───────┼─────────┼─────────┼───────┼─────────┼─────────┼─────────┼───────┼────────┤0      ├
     │      │         │P(-π/2)  │         │P(-π)  │         │         │         │       │        │       │
b_1: ┤1     ├─────────■─────────┼─────────■───────┼─────────┼─────────┼─────────┼───────┼────────┤1      ├
     │  QFT │                   │P(-π/4)          │         │P(-π/2)  │         │P(-π)  │        │  IQFT │
b_2: ┤2     ├───────────────────■─────────────────┼─────────■─────────┼─────────■───────┼────────┤2      ├
     │      │                                     │P(-π/8)            │P(-π/4)          │P(-π/2) │       │
b_3: ┤3     ├─────────────────────────────────────■───────────────────■─────────────────■────────┤3      ├
     └──────┘                                                                                    └───────┘
"""
