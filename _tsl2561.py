from tsl2561 import TSL2561

class Tsl2561(TSL2561):
	@property
	def luminosity(self):
		return self.lux()

	def __str__(self):
		ret = "Illuminance: " + str(self.luminosity) + " lx"
		return ret

if __name__ == "__main__":
	LUX = Tsl2561()
	print(str(LUX))
