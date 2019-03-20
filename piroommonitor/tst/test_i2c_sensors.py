from unittest import TestCase

try:
	from unittest.mock import ANY, call, MagicMock, patch
except ImportError:
	from mock import ANY, call, MagicMock, patch

import pigpio

import piroommonitor
from piroommonitor import I2CSensors, sensors

class I2CSensorsTest(TestCase):
	class MockFailingBme680(sensors.Bme680):
		def __init__(self):
			raise Exception('Error from mock')

	class MockBme680(sensors.Bme680):
		def __init__(self):
			pass

		@property
		def temperature(self):
			return 21

		@property
		def humidity(self):
			return 40

		@property
		def pressure(self):
			return 1013

		@property
		def gas(self):
			return 2000000

	@patch.object(I2CSensors, 'supported_sensors', [MockFailingBme680])
	@patch('piroommonitor.i2c_sensors.get_online_i2c_devices')
	def test_raises_runtime_error_when_no_supported_devices_found(self, i2c_mock):
		i2c_mock.return_value = [0x77]

		with self.assertRaises(RuntimeError):
			I2CSensors()

	@patch.object(I2CSensors, 'supported_sensors', [MockBme680])
	@patch('piroommonitor.i2c_sensors.get_online_i2c_devices')
	def test_provides_mandatory_properties(self, i2c_mock):
		i2c_mock.return_value = [0x77]

		sensors = I2CSensors()
		topic = sensors.topic
		data = sensors.data

		self.assertEqual(
			set(topic['fields']),
			set([
				'temperature',
				'humidity',
				'air_quality_resistance',
				'pressure'
			])
		)

		self.assertEqual(
			set(data),
			set({
				'temperature': 21,
				'humidity': 40,
				'air_quality_resistance': 2000000,
				'pressure': 1013
			})
		)
