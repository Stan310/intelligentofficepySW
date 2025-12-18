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

    @patch.object(IntelligentOffice, "change_servo_angle")
    @patch.object(SDL_DS3231, "read_datetime")
    def test_open_blinds_at_8_on_weekday(self, mock_rtc: Mock, mock_servo: Mock):
        mock_rtc.return_value = datetime(2025, 12, 18, 8, 0,0)
        office = IntelligentOffice()
        office.blinds_open = False
        office.manage_blinds_based_on_time()
        mock_servo.assert_called_once_with(12)
        self.assertTrue(office.blinds_open)

    @patch.object(IntelligentOffice, "change_servo_angle")
    @patch.object(SDL_DS3231, "read_datetime")
    def test_close_blinds_at_20_on_weekday(self, mock_rtc: Mock, mock_servo: Mock):
        mock_rtc.return_value = datetime(2025, 12, 18, 20, 0,0)
        office = IntelligentOffice()
        office.blinds_open = True
        office.manage_blinds_based_on_time()
        mock_servo.assert_called_once_with(2)
        self.assertFalse(office.blinds_open)

    @patch.object(IntelligentOffice, "change_servo_angle")
    @patch.object(SDL_DS3231, "read_datetime")
    def test_blinds_closed_after_20_on_weekday(self, mock_rtc: Mock, mock_servo: Mock):
        mock_rtc.return_value = datetime(2025, 12, 18, 21, 0,0)
        office = IntelligentOffice()
        office.blinds_open = False
        office.manage_blinds_based_on_time()
        mock_servo.assert_not_called()
        self.assertFalse(office.blinds_open)

    @patch.object(IntelligentOffice, "change_servo_angle")
    @patch.object(SDL_DS3231, "read_datetime")
    def test_weekend_blinds_remain_closed(self, mock_rtc: Mock, mock_servo: Mock):
        mock_rtc.return_value = datetime(2025, 12, 20, 9, 0,0)
        office = IntelligentOffice()
        office.blinds_open = False
        office.manage_blinds_based_on_time()
        mock_servo.assert_not_called()
        self.assertFalse(office.blinds_open)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "output")
    def test_light_level_lower_than_500(self, mock_led: Mock, mock_lux: Mock):
        mock_lux.return_value = 499
        office = IntelligentOffice()
        office.light_on = False
        office.manage_light_level()
        mock_led.assert_called_once_with(office.LED_PIN, True)
        outcome = office.light_on
        self.assertTrue(outcome)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "output")
    def test_light_level_higher_than_550(self, mock_led: Mock, mock_lux: Mock):
        mock_lux.return_value = 551
        office = IntelligentOffice()
        office.light_on = True
        office.manage_light_level()
        mock_led.assert_called_once_with(office.LED_PIN, False)
        outcome = office.light_on
        self.assertFalse(outcome)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "output")
    def test_light_level_higher_than_550_light_already_off(self, mock_led: Mock, mock_lux: Mock):
        mock_lux.return_value = 551
        office = IntelligentOffice()
        office.light_on = False
        office.manage_light_level()
        mock_led.assert_not_called()
        outcome = office.light_on
        self.assertFalse(outcome)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "output")
    def test_light_level_lower_than_500_light_already_on(self, mock_led: Mock, mock_lux: Mock):
        mock_lux.return_value = 499
        office = IntelligentOffice()
        office.light_on = True
        office.manage_light_level()
        mock_led.assert_not_called()
        outcome = office.light_on
        self.assertTrue(outcome)

    @patch.object(IntelligentOffice, "check_quadrant_occupancy")
    @patch.object(GPIO, "output")
    def test_not_occupied_but_light_on(self, mock_led: Mock, mock_check_quadrant_occupancy: Mock):
        mock_check_quadrant_occupancy.side_effect = [False, False, False, False]
        office = IntelligentOffice()
        office.light_on = True
        office.manage_light_level()
        mock_led.assert_called_once_with(office.LED_PIN, GPIO.LOW)
        self.assertFalse(office.light_on)

    @patch.object(IntelligentOffice, "check_quadrant_occupancy")
    @patch.object(GPIO, "output")
    def test_occupied_but_light_off(self, mock_led: Mock, mock_check_quadrant_occupancy: Mock):
        mock_check_quadrant_occupancy.side_effect = [True, False, False, False]
        office = IntelligentOffice()
        office.light_on = False
        office.manage_light_level()
        mock_led.assert_called_once_with(office.LED_PIN, GPIO.HIGH)
        self.assertTrue(office.light_on)

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_gas_detected(self, mock_gas_sensor: Mock, mock_buzzer: Mock):
        mock_gas_sensor.return_value = False
        office = IntelligentOffice()
        office.monitor_air_quality()
        mock_buzzer.assert_called_once_with(36, True)
        self.assertTrue(office.buzzer_on)

    @patch.object(GPIO, "output")
    @patch.object(GPIO, "input")
    def test_gas_not_detected(self, mock_gas_sensor: Mock, mock_buzzer: Mock):
        mock_gas_sensor.return_value = True
        office = IntelligentOffice()
        office.monitor_air_quality()
        mock_buzzer.assert_called_once_with(36, False)
        self.assertFalse(office.buzzer_on)