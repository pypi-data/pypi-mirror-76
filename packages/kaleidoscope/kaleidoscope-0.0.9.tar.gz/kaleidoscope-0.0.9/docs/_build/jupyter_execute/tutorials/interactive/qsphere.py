import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import kaleidoscope.qiskit
from kaleidoscope import qsphere

state = np.array([1/np.sqrt(2), 0, 0, 0, 0, 0, 0, 1/np.sqrt(2)])
qsphere(state)

qc = QuantumCircuit(3)
qc.h(range(3))
qc.cz(0,1)
state = Statevector.from_instruction(qc)

qsphere(state)

qsphere(qc.statevector())

qsphere(qc.statevector(), state_labels=False)