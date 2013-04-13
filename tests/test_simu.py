from testtools import TestCase
from testtools.matchers import Equals
from testscenarios import TestWithScenarios
from mock import patch, call
import simu


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
    @patch('simu.simu.init')
    def test_press_button(self, init_mock, output_mock):
        output_mock.reset_mock()
        simu.press_button(self.button)
        self.assertThat(output_mock.call_args_list,
                        Equals([call(self.button, True)]))

    @patch('simu.simu.GPIO.output')
    @patch('simu.simu.init')
    def test_release_button(self, init_mock, output_mock):
        output_mock.reset_mock()
        simu.release_button(self.button)
        self.assertThat(output_mock.call_args_list,
                        Equals([call(self.button, False)]))
