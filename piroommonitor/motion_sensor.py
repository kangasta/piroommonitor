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
				{"field":"motion", "method":"latest"}
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

	def start(self, reporter):
		self.__reporter = reporter

		def __edge_callback(pin):
			self.__reporter.push(self.data)

		GPIO.add_event_detect(self.__pin, edge=GPIO.BOTH, callback=__edge_callback)
