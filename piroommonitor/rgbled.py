import pigpio
#from time import sleep

class RGBLed(object):
	def __init__(self, r_pin=22, g_pin=23, b_pin=24):
		self.__pins = (r_pin, g_pin, b_pin)
		self.__pi = pigpio.pi()

	def __call__(self, r, g, b):
		rgb = (min(255, max(0, int(i))) for i in (r, g, b))
		for val, pin in zip(rgb, self.__pins):
			self.__pi.set_PWM_dutycycle(pin, val)
