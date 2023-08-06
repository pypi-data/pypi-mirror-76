class Device(object):
	"""Emulated.Device class
	
	An abstract container for emulated protocols.
	"""
	def __init__(self, name, devices_per_port, parent, protocols):
		self.name = name
		self.devices_per_port = devices_per_port
		self.parent = parent
		self.protocols = protocols
