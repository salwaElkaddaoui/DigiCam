"""
Receive signal from push button with raspberry pi (tested with raspberry pi 2 model B).
Based on: https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
"""
try:
    import RPi.GPIO as GPIO
except:
    raise ImportError('You need to install python3-rpi.gpi')

BUTTON_PIN=10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Set pin 10 to be an input and set initial value to be pulled down (off)
while True:
    if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        print("Button was pushed")
        break
