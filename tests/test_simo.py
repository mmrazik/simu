from testtools import TestCase
from testscenarios import TestWithScenarios
from mock import patch
import simo.simo as simo


class TestButtons(TestCase, TestWithScenarios):
    scenarios = [
        ('button_up',
         {'button': simo.BUTTON_UP} ) 
    ]

    @patch('simo.time.sleep')
    @patch('simo.press_button')
    @patch('simo.release_button')
    def test_push_button(self, release_mock, press_mock, sleep_mock):
        simo.push_button()
    
      
