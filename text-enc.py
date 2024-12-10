import random
import time
from trivium.Trivium import Trivium 
from trivium.IVGenerator import IVGenerator

message = "Hello world from LAGGOUNE Walid"

def bytes_to_bits(byte_data):
    bit_string = ""
    for byte in byte_data:
        bit_string += format(byte, '08b')
    
    return bit_string

def bits_to_bytes(bit_data):
    byte_list = []
    
    for i in range(0, len(bit_data), 8):
        byte = int(bit_data[i:i+8], 2)
        byte_list.append(byte)
    
    return bytes(byte_list)


key = bytes([0b00100100, 0b10100101, 0b01010110, 0b11000000, 0b11111100, 0b01101000, 
             0b10101011, 0b11101111, 0b11001101, 0b0111011])  # 80 bits key
iv = IVGenerator(80).generate_iv() 


start_time = time.time()
tr = Trivium()
tr.init(key, iv)

final_key_stream = bytearray()
for byte in list(message.encode('utf-8')):
    keystream_for_byte = tr.generate_keystream(8)
    print('{:<15}{:<2}{:<15}'.format('Word', '=', chr(byte)))
    print('{:<15}{:<2}{} bits'.format('Stream size', '=', len(keystream_for_byte) * 8))
    print('{:<15}{:<2}{:<15}'.format('IV', '=', bytes_to_bits(iv)))
    print('{:<15}{:<2}{:<15}'.format('Encryption key', '=', bytes_to_bits(key)))
    print('{:<15}{:<2}{:<15}'.format('Keystream', '=', bytes_to_bits(keystream_for_byte)))
    print("\n")
    final_key_stream.extend(keystream_for_byte)

print("--------------------------------- \n")


print('{:<15}{:<2}{:<15}'.format('Plaintext', '=', message))
print('{:<15}{:<2}{:<15}'.format('IV Bits', '=', bytes_to_bits(iv)))
print('{:<15}{:<2}{:<15}'.format('KEY Bits', '=', bytes_to_bits(key)))
print('{:<15}{:<2}{:<15}'.format('Message Bits', '=', bytes_to_bits(message.encode('utf-8'))))
print('{:<15}{:<2}{:<15}'.format('Enc Keystream', '=', bytes_to_bits(final_key_stream)))

ciphertext = tr.encrypt(message.encode('utf-8'), final_key_stream)
print('{:<15}{:<2}{:<15}'.format('Encrypted', '=', bytes_to_bits(ciphertext)))


tr = Trivium()
tr.init(key, iv)

decryption_key_stream = tr.generate_keystream(len(ciphertext) * 8)
print('{:<15}{:<2}{:<15}'.format('Dec keystream', '=', bytes_to_bits(decryption_key_stream)))
print('{:<15}{:<2}{:<15}'.format('cipher', '=', bytes_to_bits(ciphertext)))

plaintext = tr.decrypt(ciphertext, decryption_key_stream)
print('{:<15}{:<2}{:<15}'.format('Decrypted', '=', plaintext.decode('utf-8')))

print("\n --- %s seconds ---" % (time.time() - start_time))
