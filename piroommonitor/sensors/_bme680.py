from adafruit_bme680 import Adafruit_BME680_I2C

from ._i2c_utils import get_busio_i2c

class Bme680(Adafruit_BME680_I2C):
	address = 0x77

	def __init__(self):
		super().__init__(get_busio_i2c())

	@property
	def data(self):
		return {
			"temperature": self.temperature,
			"humidity": self.humidity,
			"pressure": self.pressure,
			"air_quality_resistance": self.gas
		}

	@property
	def units(self):
		return {
			"temperature": "celsius",
			"humidity": "percent",
			"pressure": "hectopascal",
			"air_quality_resistance": "ohm"
		}

	def __str__(self):
		ret = "Temperature:" + str(self.temperature) + " °C\n"
		ret += "Humidity: " + str(self.humidity) + " %\n"
		ret += "Pressure: " + str(self.pressure) + " hPa\n"
		ret += "Gas: " + str(self.gas) + " Ω"
		return ret
