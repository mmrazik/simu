import time
import RPi.GPIO as GPIO
from . import (BUTTON_PRESS_TIME, BUTTON_UP, BUTTON_DOWN, BUTTON_STOP,
               BUTTON_CHANNEL_SELECT, CHANNEL_FILE)


initialized = False


def init():
    global initialized
    if initialized:
        return
    GPIO.setmode(GPIO.BOARD)
    buttons = [BUTTON_UP, BUTTON_DOWN, BUTTON_STOP, BUTTON_CHANNEL_SELECT]
    for button in buttons:
        GPIO.setup(button, GPIO.OUT)
        GPIO.output(button, False)
    initialized = True


def push_button(button):
    press_button(button)
    time.sleep(BUTTON_PRESS_TIME)
    release_button(button)


def press_button(button):
    init()
    GPIO.output(button, True)


def release_button(button):
    init()
    GPIO.output(button, False)


def up(channel):
    pass


def down(channel):
    pass


def stop(channel):
    pass


def channel_up():
    pass
