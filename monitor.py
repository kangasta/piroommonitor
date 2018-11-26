from time import sleep
from datetime import datetime

from _bmp180 import Bmp180
from pi_hcsr501 import HcSr501
from pi_si7021 import Si7021
from _tsl2561 import Tsl2561

from fdbk import ClientConnection

class Sensors(object):
	def __init__(self):
		self.sensors = [Bmp180(), Si7021(), Tsl2561()]

	def get_data(self):
		data = ""
		for sensor in self.sensors:
			data += str(sensor) + "\n"
		return data

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

print("Initializing")

sensors = Sensors()
c = ClientConnection("http://192.168.1.34:8080")

try:
	c.addTopic(
		"Room monitor",
		"IoT",
		"Raspberry Pi pushing data from I2C sensor boards.",
		["temperature", "humidity", "pressure", "luminosity"],
		["celsius", "percent", "pascal", "lux"],
		[
			{"field":"temperature", "method":"latest"},
			{"field":"humidity", "method":"latest"},
			{"field":"pressure", "method":"latest"},
			{"field":"luminosity", "method":"latest"}
		],
		[
			{"field":"temperature", "method":"line"},
			{"field":"humidity", "method":"line"},
			{"field":"pressure", "method":"line"},
			{"field":"luminosity", "method":"line"}
		]
	)
except:
	pass

print("Start pushing data")

try:
	while True:
		c.addData("Room monitor", sensors.json)
		sleep(5)
except KeyboardInterrupt:
	pass

print("Stop pushing data")

sensors.close()
