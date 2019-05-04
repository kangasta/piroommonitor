from adafruit_amg88xx import AMG88XX

from ._i2c_utils import get_busio_i2c

class Amg8833(AMG88XX):
	address = 0x69

	def __init__(self):
		super().__init__(get_busio_i2c())

	@property
	def data(self):
		return {
			"pixels": self._format_pixels(self.pixels),
			"temperature": self.temperature
		}

	@property
	def units(self):
		return {
			"pixels": "string",
			"temperature": "celsius"
		}

	def _format_pixels(self, grid):
		return ''.join(["%02x" % int(column) for row in grid for column in row])

	def __str__(self):
		ret = "Pixels: " + str(self.pixels) + "\n"
		ret += "Temperature:" + str(self.temperature) + " °C"
		return ret
