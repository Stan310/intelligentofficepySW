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
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN1)
        self.assertTrue(outcome)

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_1_no(self, infrared_sensor1: Mock):
        infrared_sensor1.return_value = False
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN1)
        self.assertFalse(outcome)

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_2_yes(self, infrared_sensor2: Mock):
        infrared_sensor2.return_value = True
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN2)
        self.assertTrue(outcome)

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_2_no(self, infrared_sensor2: Mock):
        infrared_sensor2.return_value = False
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN2)
        self.assertFalse(outcome)


    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_3_yes(self, infrared_sensor3: Mock):
        infrared_sensor3.return_value = True
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN3)
        self.assertTrue(outcome)

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_3_no(self, infrared_sensor3: Mock):
        infrared_sensor3.return_value = False
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN3)
        self.assertFalse(outcome)

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_4_yes(self, infrared_sensor4: Mock):
        infrared_sensor4.return_value = True
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN4)
        self.assertTrue(outcome)

    @patch.object(GPIO, "input")
    def test_occupancy_quadrant_4_no(self, infrared_sensor4: Mock):
        infrared_sensor4.return_value = False
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN4)
        self.assertFalse(outcome)

    @patch.object(GPIO, "input")
    def test_false_test_occupancy_quadrant_5_nonexistent_should_fail(self, infrared_sensor5: Mock):
        infrared_sensor5.return_value = True
        office = IntelligentOffice()
        outcome = office.check_quadrant_occupancy(office.INFRARED_PIN5)
        self.assertTrue(outcome)
