import os
class SoundPlayer:
    def __init__(self):
        self.pause_file = "/home/pi/spotify_dj/Assets/brute-force.mp3"
        self.skip_file = "/home/pi/spotify_dj/Assets/SkipTone.mp3"
        self.boot_file = "/home/pi/spotify_dj/Assets/bootup.mp3"
        
    def play_pause_tone(self):
        os.system("mpg321 " + self.pause_file + " &")
        
    def play_skip_tone(self):
        os.system("mpg321 " + self.skip_file + " &")
    
    def play_boot_tone(self):
        os.system("mpg321 " + self.boot_file + " &")
        