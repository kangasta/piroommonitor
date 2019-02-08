from adafruit_si7021 import SI7021

from ._i2c_utils import get_busio_i2c

class Si7021(SI7021):
	def __init__(self):
		super().__init__(get_busio_i2c())

	@property
	def address(self):
		return 0x40

	def __str__(self):
		ret = "Temperature: " + str(self.temperature) + " C\n"
		ret += "Humidity: " + str(self.relative_humidity) + " %"
		return ret

if __name__ == "__main__":
	TEMP_RH = Si7021()
	print(str(TEMP_RH))
