from adafruit_tcs34725 import TCS34725

from ._i2c_utils import get_busio_i2c

class Tcs34725(TCS34725):
	address = 0x29

	def __init__(self):
		super().__init__(get_busio_i2c())

	@property
	def data(self):
		rgb = self.color_rgb_bytes
		return {
			"color_r": rgb[0],
			"color_g": rgb[1],
			"color_b": rgb[2]
		}

	@property
	def units(self):
		return {
			"color_r": None,
			"color_g": None,
			"color_b": None
		}
