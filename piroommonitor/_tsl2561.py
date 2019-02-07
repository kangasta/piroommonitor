from adafruit_tsl2561 import TSL2561

from ._i2c_utils import get_busio_i2c

class Tsl2561(TSL2561):
	def __init__(self):
		super().__init__(get_busio_i2c())

	def __str__(self):
		ret = "Illuminance: " + str(self.lux) + " lx"
		return ret

if __name__ == "__main__":
	LUX = Tsl2561()
	print(str(LUX))
