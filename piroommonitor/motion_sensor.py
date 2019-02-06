import RPi.GPIO as GPIO

class MotionSensor(object):
	def __init__(self, pir_pin):
		self.__pin = pir_pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.__pin, GPIO.IN)

	@property
	def topic(self):
		return {
			"name": "Pi Room Monitor (motion)",
			"type_str": "piroommonitor_motion",
			"description": "Raspberry Pi pushing motion data.",
			"fields": ["motion"],
			"units": [
				{"field": "motion", "unit": "binary"}
			],
			"summary": [
				{"field":"motion", "method":"last_truthy"}
			],
			"visualization": [
				{"field":"motion", "method":"line"}
			]
		}

	@property
	def data(self):
		return {
			"motion": GPIO.input(self.__pin)
		}

	def start(self, reporter, rising_cb=None, falling_cb=None):
		self.__reporter = reporter

		def __edge_callback(pin):
			data = self.data
			self.__reporter.push(data)
			if data["motion"] and rising_cb is not None:
				rising_cb()
			elif falling_cb is not None:
				falling_cb()

		__edge_callback(self.__pin)
		GPIO.add_event_detect(self.__pin, edge=GPIO.BOTH, callback=__edge_callback)
