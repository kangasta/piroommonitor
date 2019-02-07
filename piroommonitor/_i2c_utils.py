import board, busio

def get_busio_i2c():
	return busio.I2C(board.SCL, board.SDA)