import RPi.GPIO as GPIO
import time

def buttonPressed(channel):
    print("pressed")

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(18, GPIO.RISING, callback=buttonPressed,bouncetime=300)

while True:
    time.sleep(1)
    pass

GPIO.cleanup()
