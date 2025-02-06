from machine import Pin
import time

grow_lights = Pin(16, Pin.OUT) # Grow lights will be controlled with transistor, base of transistor is connected to GPIO 16

while True:
    
    # Will cycle grow lights on and off for 2 sec intervals
    grow_lights.value(1)
    time.sleep(2)
    
    grow_lights.value(0)
    time.sleep(2)
    
