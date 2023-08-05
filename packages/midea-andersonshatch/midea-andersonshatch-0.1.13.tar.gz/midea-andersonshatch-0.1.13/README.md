This is an updated version of the library component only, from the repo at [NeoAcheron/midea-ac-py](https://github.com/NeoAcheron/midea-ac-py).

So far, the only changes are to handle the session timeout properly. It should recover from an invalidated session or use of your account on another device.

It is used by the home-assistant custom component at [andersonshatch/midea-ac-py](https://github.com/andersonshatch/midea-ac-py)

Original Readme:
# midea-ac-py 

This is a library to allow communicating to a Midea AC via the Midea Cloud.

This is a very early release, and comes without any guarantees. This is still an early work in progress and simply serves as a proof of concept.

This library would not have been possible if it wasn't for the amazing work done by @yitsushi and his Ruby based command line tool. 
You can find his work here: https://github.com/yitsushi/midea-air-condition
The reasons for me converting this to Python is that this library also serves as a platform component for Home Assistant.

## Wiki
Please visit the Wiki for device support and instruction on how to use this component: https://github.com/NeoAcheron/midea-ac-py/wiki 
