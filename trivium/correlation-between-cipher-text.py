import random
import time
from Trivium import Trivium
from IVGenerator import IVGenerator 
import matplotlib.pyplot as plt 
import numpy as np

message = "Hello world"
rounds = 100000

key = bytes([0b00100100, 0b10100101, 0b01010110, 0b11000000, 0b11111100, 0b01101000, 
             0b10101011, 0b11101111, 0b11001101, 0b0111011])  # 80 bits key
iv = IVGenerator(80).generate_iv()  


tr = Trivium()
tr.init(key, iv)

print('{:<15}{:<2}{:<15}'.format('Plaintext', '=', message))

def hamming_distance(iv1: bytes, iv2: bytes) -> int:
    xor_result = int.from_bytes(iv1, 'big') ^ int.from_bytes(iv2, 'big')
    return bin(xor_result).count('1')

def normalized_correlation(iv1: bytes, iv2: bytes) -> float:
    size = len(iv1) * 8 
    hamming_dist = hamming_distance(iv1, iv2)
    return 1 - (hamming_dist / size)

correlations = [] 

reference_ciphertext = bytes()


for byte in list(message.encode('utf-8')):
    keystreamForByte = tr.generate_keystream(byte)
    reference_ciphertext += keystreamForByte

for i in range(rounds):
    new_ciphertext = bytes()
    for byte in list(message.encode('utf-8')):
        keystreamForByte = tr.generate_keystream(byte)
        new_ciphertext += keystreamForByte
    
    correlation = normalized_correlation(reference_ciphertext, new_ciphertext)
    correlations.append(correlation)
    reference_ciphertext = new_ciphertext


avg_correlation = np.mean(correlations)

plt.scatter(range(1, rounds + 1), correlations, alpha=0.5, label='Correlation')
plt.axhline(avg_correlation, color='r', linestyle='-', label=f'Avg Correlation ({avg_correlation:.4f})')
plt.xlabel('Iteration')
plt.ylabel('Correlation')
plt.title(f'Correlation Between Successive Ciphertexts ({rounds} Rounds)')
plt.grid(True)
plt.legend()
plt.show()
