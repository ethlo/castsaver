# castsaver
Chromecast "screen-saver"

The idea is that whenever the chromecast is in Backdrop mode (slides, but unfortunately with clock and text overlayed) or a supported app is idle/paused for too long, then start the default player with random media from media.txt. 

(I needed a simple app that takes over when nothing else is playing. I have a plasma TV, and it is not very happy about non-moving images over time ;-)

##Issues
* Cannot check media status of HBO Nordic (encrypted?)
* Cannot check media status of NetFlix (encrypted)
* Not the cleanest code ;-)

##Credits
PyChromecast - https://github.com/balloob/pychromecast for writing a nice library for interfacing with the Chromecast API
