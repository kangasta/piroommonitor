from pi_si7021 import Si7021

from ._bmp180 import Bmp180
from ._tsl2561 import Tsl2561

class Sensors(object):
	def __init__(self):
		self.sensors = [Bmp180(), Si7021(), Tsl2561()]

	@property
	def text(self):
		data = ""
		for sensor in self.sensors:
			data += str(sensor) + "\n"
		return data[:-1]

	@property
	def json(self):
		return {
			"temperature": self.sensors[1].temperature,
			"humidity": self.sensors[1].relative_humidity,
			"pressure": self.sensors[0].pressure,
			"luminosity": self.sensors[2].luminosity,
		}


	def close(self):
		self.sensors[1].close()

if __name__ == "__main__":
	sensors = Sensors()
	print(sensors.text)
	sensors.close()
