from pi_si7021 import Si7021

from ._bmp180 import Bmp180
from ._tsl2561 import Tsl2561

class I2CSensors(object):
	def __init__(self):
		self.sensors = [Bmp180(), Si7021(), Tsl2561()]

	@property
	def text(self):
		data = ""
		for sensor in self.sensors:
			data += str(sensor) + "\n"
		return data[:-1]

	@property
	def topic(self):
		return {
			"name": "Room monitor",
			"type_str": "IoT",
			"description": "Raspberry Pi pushing data from I2C sensor boards.",
			"fields": ["temperature", "humidity", "pressure", "luminosity"],
			"units": [
				{"field": "temperature", "unit": "celsius"},
				{"field": "humidity", "unit": "percent"},
				{"field": "pressure", "unit": "pascal"},
				{"field": "luminosity", "unit": "lux"}
			],
			"summary": [
				{"field":"temperature", "method":"latest"},
				{"field":"humidity", "method":"latest"},
				{"field":"pressure", "method":"latest"},
				{"field":"luminosity", "method":"latest"}
			],
			"visualization": [
				{"field":"temperature", "method":"line"},
				{"field":"humidity", "method":"line"},
				{"field":"pressure", "method":"line"},
				{"field":"luminosity", "method":"line"}
			]
		}

	@property
	def data(self):
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
