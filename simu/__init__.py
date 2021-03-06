__name__ = 'simu'
__version__ = '0.2'
__author__ = 'Martin Mrazik'

# how many seconds does it take to release a button during push
BUTTON_PRESS_TIME = 0.15
BUTTON_UP = 13
BUTTON_DOWN = 16
BUTTON_STOP = 15
BUTTON_CHANNEL_SELECT = 18

CHANNEL_FILE = '/etc/simu/simu.channel'

CHANNEL_ROOMS = 1
CHANNEL_KITCHEN = 2
CHANNEL_BIG_WINDOWS = 3
CHANNEL_DOORS = 4
CHANNEL_ALL = 5

from .simu import (push_button, press_button, release_button, up,
                   down, stop, channel_operation)
# suppressing pyflakes warning
assert (push_button, press_button, release_button, up, down, stop,
        channel_operation)
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
buttons = [BUTTON_UP, BUTTON_DOWN, BUTTON_STOP, BUTTON_CHANNEL_SELECT]
for button in buttons:
    GPIO.setup(button, GPIO.OUT)
    GPIO.output(button, False)
