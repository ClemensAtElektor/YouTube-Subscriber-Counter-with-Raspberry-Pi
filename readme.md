# Raspberry Pi YouTube Subscriber Counter
A [YouTube subscriber counter](https://youtu.be/PuCCMZFNgQE) built with a Raspberry Pi Zero 2 W.

Requires an 8-digit MAX7219-based 7-segment display. Also needs the [luma.led_matrix](https://github.com/rm-hull/luma.led_matrix) and httplib2 libraries.

* youtube-subscriber.py - the main Python3 script
* youtube-subscriber.service - systemd service for making the Python3 script start at boot time.
* The .nc files are G-code files for the "enclosure" (cut out of 3-mm-thick acrylic sheet)

![Alt text](schematic.png?raw=true "Wiring diagram")

![Alt text](subscriber-counter-prototype.jpg?raw=true "Prototype of the YouTube Subscriber Counter")
