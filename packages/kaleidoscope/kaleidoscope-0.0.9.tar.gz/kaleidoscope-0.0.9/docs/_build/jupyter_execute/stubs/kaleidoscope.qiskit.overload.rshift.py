from qiskit import QuantumCircuit
import kaleidoscope.qiskit
from kaleidoscope.qiskit.providers import Simulators

qc = QuantumCircuit(5, 5) >> Simulators.aer_vigo_simulator
print(qc.target_backend)