import random
import os
import base64
from trivium.Trivium import Trivium
from trivium.IVGenerator import IVGenerator
import text_to_image

input_image = "images/1mb.jpg"
out_enc = "images/encrypted-image.png"  
out_dec = "images/decrypted-image.png" 
keystream_file = "images/keystream.bin"


key = bytes([0b00100100, 0b10100101, 0b01010110, 0b11000000, 0b11111100, 0b01101000, 
             0b10101011, 0b11101111, 0b11001101, 0b0111011])  # 80 bits key
iv = IVGenerator(80).generate_iv()  

tr = Trivium()
tr.init(key, iv)

print("Encrypting the image... \n")
total_size = os.path.getsize(input_image)

with open(input_image, "rb") as f_in, open(keystream_file, "wb") as f_ks:
    processed_size = 0
    total_encrypted_bytes = b''
    
    while True:
        chunk = f_in.read(1024)
        if not chunk:
            break
        
        keystream = tr.generate_keystream(len(chunk) * 8)  
        f_ks.write(keystream) 


        encrypted_data = tr.encrypt(chunk, keystream)
        total_encrypted_bytes += encrypted_data
        
        processed_size += len(chunk)
        progress = (processed_size / total_size) * 100
        print(f"\rEncryption Progress: {progress:.2f}%", end="")


base64_total_encrypted_bytes = base64.b64encode(total_encrypted_bytes).decode('utf-8')
text_to_image.encode(base64_total_encrypted_bytes, out_enc)

print(f"\nEncrypted image saved as: {out_enc}")
print(f"Keystream saved as: {keystream_file}")


print("\n\n\nDecrypting the image \n")

decoded_text = text_to_image.decode(out_enc)
decoded_bytes = base64.b64decode(decoded_text)


tr = Trivium()
tr.init(key, iv)

with open(out_dec, "wb") as f_dec:
    keystream = tr.generate_keystream(len(decoded_bytes) * 8)
    decrypted_data = tr.decrypt(decoded_bytes, keystream)
    f_dec.write(decrypted_data)

print(f"Decrypted image saved as: {out_dec}")
