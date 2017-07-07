#! /bin/sh
redis-server --daemonize yes

python3 /home/pi/spotify_dj/server.py &

python3 /home/pi/spotify_dj/playback_master.py &

