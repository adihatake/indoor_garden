from LDR_readings import read_LDR
from water_pump import pump_water
from soil_sensor import get_soil_reading
from grower_lights import LED_switch


current_exposure_time = 0

def main():
    global current_exposure_time
    
    while True:
        turn_on_LED = read_LDR()
        LED_switch(turn_on_LED)
            
        
        moisture, temperature = get_soil_reading()
        
        # if the plant is dry
        if moisture <= 400:
            pump_water() 
        
        # notifies raspberry pi status
        if temperature < 20:
            print('too cold')
            
        elif temperature > 35:
            print('too hot')
            
        
        with open('/data_sensors.txt','r') as file:
            for line in file:
                entry = line.strip().split(",")
                exposure_time = int(entry[-1])
                current_exposure_time = (exposure_time + 1)
            file.close()
            
        data_to_append = [str(temperature), str(moisture), str(current_exposure_time)]
            
        with open('/data_sensors.txt','a') as file:
            data_to_append = ','.join(data_to_append)
            file.write(data_to_append + "\n")
            print(data_to_append)
            file.close()
            

main()
