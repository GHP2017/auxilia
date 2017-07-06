import os
import time
class Mouse:

    def __init__(self):
        self.in_transition = False
        pass

    def play_song(self, track_id):
        self.in_transition = True
        os.system("xdotool mousemove 45 260")
        time.sleep(.3)
        os.system("xdotool click 1")
        time.sleep(.4)
        os.system("xdotool mousemove 45 200")
        time.sleep(.3)
        os.system("xdotool click 1")
        time.sleep(1)
        os.system("xdotool key KP_Delete")
        time.sleep(.2)
        os.system("xdotool type spotify:track:"+ track_id)
        time.sleep(.5)
        os.system("xdotool key KP_Enter")
        self.in_transition = False

    def pause(self):
        os.system("xdotool key KP_Space")
    
    def play(self):
        os.system("xdotool key KP_Space")

        
    