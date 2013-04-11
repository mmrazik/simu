from testtools import TestCase
from testtools.matchers import Equals
from testscenarios import TestWithScenarios
from mock import patch, call
import simo


class TestButtons(TestWithScenarios, TestCase):
    scenarios = [
        ('button_up',
         {'button': simo.BUTTON_UP}),
        ('button_down',
         {'button': simo.BUTTON_DOWN}),
        ('button_stop',
         {'button': simo.BUTTON_STOP}),
        ('button_channel_select',
         {'button': simo.BUTTON_CHANNEL_SELECT})
    ]

    @patch('simo.simo.time.sleep')
    @patch('simo.simo.press_button')
    @patch('simo.simo.release_button')
    def test_push_button(self, release_mock, press_mock, sleep_mock):
        simo.push_button(self.button)
        self.assertThat(press_mock.call_args_list,
                        Equals([call(self.button)]))
        self.assertThat(sleep_mock.call_args_list,
                        Equals([call(simo.BUTTON_PRESS_TIME)]))
        self.assertThat(release_mock.call_args_list,
                        Equals([call(self.button)]))

    @patch('simo.simo.GPIO.output')
    @patch('simo.simo.init')
    def test_press_button(self, init_mock, output_mock):
        output_mock.reset_mock()
        simo.press_button(self.button)
        self.assertThat(output_mock.call_args_list,
                        Equals([call(self.button, True)]))

    @patch('simo.simo.GPIO.output')
    @patch('simo.simo.init')
    def test_release_button(self, init_mock, output_mock):
        output_mock.reset_mock()
        simo.release_button(self.button)
        self.assertThat(output_mock.call_args_list,
                        Equals([call(self.button, False)]))
