from testtools import TestCase
from testtools.matchers import Equals
from testscenarios import TestWithScenarios
from simu import blindersd
from simu import CHANNEL_KITCHEN, BUTTON_STOP, BUTTON_UP
from mock import patch, MagicMock, call
from datetime import datetime, timedelta

class TestGetLastAction(TestWithScenarios, TestCase):
    scenarios = [
        ('kitchen',
         {'channel': 'kitchen',
          'operation': 'up'
         }),
        ('big_windows',
         {'channel': 'big_windows',
          'operation': 'up'
         }),
        ('kitchen',
         {'channel': 'kitchen',
          'operation': 'down'
         }),
        ('big_windows',
         {'channel': 'big_windows',
          'operation': 'down'
         }),

    ]

    @patch('simu.blindersd.open', create=True)
    def test_IOError(self, mock_open):
        # Given
        mock_open.side_effect = IOError()
        # When
        time_delta, event_type = blindersd.get_last_action(self.channel)
        # Then
        self.assertThat(time_delta, Equals(None))
        self.assertThat(event_type, Equals(None))

    @patch('simu.blindersd.open', create=True)
    def test_empty_logfile(self, mock_open):
        logfile_content = []
        mock_open.readlines = lambda: logfile_content
        time_delta, event_type = blindersd.get_last_action(self.channel)
        self.assertThat(time_delta, Equals(None))
        self.assertThat(event_type, Equals(None))

    @patch('simu.blindersd.datetime')
    @patch('simu.blindersd.open', create=True)
    def test_blinders_up(self, mock_open, datetime_mock):
        # Given 
        logfile_content = [
            'INFO:2013-01-04 15:00:00:%s %s' % (self.channel, self.operation)
        ]
        file_mock = MagicMock()
        file_mock.readlines = lambda: logfile_content
        mock_open.return_value = file_mock
        datetime_mock.strptime = datetime.strptime
        datetime_mock.now = lambda: datetime(2013, 1, 4, 16, 0, 0, 0)
        
        # When
        time_delta, event_type = blindersd.get_last_action(self.channel)
        # Then
        self.assertThat(time_delta, Equals(timedelta(0, 3600)))
        self.assertThat(event_type, Equals(self.operation))

    @patch('simu.blindersd.datetime')
    @patch('simu.blindersd.open', create=True)
    def test_with_darkness_in_log(self, mock_open, datetime_mock):
        # Given 
        logfile_content = [
            'INFO:2013-01-04 15:00:00:%s %s (darkness 79.0)' % (self.channel,
                                                              self.operation)
        ]
        file_mock = MagicMock()
        file_mock.readlines = lambda: logfile_content
        mock_open.return_value = file_mock
        datetime_mock.strptime = datetime.strptime
        datetime_mock.now = lambda: datetime(2013, 1, 4, 16, 0, 0, 0)
        
        # When
        time_delta, event_type = blindersd.get_last_action(self.channel)
        # Then
        self.assertThat(time_delta, Equals(timedelta(0, 3600)))
        self.assertThat(event_type, Equals(self.operation))

class TestCheckStatus(TestWithScenarios, TestCase):
    DARKNESS_THRESHOLDS = {
        'kitchen': {
            'threshold_up': 60.0,
            'threshold_down': 60.0,
            'channel': CHANNEL_KITCHEN,
            'operation_down': BUTTON_STOP,
        },
    }

    @patch('simu.blindersd.get_current_darkness', return_value=None)
    def test_no_darkness(self, current_darkness_mock):
        result = blindersd.check_status()
        self.assertThat(result, Equals(False))

    @patch('simu.blindersd.get_current_darkness', new=lambda: 80.0)
    @patch('simu.blindersd.DARKNESS_THRESHOLDS', new=DARKNESS_THRESHOLDS)
    @patch('simu.blindersd.simu.channel_operation')
    @patch('simu.blindersd.get_last_action')
    def test_time_delta_too_small(self, get_last_action_mock,
                                  channel_operation_mock):
        # Given
        get_last_action_mock.return_value = (
            blindersd.TIME_THRESHOLD - timedelta(0, 1), 'up')
        # When
        blindersd.check_status()

        # Then
        self.assertThat(channel_operation_mock.call_count, Equals(0))

    @patch('simu.blindersd.get_current_darkness', new=lambda: 80.0)
    @patch('simu.blindersd.DARKNESS_THRESHOLDS', new=DARKNESS_THRESHOLDS)
    @patch('simu.blindersd.simu.channel_operation')
    @patch('simu.blindersd.get_last_action')
    def test_dark_outside_time_delta_ok_last_action_down(
            self, get_last_action_mock, channel_operation_mock):
        # Given
        get_last_action_mock.return_value = (
            blindersd.TIME_THRESHOLD + timedelta(0, 1), 'down')
        # When
        blindersd.check_status()

        # Then
        self.assertThat(channel_operation_mock.call_count, Equals(0))

    @patch('simu.blindersd.get_current_darkness', new=lambda: 80.0)
    @patch('simu.blindersd.DARKNESS_THRESHOLDS', new=DARKNESS_THRESHOLDS)
    @patch('simu.blindersd.simu.channel_operation')
    @patch('simu.blindersd.get_last_action')
    def test_dark_outside_time_delta_ok_last_action_up(self, 
                                                       get_last_action_mock,
                                                       channel_operation_mock):
        # Given
        get_last_action_mock.return_value = (
            blindersd.TIME_THRESHOLD + timedelta(0, 1), 'up')
        # When
        blindersd.check_status()

        # Then
        channel_operation_mock.assert_has_calls(
            [call(CHANNEL_KITCHEN, BUTTON_STOP)])


    @patch('simu.blindersd.get_current_darkness', new=lambda: 20.0)
    @patch('simu.blindersd.DARKNESS_THRESHOLDS', new=DARKNESS_THRESHOLDS)
    @patch('simu.blindersd.simu.channel_operation')
    @patch('simu.blindersd.get_last_action')
    def test_light_outside_time_delta_ok_last_action_down(
        self, get_last_action_mock, channel_operation_mock):
        # Given
        get_last_action_mock.return_value = (
            blindersd.TIME_THRESHOLD + timedelta(0, 1), 'down')
        # When
        blindersd.check_status()
        # Then
        channel_operation_mock.assert_has_calls(
            [call(CHANNEL_KITCHEN, BUTTON_UP)])
