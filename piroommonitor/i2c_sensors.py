from functools import reduce

from .sensors import Amg8833, Bme680, Bmp180, Si7021, Tcs34725, Tsl2561, get_online_i2c_devices

class I2CSensors(object):
	supported_sensors = [Amg8833, Bmp180, Si7021, Tcs34725, Tsl2561, Bme680]

	def __init__(self, compensate=[]):
		detected_sensors = [sensor for sensor in I2CSensors.supported_sensors if sensor.address in get_online_i2c_devices()]

		self.__compensate = compensate
		self.__sensors = []
		for sensor in detected_sensors:
			try:
				self.__sensors.append(sensor())
			except:
				pass

		if len(self.__sensors) == 0:
			raise RuntimeError("No online supported sensors found")

	@property
	def text(self):
		data = ""
		for sensor in self.__sensors:
			data += str(sensor) + "\n"
		return data[:-1]

	@property
	def topic(self):
		fields = list(set(reduce(
			(lambda a,b: a + b),
			(list(sensor.units.keys()) for sensor in self.__sensors)
		)))

		units_d = reduce(
			(lambda a,b: {**a, **b}),
			(sensor.units for sensor in self.__sensors)
		)

		units = [{"field": key, "unit": units_d[key]} for key in units_d]
		summary = [{"field": key, "method": "latest"} for key in units_d]
		visualization = [{"field": key, "method": "line"} for key in units_d]

		return {
			"name": "Pi Room Monitor",
			"type_str": "piroommonitor",
			"description": "Raspberry Pi pushing indoor weather data.",
			"fields": fields,
			"units": units,
			"summary": summary,
			"visualization": visualization
		}

	@property
	def data(self):
		combined = reduce(
			(lambda a,b: {**a, **b}),
			(sensor.data for sensor in self.__sensors)
		)

		for field, value in self.__compensate:
			try:
				combined[field] += float(value)
			except Exception:
				pass

		return combined

if __name__ == "__main__":
	sensors = I2CSensors()
	print(sensors.data)
