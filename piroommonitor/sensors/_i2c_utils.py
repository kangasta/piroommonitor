try:
	import board, busio
except NotImplementedError:
	# Let's assume we are here because of we are running unittests on non-supported host.
	pass

def get_busio_i2c():
	return busio.I2C(board.SCL, board.SDA)

def get_online_i2c_devices():
	return get_busio_i2c().scan()
