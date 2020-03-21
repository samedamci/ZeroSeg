#!/usr/bin/env python

import ZeroSeg.led as led
import time
from datetime import datetime

def clock(device, deviceId, seconds):

    for _ in range(seconds):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        #dot = second % 2 == 0                # calculate blinking dot
        # Set hours
        device.letter(deviceId, 8, int(hour / 10))     # Tens
        device.letter(deviceId, 7, hour % 10)     # Ones
        device.letter(deviceId, 6, '.')                # dot
        # Set minutes
        device.letter(deviceId, 5, int(minute / 10))   # Tens
        device.letter(deviceId, 4, minute % 10)        # Ones
        device.letter(deviceId, 3, '.')                # dot
        # Set seconds
        device.letter(deviceId, 2, int(second / 10))
        device.letter(deviceId, 1, second % 10)
        time.sleep(1)

device = led.sevensegment()

while True:
    clock(device, 0, seconds=10)
