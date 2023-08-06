class DeviceEndpoint(object):
	"""Flow.DeviceEndpoint class
	
	An endpoint that contains 1..n emulated transmit devices and 1..n  emulated receive devices.
	"""
	def __init__(self, tx_devices, rx_devices):
		self.tx_devices = tx_devices
		self.rx_devices = rx_devices
