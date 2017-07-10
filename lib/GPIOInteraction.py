import RPi.GPIO as GPIO
import time
class GPIOInteractor:
    
    def button_state_changed(self, channel):
        print(GPIO.input(18))
        if(not GPIO.input(18)):
            self.button_pressed()
        else:
            self.button_released()
            
    def button_pressed(self):
        self.pressed_at = time.time()
        
    def button_released(self):
        if(time.time() - self.pressed_at > self.time_to_hold):
            self.button_held_callback()
        else:    
            self.button_callback()
        
    def __init__(self):
        self.button_callback = None
        self.button_held_callback = None
        self.reset_callback = None
        self.pressed_at = None
        self.time_to_hold = 1
        self.time_to_reset = 5
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(18, GPIO.BOTH, callback=self.button_state_changed,bouncetime=200)        
        
    def set_button_callback(self, funct):
        self.button_callback = funct
        
    def set_button_held_callback(self, funct):
        self.button_held_callback = funct
        
    def set_reset_callback(self,funct):
        self.reset_callback = funct
        
    def cleanup(self):
        GPIO.cleanup()