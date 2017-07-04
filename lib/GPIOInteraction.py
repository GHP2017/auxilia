import RPi.GPIO as GPIO
import time
class GPIOInteractor:
    
    def buttonPressed(self, channel):
        self.buttonCallback()
        
    def __init__(self):
        self.buttonCallback = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(18, GPIO.RISING, callback=self.buttonPressed,bouncetime=300)
        
    def setButtonCallback(self, funct):
        self.buttonCallback = funct
        
    def cleanup(self):
        GPIO.cleanup()