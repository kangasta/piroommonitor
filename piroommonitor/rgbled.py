import pigpio

class FRange(object):
	def __init__(self, _min, _max):
		self.__min = float(_min)
		self.__max = float(_max)

	def __eq__(self, other):
		return other >= self.__min and other <= self.__max

	def __getitem__(self, i):
		if i > 0:
			raise IndexError()
		return self

	def __str__(self):
		return str(self.__min) + "-" + str(self.__max)

class RGBLed(object):
	def __init__(self, r_pin=22, g_pin=23, b_pin=24, brightness=1.0):
		self.__pins = (r_pin, g_pin, b_pin)
		self.__pi = pigpio.pi()
		self.__brightness = brightness

	def __call__(self, r, g, b):
		rgb = (min(255, max(0, int(i*self.__brightness))) for i in (r, g, b))
		for val, pin in zip(rgb, self.__pins):
			self.__pi.set_PWM_dutycycle(pin, val)
