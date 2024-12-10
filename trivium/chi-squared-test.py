import numpy as np
from scipy.stats import chisquare
from bitstring import BitArray
from IVGenerator import IVGenerator  # Assuming the class is in IVGenerator.py


rounds = 100000

def chi_squared_test_on_ivs(iv_generator, num_ivs=100):
    bit_counts = [0, 0]  # Index 0 for bit 0, index 1 for bit 1

    for _ in range(num_ivs):
        iv = iv_generator.generate_iv() 
        
        for byte in iv:
            bits = format(byte, '08b')
            bit_counts[0] += bits.count('0')  # Count 0
            bit_counts[1] += bits.count('1')  # Count 1

    total_bits = bit_counts[0] + bit_counts[1]
    expected_frequencies = [total_bits / 2, total_bits / 2]  # Expected uniform distribution

    chi2_statistic, p_value = chisquare(bit_counts, f_exp=expected_frequencies)

    return chi2_statistic, p_value, bit_counts


iv_generator = IVGenerator(size=80)

chi2_statistic, p_value, bit_counts = chi_squared_test_on_ivs(iv_generator, num_ivs=rounds)


print(f"P-value: {p_value}")
if p_value > 0.05:
    print(f"The Generated IV are random distribution for "+str(rounds)+" IV")
else:
    print(f"The IV generator is not random ")

