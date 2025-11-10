# QERRA Starter Simulation: Quantum Ethical Rescue Resource Allocator
# A hybrid quantum-classical demo for bias-free resource allocation.
# Aided by Grok - For QAI PROJECT. Run with: python qerra_sim.py
# Requires: pip install qiskit numpy

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

def qerra_ethical_allocator(resources_available, priorities):
    """
    QERRA Core: Quantum sim for ethical resource allocation.
    - Inputs: Resources (e.g., [10, 20] drones/bots), Priorities (e.g., ['high', 'low'] for rescues).
    - Quantum: 2 qubits - Superposition (uncertainty), Entanglement (interdependence).
    - Output: Ethical decision (e.g., "Allocate to high-priority" if quantum prob > threshold).
    Ethics: Asimov-inspired - Prioritize life-saving, minimize bias.
    """
    # Setup 2-qubit circuit (qubit 0: Priority, qubit 1: Resource balance)
    qc = QuantumCircuit(2, 2)
    
    # Step 1: Superposition for ethical uncertainty (fair chance)
    qc.h(0)  # Hadamard on priority qubit
    
    # Step 2: Encode priorities (high=1, low=0 rotation)
    if priorities[0] == 'high':
        qc.rx(np.pi / 2, 0)  # Rotate for high priority
    
    # Step 3: Entangle for resource correlation (can't allocate without balance)
    qc.cx(0, 1)  # CNOT: Priority affects resources
    
    # Step 4: Measure outcomes
    qc.measure([0, 1], [0, 1])
    
    # Run on simulator (NISQ-ready; swap for IBM hardware later)
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Classical post-process: Ethical threshold (e.g., >50% for high-priority)
    high_priority_prob = counts.get('11', 0) / 1024  # '11' = High + Balanced
    
    if high_priority_prob > 0.5 and resources_available[0] >= 5:
        decision = "ETHICAL ALLOCATE: Send high-priority resources (bias-free quantum verdict)."
    else:
        decision = "BALANCE ETHICALLY: Diversify allocation (quantum uncertainty detected)."
    
    # Viz: Histogram for quantum results (save/plot)
    plot = plot_histogram(counts)
    plt.savefig('qerra_output.png')  # Saves plot image
    plt.show()
    
    return decision, counts, high_priority_prob

# Demo Run: Simulate a rescue scenario
if __name__ == "__main__":
    resources = [10, 5]  # e.g., drones for two sites
    priorities = ['high', 'low']  # Site 1: Critical rescue
    decision, counts, prob = qerra_ethical_allocator(resources, priorities)
    
    print(f"QERRA Verdict: {decision}")
    print(f"Quantum Counts: {counts}")
    print(f"High-Priority Probability: {prob:.2%}")
    print("Plot saved as qerra_output.png - Check for ethics viz!")
  Add starter QERRA simulation code

