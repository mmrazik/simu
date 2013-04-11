__name__ = 'simo'
__version__ = '0.2'
__author__ = 'Martin Mrazik'

# how many seconds does it take to release a button during push
BUTTON_PRESS_TIME = 0.2
BUTTON_UP = 7
BUTTON_DOWN = 11
BUTTON_STOP = 13
BUTTON_CHANNEL_SELECT = 15

CHANNEL_FILE = '/home/mmrazik/.simo.channel'

from .simo import (push_button, press_button, release_button, up,
                   down, stop, channel_up)
