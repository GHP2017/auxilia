import os
class SoundPlayer:
    def __init__(self):
        self.pauseFile = "/home/pi/spotify_dj/Assets/brute-force.mp3"
        
    def play_pause_tone(self):
        os.system("mpg321 " + self.pauseFile)