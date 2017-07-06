import RPi.GPIO as GPIO
import time
class GPIOInteractor:
    
    def button_pressed(self, channel):
        self.buttonCallback()
        
    def __init__(self):
        self.buttonCallback = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(18, GPIO.RISING, callback=self.button_pressed,bouncetime=300)
        
    def set_button_callback(self, funct):
        self.buttonCallback = funct
        
    def cleanup(self):
        GPIO.cleanup()