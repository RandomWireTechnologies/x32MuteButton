#!/usr/local/bin/python3.11

import serial
import json
import xair_api
import time

ip = '192.168.2.240'
kind_id = "X32"
ch = 8
usbPort = '/dev/ttyACM1'
state = 0
count = 0
cycle_delay = 0.1

with serial.Serial(usbPort, timeout=0.1) as ser:
    print("USB Device Opened")
    while True:
        with xair_api.connect(kind_id, ip=ip) as mixer:
            print("Mixer Connected")
            while True:
                # Read mixer state
                enabled = int(mixer.strip[ch-1].mix.on == True)
                msg = json.dumps({"led": enabled}) + "\r"
                ser.write(msg.encode())
                #print(f"Setting LED to {enabled} with {msg}")
                # Read button state
                data = ser.readline().decode().strip()
                if data:
                    try:
                        #print(f"Debug: RCV from button={data}")
                        button_state = json.loads(data).get("button")
                        if button_state == 1:
                            # Toggle state
                            enabled = 1 - enabled
                            mixer.strip[ch-1].mix.on = enabled
                            print(f"Toggling enabled state to {enabled}")
                        else:
                            time.sleep(cycle_delay)
                    except:
                        time.sleep(cycle_delay)
                else:
                    time.sleep(cycle_delay)
                    count = count + 1



