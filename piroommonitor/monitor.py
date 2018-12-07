import json
from time import sleep
from datetime import datetime
from argparse import ArgumentParser

from piroommonitor import Sensors

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
			self.__topic_id = self.__client.addTopic(**self.__sensors.topic)
		except Exception as e:
			print("Received error: " + str(e))

	def start(self):
		try:
			while True:
				data = self.__sensors.data
				for key in data:
					data[key] = 0

				for _ in range(self.__num_samples):
					sample = self.__sensors.data
					for key in sample:
						data[key] += sample[key]/self.__num_samples
					sleep(self.__interval/self.__num_samples)

				try:
					self.__client.addData(self.__topic_id, data)
				except Exception as e:
					print("Received error: " + str(e))

				if self.__verbose:
					print("Push:\n" + json.dumps(data, indent=2, sort_keys=True))
		except KeyboardInterrupt:
			pass
