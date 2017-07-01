import os
import time
class Mouse:

    def __init__(self):
        pass

    def playSong(track_id):
        os.system("xdotool mousemove 45 260")
        time.sleep(.1)
        os.system("xdotool click 1")
        time.sleep(.2)
        os.system("xdotool mousemove 45 200")
        time.sleep(.1)
        os.system("xdotool click 1")
        time.sleep(.3)
        os.system("xdotool type "+ track_id)
        time.sleep(.2)
        os.system("xdotool key KP_Enter")

    def pause():
        os.system("xdotool key KP_Space")
    
    def play():
        os.system("xdotool key KP_Space")
    