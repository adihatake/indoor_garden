from machine import Pin
import time

pump = Pin(16, Pin.OUT) # Pump pin is connected to the transistor base, Pump is connected to 5v of PI Pico with a potentiometer in series to control flow.

while True:
        try:
            #Cycles pump on for 2 seconds and off for 2 seconds
            pump.value(1)
            time.sleep(2)
                
            pump.value(0)
            time.sleep(2)
            
            print('hello')
        except:
            pass