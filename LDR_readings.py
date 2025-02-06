from machine import Pin  
import time

ldr = machine.ADC(28)  # Initialize an ADC object for pin 28

while True:
    ldr_value = ldr.read_u16()  # Read the LDR value and convert it to a 16-bit unsigned integer
    print("LDR Value:", ldr_value)  # Print the LDR value to the console
    # Dark Values ~ 400
    # Indoor Lighting ~ 200
    #time.sleep(1)  
