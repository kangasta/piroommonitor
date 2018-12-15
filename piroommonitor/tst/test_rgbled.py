from unittest import TestCase

try:
	from unittest.mock import ANY, call, MagicMock, patch
except ImportError:
	from mock import ANY, call, MagicMock, patch

import pigpio

from piroommonitor import FRange, RGBLed

class RGBLedTest(TestCase):
	@patch.object(pigpio, 'pi')
	def test_allows_custom_pins(self, mock):
		pi = MagicMock()
		mock.return_value = pi

		pins = [1,2,3]
		rgb = [4,5,6]
		led = RGBLed(*pins)
		led(*rgb)
		pi.set_PWM_dutycycle.has_calls(call(*z) for z in zip(pins, rgb))

	@patch.object(pigpio, 'pi')
	def test_allows_setting_max_brightness(self, mock):
		pi = MagicMock()
		mock.return_value = pi

		brightness = 0.5
		pins = [1,2,3]
		rgb = [4,5,6]
		led = RGBLed(*pins, brightness)
		led(*rgb)
		pi.set_PWM_dutycycle.has_calls(call(*z) for z in zip(pins, (i*brightness for i in rgb)))

class FRangeTest(TestCase):
	def test_checks_given_value_is_in_range(self):
		frange = FRange(0.0, 1.0)
		values = [-0.5, 0.0, 0.5, 1.0, 1.5]
		results = [False, True, True, True, False]
		for value, result in zip(values, results):
			self.assertEqual(frange == value, result)

	def test_supports_indexing(self):
		frange = FRange(0.0, 1.0)
		self.assertEqual(frange[0], 0.5)
		with self.assertRaises(IndexError):
			frange[1]

	def test_has_string_representation(self):
		frange = FRange(0.0, 1.0)
		self.assertEqual(str(frange), "0.0-1.0")
