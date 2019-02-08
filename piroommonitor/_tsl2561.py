from adafruit_tsl2561 import TSL2561

from ._i2c_utils import get_busio_i2c

class Tsl2561(TSL2561):
	def __init__(self):
		super().__init__(get_busio_i2c())

	@property
	def address(self):
		return 0x39

	@property
	def lux(self):
		self.gain = 0
		lux = super().lux

		# If no lux value available try with higher gain
		if lux is None:
			self.gain = 1
			lux = super().lux

		# If still no lux value return 0 and reset gain
		if lux is None:
			self.gain = 0
			return 0
		return lux

	def __str__(self):
		ret = "Illuminance: " + str(self.lux) + " lx"
		return ret

if __name__ == "__main__":
	LUX = Tsl2561()
	print(str(LUX))
