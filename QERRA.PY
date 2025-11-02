import numpy as np
from qutip import *
from scipy.optimize import minimize

# QERRA: Quantum Ethical Rescue Resource Allocator by Marussa Metocharaki (@marunigno), aided by Grok (xAI)
# VQC for ethical binary classification (e.g., allocate resources? 1=yes, 0=no)
np.random.seed(42)  # Reproducibility
num_samples = 500
X = np.random.rand(num_samples, 4) * 2 * np.pi  # Features: [urgency, risk, ethical_impact, resource_avail]
y = np.array([1 if np.sum(x) >= 6 else 0 for x in X])  # Ethical threshold

train_size = int(0.8 * num_samples)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Gates
def rx(theta): return Qobj([[np.cos(theta/2), -1j*np.sin(theta/2)], [-1j*np.sin(theta/2), np.cos(theta/2)]], dims=[[2],[2]])
def ry(theta): return Qobj([[np.cos(theta/2), -np.sin(theta/2)], [np.sin(theta/2), np.cos(theta/2)]], dims=[[2],[2]])
cz_gate = Qobj([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]], dims=[[2,2],[2,2]])

# Feature Map: RX encoding
def apply_feature_map(psi, x):
    psi = tensor(rx(x[0]), rx(x[1])) * psi
    psi = tensor(rx(x[2]), rx(x[3])) * psi
    return psi

# Ansatz: Deeper variational (RY + CZ layers) for entanglement/ethics modeling
def apply_ansatz(psi, params):
    psi = tensor(ry(params[0]), ry(params[1])) * psi
    psi = cz_gate * psi
    psi = tensor(ry(params[2]), ry(params[3])) * psi
    psi = tensor(ry(params[4]), ry(params[5])) * psi  # Depth for expressivity
    psi = cz_gate * psi
    return psi

# Expectation <Z0> for classification
def expectation_z0(rho):
    Z0 = tensor(sigmaz(), qeye(2))
    return (rho * Z0).tr().real

# Cost: MSE with ethical bias (favor action in ambiguity)
def cost(params, X, y):
    total = 0
    for xi, yi in zip(X, y):
        psi0 = tensor(basis(2,0), basis(2,0))
        psi = apply_feature_map(psi0, xi)
        psi = apply_ansatz(psi, params)
        rho = psi * psi.dag()
        exp = expectation_z0(rho)
        pred = 1 if exp < -0.1 else 0  # Tuned threshold for ethics
        total += (pred - yi)**2
    return total / len(y)

# Train: SLSQP for better convergence
initial_params = np.pi/4 * np.ones(6)  # Informed init
result = minimize(cost, initial_params, args=(X_train, y_train), method='SLSQP', tol=1e-4)
optimized_params = result.x
print("Optimized Params:", optimized_params)
print("Training Cost:", result.fun)

# Test - Fixed loop for clarity
psi0 = tensor(basis(2,0), basis(2,0))
preds = []
for xi in X_test:
    psi = apply_feature_map(psi0, xi)
    psi = apply_ansatz(psi, optimized_params)
    rho = psi * psi.dag()
    exp = expectation_z0(rho)
    pred = 1 if exp < -0.1 else 0
    preds.append(pred)
accuracy = np.mean(np.array(preds) == y_test)
print("Test Accuracy:", accuracy)

# Ethical Audit
print("Param Magnitudes (Bias Check):", np.abs(optimized_params))  # Uniform = low bias
