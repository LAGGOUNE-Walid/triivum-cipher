from Trivium import Trivium 
from IVGenerator import IVGenerator

def detect_period(trivium: Trivium) -> int:
    initial_state = trivium.lsfrsStats[:93]  
    
    period = 0
    current_state = trivium.lsfrsStats
    
    while True:
        trivium._execute()
        
        current_state = trivium.lsfrsStats[:93]
        print(f"Period {period}: \n \r {current_state} == {initial_state}")
    
        if current_state[:93] == initial_state:
            return period
        
        period += 1
tr = Trivium()

key = bytes([0b00100100, 0b10100101, 0b01010110, 0b11000000, 0b11111100, 0b01101000, 
             0b10101011, 0b11101111, 0b11001101, 0b0111011])  # 80 bits key
iv = IVGenerator(80).generate_iv() 
tr.init(key, iv)
detect_period(tr)