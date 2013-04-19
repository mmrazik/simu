import time
import RPi.GPIO as GPIO
from . import (BUTTON_PRESS_TIME, BUTTON_UP, BUTTON_DOWN, BUTTON_STOP,
               BUTTON_CHANNEL_SELECT, CHANNEL_FILE)


initialized = False

class Channel():
    _channel_file = None

    def __init__(self, channel_file=CHANNEL_FILE):
        self._channel_file = channel_file

    def get_channel(self):
        try:
            fd = open(self._channel_file, 'r')
            channel = fd.readline()
            channel = int(channel)
            if channel >= 1 and channel <=5:
                return channel
            else:
                return None
        except IOError:
            return None
        except ValueError:
            return None

    def write_channel(self, channel):
        if channel < 0 or channel > 5:
            return False
        try:
            fd = open(self._channel_file, 'w')
            channel = fd.write('{}'.format(channel))
            fd.close()
            return True
        except IOError:
            return False


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
