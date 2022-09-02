#!/usr/bin/env python
# -*- coding: utf-8 -*-

from RPi_AS3935 import RPi_AS3935
import RPi.GPIO as GPIO
import time
from datetime import datetime
import slackweb

GPIO.setmode(GPIO.BCM)

# Rev. 1 Raspberry Pis should leave bus set at 0, while rev. 2 Pis should set
# bus equal to 1. The address should be changed to match the address of the
# sensor. (Common implementations are in README.md)
sensor = RPi_AS3935(address=0x00, bus=1)

sensor.set_indoors(True)
sensor.set_noise_floor(0)
sensor.calibrate(tun_cap=0x0F)


def handle_interrupt(channel):
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        # ノイズが高杉
        print "Noise level too high - adjusting"
        sensor.raise_noise_floor()
    elif reason == 0x04:
        print "Disturber detected - masking"
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
        # 雷検出
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = sensor.get_distance()
        print "We sensed lightning!"
        print "It was " + str(distance) + "km away. (%s)" % now
        print "---"
        if distance > 1:
            msg = 'We sensed lightning! It was ' + str(distance) + 'km away.'
            message_send(msg)

def message_send(msg):
    url = 'https://hooks.slack.com/services/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'
    slack = slackweb.Slack(url=url)
    slack.notify(text=msg)

pin = 17
#IRQ = 4

GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)
#GPIO.setup(IRQ, GPIO.IN)
#GPIO.add_event_detect(IRQ, GPIO.RISING, callback=handle_interrupt)

print "Waiting for lightning - or at least something that looks like it"

try:
    while True:
        time.sleep(1.0)
except KeyboardInterrupt:
    print 'KeyboardInterrupt キーボードによるキャンセルがありました。'
    pass
