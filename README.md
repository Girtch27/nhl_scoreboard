# NHL Scoreboard
Scoreboard for your fav NHL team.
Thanks to nhl_goal_light

## Overview

NHL Scoreboard written in python3 for raspberry pi GPIO. Works with any team but currently hardcoded...

To start application, use following commands:
	
    $ sudo python3 NHL_Scoreboard.py

***
### Materials

For documentation on how to wire the GPIOs with the lights and the button, pleaser refer to the "docs" folder.

* Raspberry Pi (currently using raspberry pi A model, but any model will work)
* Red Rotating Beacon Warning Light from ebay
* 5V 2 Channel Relay Module from ebay
* Momentary OFF ON Push Round Button
* 12V to 5V 1A adapter (used a car usb adapter) would be good to have a dual usb adapter in case you need to plug something else like a usb speaker.
* 3.5mm audio extension cable

***
### Audio

If you wish to change the audio clips to sounds with your teams goal horn and music, just download them, rename them (goal_horn_#.mp3) and save them in the "audio" folder.

***
### Delay
Not used, if needed will update.
I've teste my code while watching Rogers Gamecenter Live and the stream seems to be a bit delayed, so I added a delay to my code to make the goal horn start later. You will be prompted to enter a delay that works with your stream.

### Credit
Thank you to dword4/nhlapi for documenting the public NHL API
