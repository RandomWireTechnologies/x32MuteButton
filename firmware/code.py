import time
import board
import neopixel
import digitalio
import usb_cdc

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
button = digitalio.DigitalInOut(board.SWITCH)
lastButton = False
state = False
usb = usb_cdc.data
usb_buffer = b""
watchdogTimeout = 20

def getLEDState():
    global usb_buffer
    if usb:
        if usb.connected:
            if usb.in_waiting:
                data = usb.read(usb.in_waiting)
                usb_buffer += data
                print("usb_buffer: " + str(usb_buffer))
                if usb_buffer.find(b'\r') > -1:
                    if "led" in usb_buffer:
                        if "on" in usb_buffer or "1" in usb_buffer:
                            usb_buffer = b''
                            return True
                        elif "off" in usb_buffer or "0" in usb_buffer:
                            usb_buffer = b''
                            return False
                    usb_buffer = b''
    return None

def sendButtonState(buttonState):
    if usb:
        if usb.connected:
            if buttonState:
                usb.write(b"{\"button\": 1}\r")
            else:
                usb.write(b"{\"button\": 0}\r")
        
while True:
    # If button is pressed turn on the LED
    if button.value and not lastButton:
        #state = not state
        print("{\"button\": 1}")
        sendButtonState(True)
        # Sleep for 0.1 seconds to avoid bouncing
        time.sleep(0.1)
    elif not button.value and lastButton:
        print("{\"button\": 0}")
        sendButtonState(False)
        # Sleep for 0.1 seconds to avoid bouncing
        time.sleep(0.1)
    lastButton = button.value
    
    # Check for LED state from USB
    ledState = getLEDState()
    if ledState == None:
        if watchdogTimeout == 0:
            pixels.fill((255,0,0))
        else:
            watchdogTimeout -= 1
    else:
        watchdogTimeout = 20
        state = ledState
        if state:
            pixels.fill((0, 255, 0))
        else:
            pixels.fill((0, 0, 0))
    time.sleep(0.1)
