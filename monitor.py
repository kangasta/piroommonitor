import json
from time import sleep
from datetime import datetime
from argparse import ArgumentParser

from _bmp180 import Bmp180
from pi_hcsr501 import HcSr501
from pi_si7021 import Si7021
from _tsl2561 import Tsl2561

from fdbk import ClientConnection

class Sensors(object):
	def __init__(self):
		self.sensors = [Bmp180(), Si7021(), Tsl2561()]

	@property
	def text(self):
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

parser = ArgumentParser()
parser.add_argument("remote_url", type=str, help="URL of the fdbk server to push the data to.")
parser.add_argument("--interval", "-n", type=int, default=360, help="Data pushing interval in seconds.")
parser.add_argument("--verbose", "-v", action="store_true", help="Be more verbose.")
args = parser.parse_args()

c = ClientConnection(args.remote_url)

try:
	c.addTopic(
		"Room monitor",
		"IoT",
		"Raspberry Pi pushing data from I2C sensor boards.",
		["temperature", "humidity", "pressure", "luminosity"],
		[
			{"field": "temperature", "unit": "celsius"},
			{"field": "humidity", "unit": "percent"},
			{"field": "pressure", "unit": "pascal"},
			{"field": "luminosity", "unit": "lux"}
		],
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
		data = sensors.json
		c.addData("Room monitor", data)
		if args.verbose:
			print("Push:\n" + json.dumps(data, indent=2, sort_keys=True))
		sleep(args.interval)
except KeyboardInterrupt:
	pass

print("Stop pushing data")

sensors.close()
