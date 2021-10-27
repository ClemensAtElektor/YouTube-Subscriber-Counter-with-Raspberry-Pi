#!/usr/bin/env python

"""
Raspberry Pi Youtube Counter for Elektor TV Channel

elektor.tv

Helped me:
http://stackoverflow.com/questions/36252027/how-to-use-youtube-api-v3-for-realtime-subscribers
https://max7219.readthedocs.io/en/latest/
http://raspi.tv/2013/8-x-8-led-array-driven-by-max7219-on-the-raspberry-pi-via-python
http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/
http://raspberrypi.stackexchange.com/questions/8734/execute-script-on-start-up
"""
#import RPi.GPIO as GPIO
import math
import os
import sys

import httplib2
import json
from urllib.request import urlopen

import time
from datetime import datetime

import random
import socket

from select import select

# Needed to get MAX7219 support
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

# Channel ID and API key, get them from your YouTube channel.
channel_id = "my channel id"
api_key = "my API key"
lookup_url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + api_key

#Change brightness here
#brightness = 1


def is_connected():
	try:
		host = socket.gethostbyname("www.google.com")
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False

def date(display):
	now = datetime.now()
	display.text = now.strftime("%d-%m-%y")

def clock(display,seconds):
	interval = 0.5
	for i in range(int(seconds/interval)):
		now = datetime.now()
		if i%2==0:
			display.text = now.strftime("%H_%M_%S")
		else:
			display.text = now.strftime("%H %M %S")
		time.sleep(interval)

def show_message_vp(device, msg, delay=0.1):
	# Implemented with virtual viewport
	width = device.width
	padding = " " * width
	msg = padding + msg + padding
	n = len(msg)

	virtual = viewport(device, width=n, height=8)
	sevensegment(virtual).text = msg
	for i in reversed(list(range(n - width))):
		virtual.set_position((i, 0))
		time.sleep(delay)
        
def main():
	# create seven segment device
	serial = spi(port=0,device=0,gpio=noop())
	device = max7219(serial,cascaded=1)
	display = sevensegment(device)

	#display = led.sevensegment(cascaded=1)
	
	#display.brightness(brightness_setting)
	#display.clear()
	display.text = "  ----  "
	
	while 1:
		show_message_vp(device,"ELEKtor TV SubScribErS",0.2)
		date(display)
		time.sleep(3)
		try:
			# Catches the webpage from google
			soup = urlopen(lookup_url)
			markup = soup.read()
			
			# Access the part of the JSON object that we care about
			feed_json = json.loads(markup)
			sub_count = feed_json["items"][0]["statistics"]["subscriberCount"]

			# Tells us how great we are (writes to display)
			if len(sub_count)>8:
				sub_count = "99999999"
			padding = " " * (8-len(sub_count))
			display.text = padding + sub_count
			print(sub_count)

		except:
			# If can't get new number, screen goes blank
			# display.clear()
			display.text = "Error"
			print("some exception happened")
			
		#time.sleep(1)
		time.sleep(5)
		clock(display,seconds=10)

if __name__ == '__main__':
	main()
