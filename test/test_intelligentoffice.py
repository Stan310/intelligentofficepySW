import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_1_yes(self, infrared_sensor1: Mock):
        infrared_sensor1.return_value = True
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy()
        self.assertTrue(outcome)