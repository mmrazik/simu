import logging
import json
import re
from datetime import datetime, timedelta
import time
from . import (CHANNEL_KITCHEN, BUTTON_STOP, CHANNEL_BIG_WINDOWS, BUTTON_DOWN,
               BUTTON_UP)
import simu

LOGFILE = '/var/log/simu.log'
DARKNESS_JSON = '/home/mmrazik/weather/data/live_darkness_json.txt'
TIME_THRESHOLD = timedelta(seconds=30 * 60)
DARKNESS_THRESHOLD_DOWN = 60.0
DARKNESS_THRESHOLD_UP = 60.0

DARKNESS_THRESHOLDS = {
    'kitchen': {
        'threshold_up': 60.0,
        'threshold_down': 60.0,
        'channel': CHANNEL_KITCHEN,
        'operation_down': BUTTON_STOP,
    },
    'big_windows': {
        'threshold_up': 200.0,
        'threshold_down': 200.0,
        'channel': CHANNEL_BIG_WINDOWS,
        'operation_down': BUTTON_DOWN,
    },
}


logging.basicConfig(filename=LOGFILE,
                    format='%(levelname)s:%(asctime)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


def get_last_action(channel):
    try:
        lines = open(LOGFILE, 'r').readlines()
    except IOError as error:
        logging.error(error)
        return None, None

    for line in reversed(lines):
        regexp = '^INFO:(.*):%s (up|down)' % channel
        match = re.search(regexp, line)
        if match:
            event_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            time_delta = datetime.now() - event_time
            return time_delta, match.group(2)
    return None, None


def get_current_darkness():
    try:
        raw_data = open(DARKNESS_JSON, 'r').read()
    except IOError as detail:
        logging.error("Unable to open darkness file: %s" % detail)
        return None

    data = json.loads(raw_data)
    return float(data['Darkness'])


def check_status():
    darkness = get_current_darkness()
    if darkness is None:
        logging.error("Unable to acquire darkness. Giving up.")
        return False

    for channel_name in DARKNESS_THRESHOLDS:
        time_delta, event_type = get_last_action(channel_name)
        if time_delta is None:
            time_delta = TIME_THRESHOLD + timedelta(0, 1)
        channel_config = DARKNESS_THRESHOLDS[channel_name]
        if darkness > channel_config['threshold_down']:
            if time_delta > TIME_THRESHOLD and event_type != 'down':
                logging.info(
                    '%s down (darkness %s)' % (channel_name, darkness))
                simu.channel_operation(channel_config['channel'],
                                       channel_config['operation_down'])
        elif darkness < channel_config['threshold_up']:
            if time_delta > TIME_THRESHOLD and event_type != 'up':
                logging.info(
                    '%s up (darkness %s)' % (channel_name, darkness))
                simu.channel_operation(channel_config['channel'],
                                       BUTTON_UP)
        time.sleep(0.5)
