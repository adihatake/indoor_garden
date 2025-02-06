from machine import Pin, I2C
from stemma_soil_sensor import StemmaSoilSensor # Save the two Libraries to the Pi Pico seesaw and stemma_soil_sensor 

SDA_PIN = 4 # GPIO 4 
SCL_PIN = 5 # GPIO 5

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)

stemma_soil_sensor = StemmaSoilSensor(i2c)
seesaw = stemma_soil_sensor # Data Sheet = ~200 (very dry) to ~2000 (very wet) 1015 = Wet, 331 = Dry
                            # Soil sensor has temp + or - 2 degrees Celsius

while True:
    try:
        moisture = seesaw.get_moisture()
        temperature = seesaw.get_temp()
        print(f'Moisture Level: {moisture}, Temperature: {temperature:.1f}{chr(176)}C')
         
    except Exception as e:
        # Sensor reset after 10 sec
        print(f"Error,Resetting: {e}")
        time.sleep(10)
        i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        stemma_soil_sensor = StemmaSoilSensor(i2c)
        seesaw = stemma_soil_sensor
