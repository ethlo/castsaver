# castsaver
Chromecast "screen-saver"

The idea is that whenever the chromecast is in Backdrop mode (slides, but unfortunately with clock and text overlayed) or a supported app is idle/paused for too long, then start the default player with random media from 'media.txt'. 

(I needed a simple app that takes over when nothing else is playing. I have a plasma TV, and it is not very happy about non-moving images over time ;-)

## Supported apps
* Default Media Player (and derivatives)
* NRK TV
* TV 2 Sumo

## Setup

```bash
sudo apt-get install python-pip
sudo apt-get install python-dev
```
```bash
pip install netifaces
pip install enum34
pip install pychromecast
```

* Download ```castsaver.py``` and ```castsaver.ini```
* chmod +x castsaver.py
* Enable media resource file (URL per line in file) in ```castsaver.ini``` if you want do define your own media URLs

##Usage
```bash
nohup ./castsaver.py > out.log 2>&1&
````

##Example log
```text
2015-07-27 21:35:23,088 - __main__ - INFO - Dicovered chromecast devices: ['LivingRoom']
2015-07-27 21:35:58,113 - __main__ - INFO - Discovered idle/paused player 1438025758.11
2015-07-27 21:36:03,118 - __main__ - INFO - Discovered active player, resetting idle timer
2015-07-27 21:40:43,329 - __main__ - INFO - Discovered idle/paused player 1438026043.33
2015-07-27 21:41:43,380 - __main__ - INFO - Current application has been idle too long, starting screensaver
```
##Issues
* Cannot check media status of HBO Nordic (encrypted?)
* Cannot check media status of NetFlix (encrypted)
* Not the cleanest code ;-)

##Credits
PyChromecast - https://github.com/balloob/pychromecast for writing a nice library for interfacing with the Chromecast
