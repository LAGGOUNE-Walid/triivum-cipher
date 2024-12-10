"""
    Written by LAGGOUNE Walid
    2024-12
    Trivium stream cipher
    Trivium has been designed by Christophe De Cannière and Bart Preneel. It is a 
    stream cipher (i.e. a cryptographic-strength RNG) selected by eSTREAM  (part of
    the the EU ECRYPT project) to be part of a portfolio of secure  algorithms
    https://www.ecrypt.eu.org/stream/e2-trivium.html
"""
import os
import random

class IVGenerator:
    
    def __init__(self, size=80):
        if size <= 0 or size % 8 != 0:
            raise ValueError("IV size must be a positive multiple of 8 bits.")
        self.size = size

    def generate_iv(self) -> bytes:
        byte_size = self.size // 8
        
        # On Linux, if the getrandom() syscall is available, it is used in blocking mode: 
        # block until the system urandom entropy pool is initialized (128 bits of entropy are collected by the kernel). 
        # See the PEP 524 for the rationale. On Linux, the getrandom() function can be used to get random bytes in non-blocking mode (using the GRND_NONBLOCK flag) or to poll until the system urandom entropy pool is initialized.
        # On a Unix-like system, random bytes are read from the /dev/urandom device https://en.wikipedia.org/wiki//dev/random. 
        # If the /dev/urandom  device is not available or not readable, the NotImplementedError exception is raised.
        # On Windows, it will use BCryptGenRandom().
        # os.urandom uses system entropy sources to have better random generation. 
        # Entropy sources are something that we cannot predict, like asynchronous events. 
        # For instance the frequency that we hit the keyboard keys cannot be predicted. 
        # Interrupts from other devices can also be unpredictable.
        random_bytes_seeder = os.urandom(byte_size) 
        random.seed(random_bytes_seeder)
        return random.randbytes(byte_size)

