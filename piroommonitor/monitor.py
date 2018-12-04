import json
from time import sleep
from datetime import datetime
from argparse import ArgumentParser

from sensors import Sensors

from fdbk import ClientConnection

class Monitor(object):
	def __init__(self, sensors, remote_url, interval=360, num_samples=60, verbose=False):
		self.__sensors = sensors
		self.__remote = remote_url
		self.__interval = interval
		self.__num_samples = num_samples
		self.__verbose = verbose

		self.__client = ClientConnection(self.__remote)

		if self.__verbose:
			print("Creating topic 'Room monitor' to fdbk server at '" + self.__remote + "'")

		try:
			self.__client.addTopic(
				"Room monitor",
				type_str="IoT",
				description="Raspberry Pi pushing data from I2C sensor boards.",
				fields=["temperature", "humidity", "pressure", "luminosity"],
				units=[
					{"field": "temperature", "unit": "celsius"},
					{"field": "humidity", "unit": "percent"},
					{"field": "pressure", "unit": "pascal"},
				{"field": "luminosity", "unit": "lux"}
				],
				summary=[
					{"field":"temperature", "method":"latest"},
					{"field":"humidity", "method":"latest"},
					{"field":"pressure", "method":"latest"},
					{"field":"luminosity", "method":"latest"}
				],
				visualization=[
					{"field":"temperature", "method":"line"},
					{"field":"humidity", "method":"line"},
					{"field":"pressure", "method":"line"},
					{"field":"luminosity", "method":"line"}
				]
			)
		except Exception as e:
			print("Received error: " + str(e))

	def start(self):
		try:
			while True:
				data = self.__sensors.json
				for key in data:
					data[key] = 0

				for _ in range(self.__num_samples):
					sample = self.__sensors.json
					for key in sample:
						data[key] += sample[key]/self.__num_samples
					sleep(self.__interval/self.__num_samples)

				try:
					self.__client.addData("Room monitor", data)
				except Exception as e:
					print("Received error: " + str(e))

				if args.verbose:
					print("Push:\n" + json.dumps(data, indent=2, sort_keys=True))
		except KeyboardInterrupt:
			pass

parser = ArgumentParser()
parser.add_argument("remote_url", type=str, help="URL of the fdbk server to push the data to.")
parser.add_argument("--interval", "-i", type=float, default=360.0, help="Data pushing interval in seconds.")
parser.add_argument("--num-samples", "-n", type=int, default=60, help="Number of samples to average during the push interval")
parser.add_argument("--verbose", "-v", action="store_true", help="Be more verbose.")
args = parser.parse_args()

print("Initializing")

sensors = Sensors()
monitor = Monitor(sensors, args.remote_url, args.interval, args.num_samples, args.verbose)

print("Start pushing data")

monitor.start()

print("Stop pushing data")

sensors.close()
