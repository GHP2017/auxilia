# Auxilia
A server that runs on a Raspberry Pi enabling several users to enjoy a shared music experience.

## Features
* Collaborative Playlist Building -- share your favorite songs with your friends, and discover their music tastes
* Keep The Party Going -- when the queue drops low, songs that fit the mood are added to the playlist, so no user needs to sacrifice time and effort to keep music playing
* User feedback -- Thumbs up/down to influence the flow of the queue

### Hardware Features
* Physical volume and play/pause control
* Sturdy, durable speaker housing

## Getting Started
These instructions will walk you through the steps needed to begin the experience.

### Setup
Let's connect speaker's Raspberry Pi to the same network as the users' devices. 
The Raspberry Pi will host the server running the Auxilia web app, so you'll need to go to this address:
*coming soon*

### Having a Good Time
Here's how it works:
After you search for a song and click "add," the queue automatically updates across all devices and reflects the change.
Upvoting or downvoting can impact the order of songs that are played, or if a song (added by algorithm) accrues a specified number of downvotes, it will delete itself.

## Dependencies
* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) - Websockets
* [Spotify Web API](https://developer.spotify.com/web-api/) - Retrieves data from Spotify's catalog
* [Requests](http://docs.python-requests.org/en/latest/index.html) - HTTP for Humans

## Our Team

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowlegments
* Hats off to the good folks at HackBerry Lab- Zane and Chris- for good advice, good times, and good 3D Printers
* Thanks to Tim for kind suggestions and biting sarcasm
