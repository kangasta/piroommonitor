from ._bmp180 import Bmp180
from ._si7021 import Si7021
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
			"name": "Pi Room Monitor",
			"type_str": "piroommonitor",
			"description": "Raspberry Pi pushing indoor weather data.",
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
			"luminosity": self.sensors[2].lux,
		}

if __name__ == "__main__":
	sensors = Sensors()
	print(sensors.text)
	sensors.close()
