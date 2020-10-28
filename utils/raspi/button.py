"""
Functions for interacting witha  simple push button connected to a raspberry pi..
Based on: https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
"""
try:
    import RPi.GPIO as GPIO
except:
    raise ImportError('You need to install python3-rpi.gpio')

def receive(button_pin: int) -> bool:
    """Receive signal when a push button is pushed.
        #Arguments:
            button_pin: pin of the push button
        #Returns
            True when the button is pushed, otherwise it keeps listening for a push
    """
    assert isinstance(button_pin, int), "button pin should be an integer"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) #use physical pin numbering
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Set button pin to be an input and set initial value to be pulled down (off)
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            print("Button was pushed")
            break
    return True
