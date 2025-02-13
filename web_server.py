import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import os
import machine
import rp2
import sys
import json


ssid = ""
password = ""


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
        
    # obtain IP address
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    pico_led.on()
    return ip


def read_csv():
    """Read CSV file and return as JSON string (without ujson)."""
    filename = "data.csv"
    data_list = []

    if filename not in os.listdir():
        return json.dumps({"error": "File not found"})

    with open(filename, "r") as file:
        headers = file.readline().strip().split(",")
        for line in file:
            values = line.strip().split(",")
            data_list.append(dict(zip(headers, values)))

    print(data_list)
    return json.dumps(data_list)  # Convert list to JSON string




# Open a socket so that the server and client can communicate
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    
    return connection

# define our web page
def webpage(temperature, state):
    html =f"""<!DOCTYPE html>
            <html>
            <body>

                <form action="./lighton">
                    <input type="submit" value="Light on" />
                </form>

                <form action="./lightoff">
                    <input type="submit" value="Light off" />
                </form>

                <form action="./close">
                    <input type="submit" value="Stop server" />
                </form>

                <p>LED is {state} </p>

                <p>Temperature is {temperature} </p>

            </body>
            </html>"""
    
    return str(html)

# serve our webpage and serve requests
def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    print('herere')
    
    # while listening to the client
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        
        # get the request string, and I try to see if the
        # light wants to be turned on/off or close the page
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        if request == '/lighton?':
            pico_led.on()
        elif request =='/lightoff?':
            pico_led.off()
        elif request == '/close?':
            sys.exit()
        elif request == "/data":
            data = read_csv()
            response = "HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + data
            client.send(response)
            client.close()

        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()

    

ip = connect()
connection = open_socket(ip)
serve(connection)


