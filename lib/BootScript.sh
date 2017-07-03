#! /bin/sh
DISPLAY=:0
sleep 5
sudo su pi -c "chromium-browser --start-maximized"
sleep 10
sudo su pi -c "chromium-browser play.spotify.com"
