from testtools import TestCase
from testtools.matchers import Equals
from testscenarios import TestWithScenarios
from mock import patch, call
import simu
from simu.simu import Channel
import os


class TestChannel(TestCase):
    def test_no_channel_file(self):
        channel = Channel('/non/existen/file')
        self.assertThat(channel.get_channel(), Equals(None))

    def test_with_existing_channel_file(self):
        channel_file = '/tmp/channel'
        channel = 4
        with open(channel_file, 'w') as fd:
            fd.write('{}'.format(channel))
        ch = Channel(channel_file)
        self.assertThat(ch.get_channel(), Equals(channel))
        os.remove(channel_file)

    def test_with_corrupted_channel_file(self):
        channel_file = '/tmp/channel_corrupted'
        channel = 'df'
        with open(channel_file, 'w') as fd:
            fd.write('{}'.format(channel))
        ch = Channel(channel_file)
        self.assertThat(ch.get_channel(), Equals(None))
        os.remove(channel_file)

    def test_with_channel_out_of_range(self):
        channel_file = '/tmp/channel_out_of_range'
        channel = '6'
        with open(channel_file, 'w') as fd:
            fd.write('{}'.format(channel))
        ch = Channel(channel_file)
        ch.channel = 7
        self.assertThat(ch.get_channel(), Equals(None))
        os.remove(channel_file)

    def test_write_channel(self):
        channel_file = '/tmp/test_write_channel'
        channel = '4'
        new_channel = 3
        with open(channel_file, 'w') as fd:
            fd.write('{}'.format(channel))
        ch = Channel(channel_file)
        ret = ch.write_channel(new_channel)
        self.assertThat(ch.get_channel(), Equals(new_channel))
        self.assertThat(ret, Equals(True))
        os.remove(channel_file)

    def test_out_of_bound_channel(self):
        channel_file = '/tmp/test_out_of_bound_channel'
        channel = 4
        new_channel = 7
        with open(channel_file, 'w') as fd:
            fd.write('{}'.format(channel))
        ch = Channel(channel_file)
        ret = ch.write_channel(new_channel)
        self.assertThat(ch.get_channel(), Equals(channel))
        self.assertThat(ret, Equals(False))
        os.remove(channel_file)


class TestButtons(TestWithScenarios, TestCase):
    scenarios = [
        ('button_up',
         {'button': simu.BUTTON_UP}),
        ('button_down',
         {'button': simu.BUTTON_DOWN}),
        ('button_stop',
         {'button': simu.BUTTON_STOP}),
        ('button_channel_select',
         {'button': simu.BUTTON_CHANNEL_SELECT})
    ]

    @patch('simu.simu.time.sleep')
    @patch('simu.simu.press_button')
    @patch('simu.simu.release_button')
    def test_push_button(self, release_mock, press_mock, sleep_mock):
        simu.push_button(self.button)
        self.assertThat(press_mock.call_args_list,
                        Equals([call(self.button)]))
        self.assertThat(sleep_mock.call_args_list,
                        Equals([call(simu.BUTTON_PRESS_TIME)]))
        self.assertThat(release_mock.call_args_list,
                        Equals([call(self.button)]))

    @patch('simu.simu.GPIO.output')
    def test_press_button(self, output_mock):
        output_mock.reset_mock()
        simu.press_button(self.button)
        self.assertThat(output_mock.call_args_list,
                        Equals([call(self.button, True)]))

    @patch('simu.simu.GPIO.output')
    def test_release_button(self, output_mock):
        output_mock.reset_mock()
        simu.release_button(self.button)
        self.assertThat(output_mock.call_args_list,
                        Equals([call(self.button, False)]))
