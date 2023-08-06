class DeviceGroup(object):
	"""Emulated.DeviceGroup class
	
	An abstract container for emulated device containers.
	"""
	def __init__(self, name, ports, devices):
		self.name = name
		self.ports = ports
		self.devices = devices
