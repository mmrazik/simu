import time
import RPi.GPIO as GPIO
from .socketlock import SocketLock
from . import (BUTTON_PRESS_TIME, BUTTON_UP, BUTTON_DOWN, BUTTON_STOP,
               BUTTON_CHANNEL_SELECT, CHANNEL_FILE)

class Channel():
    _channel_file = None

    def __init__(self, channel_file=CHANNEL_FILE):
        self._channel_file = channel_file

    def get_channel(self):
        try:
            fd = open(self._channel_file, 'r')
            channel = fd.readline()
            channel = int(channel)
            if channel >= 1 and channel <= 5:
                return channel
            else:
                return None
        except IOError:
            return None
        except ValueError:
            return None

    def write_channel(self, channel):
        if channel < 1 or channel > 5:
            return False
        try:
            fd = open(self._channel_file, 'w')
            channel = fd.write('{}'.format(channel))
            fd.close()
            return True
        except IOError:
            return False


def push_button(button):
    press_button(button)
    time.sleep(BUTTON_PRESS_TIME)
    release_button(button)


def press_button(button):
    GPIO.output(button, True)


def release_button(button):
    GPIO.output(button, False)


def channel_operation(channel, button):
    if channel < 1 or channel > 5:
        return False

    lock = SocketLock('simu.channel_operation')
    lock.acquire()
    ch = Channel()
    if ch.get_channel() == channel:
        ret = push_button(button)
    else:
        _channel_up(channel - ch.get_channel())
        ret = push_button(button)
    lock.release()
    return ret


def up(channel):
    return channel_operation(channel, BUTTON_UP)

def down(channel):
    return channel_operation(channel, BUTTON_DOWN)

def stop(channel):
    return channel_operation(channel, BUTTON_STOP)

def _channel_up(number_of_channels):
    # this method expects a button is pressed afterwards which is 
    # different from the BUTTON_CHANNEL_SELECT. There needs to be a 5 
    # seconds sleep between subsequent calls of this method otherwise.
    if number_of_channels < 0:
        number_of_channels = number_of_channels + 5
    ch = Channel() 

    # first push just shows the current channel
    push_button(BUTTON_CHANNEL_SELECT)
    time.sleep(0.2)

    while number_of_channels > 0:
        push_button(BUTTON_CHANNEL_SELECT)
        time.sleep(0.2)
        number_of_channels = number_of_channels - 1
        current_channel = ch.get_channel() + 1
        if current_channel > 5:
            current_channel = current_channel % 5
        ch.write_channel(current_channel)
