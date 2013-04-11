import RPi.GPIO as GPIO
import time

# how many seconds does it take to release a button during push
BUTTON_PRESS_TIME = 0.5 
BUTTON_UP = 1
BUTTON_DOWN = 2 
BUTTON_STOP = 3
BUTTON_CHANNEL_SELECT = 4

CHANNEL_FILE = '/home/mmrazik/.simo.channel'


def push_button(button):
    press_button(button)
    time.sleep(BUTTON_PRESS_TIME)
    release_button(button)

def press_button(button):
    pass


def release_button(button):
    pass


def up(channel):
    pass

def down(channel):
    pass

def stop(channel):
    pass

def channel_up():
    pass

