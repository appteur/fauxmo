#!/usr/bin/env python

from lib import *
import sys
import time

# uncomment RPi imports if you are launching or using on a raspberry pi.
# references will need to be uncommented here (line 9 & 70) as well
# as in the Handler.py file (import and gpio class definition).
# import RPi.GPIO as GPIO


# NOTE: As of 2015-08-17, the Echo appears to have a hard-coded limit of
# 16 switches it can control. Only the first 16 elements of the FAUXMOS
# list will be used.


# Provide a list of virtual 'devices' you want to provide control for by
# defining a FAUXMOS array of handlers. Use any handler defined in the
# Handler.py file or define your own.
#
# Each item in the array is a list with the following elements:
# 	- index 0 - name of the virtual switch or device
# 	- index 1 - object with 'on' and 'off' methods
# 	- index 2 - port # (optional; may be omitted)


# Sample array using rest handlers, defined urls will be called when on/off actions are triggered.
# FAUXMOS = [
#     ['office lights', Handler.rest('http://192.168.5.4/ha-api?cmd=on&a=office', 'http://192.168.5.4/ha-api?cmd=off&a=office')],
#     ['kitchen lights', Handler.rest('http://192.168.5.4/ha-api?cmd=on&a=kitchen', 'http://192.168.5.4/ha-api?cmd=off&a=kitchen')],
# ]

# Sample array using gpio handlers. For office lights gpio pin 35 will be turned on/off... etc.
# FAUXMOS = [
#         ['office lights', Handler.gpio(35)],
#         ['kitchen lights', Handler.gpio(37)],
#     ]

# Sample array using file handlers, file handlers specify python files to execute when called.
# 'file' handler expects the name of a script, it should be located in the same directory as
# the 'main.py' file.
# When you say "Alexa, turn on text", the 'sendText.py' script will be executed if implemented
# with your custom behavior.
# FAUXMOS = [
#         ['text', Handler.file("sendText")],
#         ['news', Handler.file("fetchNews")],
#     ]

# Sample array using dummy handlers. For office lights 'officeLight ON' or 'officeLight OFF' will be logged to the console.
FAUXMOS = [
        ['office lights', fmHandler.dummy("officelight"), 52581],
        ['kitchen lights', fmHandler.dummy("kitchenlight"), 52582],
        ['fetch news', fmHandler.file('fetch_news'), 52583]
    ]

# if you run this script with the -d flag, then enable logging for verbosity.
if len(sys.argv) > 1 and sys.argv[1] == '-d':
    fmUtilities.DEBUG = True

# Set up our singleton for polling the sockets for data ready
p = fmPoller.poller()

# Set up our singleton listener for UPnP broadcasts
u = fmResponder.upnp_broadcast_responder()
u.init_socket()

# Add the UPnP broadcast listener to the poller so we can respond
# when a broadcast is received.
p.add(u)

# Create our FauxMo virtual switch devices
for item in FAUXMOS:
    if len(item) == 2:
        # a fixed port wasn't specified, use a dynamic one
        item.append(0)
    switch = fauxmo.fauxmo(item[0], u, p, None, item[2], action_handler = item[1])

# log if enabled
fmUtilities.dbg("Entering main loop\n")

while True:
    try:
        # Allow time for a ctrl-c to stop the process
        p.poll(100)
        time.sleep(0.1)
    except Exception, e:
        # GPIO.cleanup()
        fmUtilities.dbg(e)
        break

