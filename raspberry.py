import RPi.GPIO as GPIO
import requests
import time

from OSC import OSCMessage
from OSC import OSCClient

RED_LED = 3
GREEN_LED = 21
SERVER = 'http://192.168.178.24:5000'

def led_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)

def red_led_on():
    GPIO.output(RED_LED, 1)

def red_led_off():
    GPIO.output(RED_LED, 0)

def green_led_on():
    GPIO.output(GREEN_LED, 1)

def green_led_off():
    GPIO.output(GREEN_LED, 0)

def led_teardown():
    GPIO.cleanup()

def hand_state():
    return requests.get(SERVER).json()

def led_control(state):
    distance = state['right']
    if distance and distance > 100 and distance < 600:
        red_led_off()
        green_led_on()
    else:
        red_led_on()
        green_led_off()

def clamp(n, lower, upper):
    if n < lower:
        return 0.0
    elif n >= lower and n < upper:
        return (n - lower) / float(upper)
    else:
        return 1.0

def main():
    led_setup()
    client = OSCClient()
    address = ('127.0.0.1', 6666)
    while True:
        state = hand_state()
        led_control(state)
        if state['left']:
            msg = OSCMessage('/volume')
            msg.append(clamp(state['left'], 100, 600))
            client.sendto(msg, address)
        if state['right']:
            msg = OSCMessage('/pitch')
            msg.append(clamp(state['right'], 100, 600))
            client.sendto(msg, address)
        time.sleep(0.01)
    led_teardown()

if __name__ == '__main__':
    main()
