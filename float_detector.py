from machine import Pin
import time

# Configure GPIO pin 0 connected to the float switch
float_switch = Pin(10, Pin.IN, Pin.PULL_UP)  # Assuming the float switch uses a pull-up configuration
led = Pin('LED', Pin.OUT)

def read_float_switch():
    """Reads the state of the float switch."""
    if float_switch.value() == 1:  # Assuming 1 means liquid is present.
        led(1)
        return "Liquid Level HIGH (Float Switch Activated)"
    else:
        led(0)
        return "Liquid Level LOW (Float Switch Deactivated)"

try:
    while True:
        status = read_float_switch()
        print(status)
        time.sleep(0.5)  # Update every second
except KeyboardInterrupt:
    print("Exiting program.")

