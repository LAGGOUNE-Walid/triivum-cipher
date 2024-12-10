"""
    Written by LAGGOUNE Walid
    2024-12
    Trivium stream cipher
    Trivium has been designed by Christophe De Cannière and Bart Preneel. It is a 
    stream cipher (i.e. a cryptographic-strength RNG) selected by eSTREAM  (part of
    the the EU ECRYPT project) to be part of a portfolio of secure  algorithms
    https://www.ecrypt.eu.org/stream/e2-trivium.html
"""
class Trivium:
    def __init__(self):
        self.lsfrsStats = [0] * 288  
        self.key = None
        self.initialVector = None

    def init(self, key: bytes, initialVector: bytes):
        if len(key) != 10 or len(initialVector) != 10:
            raise ValueError("Key and IV must each be exactly 10 bytes (80 bits).")

        for i in range(80):
            byte = key[i // 8]
            bit = (byte >> (7 - (i % 8))) & 1 # byte to bit
            self.lsfrsStats[i] = bit
            
        for i in range(80):
            byte = initialVector[i // 8]
            bit = (byte >> (7 - (i % 8))) & 1            
            self.lsfrsStats[93 + i] = bit
        
        self.lsfrsStats[285:288] = [1, 1, 1]

        for _ in range(288):
            self._execute()

    def _execute(self):
        """
        This function runs one step of the Trivium algorithm and updates the state.
        It also returns a new bit (keystream bit).
        """
        # Calculate three feedback bits t1, t2, t3 based on certain positions in the state
        t1 = self.lsfrsStats[65] ^ (self.lsfrsStats[90] & self.lsfrsStats[91]) ^ self.lsfrsStats[92] ^ self.lsfrsStats[170]
        t2 = self.lsfrsStats[161] ^ (self.lsfrsStats[174] & self.lsfrsStats[175]) ^ self.lsfrsStats[176] ^ self.lsfrsStats[68]
        t3 = self.lsfrsStats[242] ^ (self.lsfrsStats[285] & self.lsfrsStats[286]) ^ self.lsfrsStats[287] ^ self.lsfrsStats[91]

        # Combine t1, t2, t3 into a new output bit
        keystreamBit = t1 ^ t2 ^ t3

        # Shift the state (move everything forward by one spot) and inject the new bits t1, t2, t3
        self.lsfrsStats = [t3] + self.lsfrsStats[:92] + [t1] + self.lsfrsStats[93:176] + [t2] + self.lsfrsStats[177:287]

        return keystreamBit

    def generate_keystream(self, length: int) -> bytes:
        keystream_bits = [self._execute() for _ in range(length)]
        
        # Convert the bits into bytes (group every 8 bits to form a byte)
        keystream_bytes = bytearray()
        for i in range(0, length, 8):
            byte = 0
            for j in range(8):
                if i + j < length:
                    byte = (byte << 1) | keystream_bits[i + j]
            keystream_bytes.append(byte)
        
        return bytes(keystream_bytes)  # Return the keystream as a byte object

    def encrypt(self, data: bytes, keystream: bytes) -> bytes:
        return bytes([data[i] ^ keystream[i] for i in range(len(data))])

    def decrypt(self, ciphertext: bytes, keystream: bytes) -> bytes:
        return self.encrypt(ciphertext, keystream) 
