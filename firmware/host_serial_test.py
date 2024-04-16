import serial
import json
import time
import os

# Check for /dev/ttyACM1
port = '/dev/ttyACM1'


# Toggle state variable
state = 0

while True:
    try:
        print("Waiting for port " + port)
        # Wait for the port to exist
        while not os.path.exists(port):
            time.sleep(1)
        # Open the serial port
        ser = serial.Serial(port, timeout=0.1)
        print("Waiting for data on " + port)

        while True:
            # Read JSON data with a timeout of 0.1 seconds
            data = ser.readline().decode().strip()
            if data:
                try:
                    json_data = json.loads(data)
                    button_state = json_data.get("button")
                    print("Button state: " + str(button_state))
                    if button_state == 1:
                        # Toggle the state
                        state = 1 - state
                        # Send JSON message representing the state change
                        message = json.dumps({"led": state}) + "\r"
                        print("Sending: " + message)
                        ser.write(message.encode())
                except json.JSONDecodeError:
                    print("Invalid JSON data")
    except serial.SerialException:
        print("Serial port error. Waiting 1 second.")
        time.sleep(1)
    else:
        print("Serial port closed. Waiting 1 second.")
        time.sleep(1)
