import numpy as np
import IVGenerator
import time
import matplotlib.pyplot as plt 

def hamming_distance(iv1: bytes, iv2: bytes) -> int:
    xor_result = int.from_bytes(iv1, 'big') ^ int.from_bytes(iv2, 'big')
    return bin(xor_result).count('1')

def normalized_correlation(iv1: bytes, iv2: bytes) -> float:
    size = len(iv1) * 8 
    hamming_dist = hamming_distance(iv1, iv2)
    return 1 - (hamming_dist / size)

def auto_correlation(iv: bytes, lag: int) -> float:
    n = len(iv)
    correlation = 0
    for i in range(n - lag):
        correlation += (iv[i] == iv[i + lag])
    return correlation / (n - lag)

generator = IVGenerator.IVGenerator(size=80)
reference_iv = generator.generate_iv()

correlations = [] 
rounds = 100000
for i in range(rounds):
    new_iv = generator.generate_iv()
    correlation = normalized_correlation(reference_iv, new_iv)
    correlations.append(correlation)
    reference_iv = new_iv

avg_correlation = np.mean(correlations)

plt.scatter(range(1, rounds + 1), correlations, alpha=0.5, label='Correlation')
plt.axhline(avg_correlation, color='r', linestyle='-', label=f'Avg Correlation ({avg_correlation:.4f})')
plt.xlabel('Iteration')
plt.ylabel('Correlation')
plt.title(f'Correlation Between Successive IVs ({rounds} Rounds)')
plt.grid(True)
plt.legend()
plt.show()

lags = []

for lag in range(1, len(reference_iv) - 1):
    lags.append(auto_correlation(reference_iv, lag))

plt.plot(range(1, len(reference_iv) - 1), lags)
plt.xlabel('Lag')
plt.ylabel('Auto-correlation')
plt.title(f'Auto-correlation of the last IV (lags 1 to {len(reference_iv)})')
plt.grid(True)
plt.show()
