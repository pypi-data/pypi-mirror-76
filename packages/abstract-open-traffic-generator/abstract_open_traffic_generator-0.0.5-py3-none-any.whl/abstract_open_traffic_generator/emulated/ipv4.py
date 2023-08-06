class Ipv4(object):
	"""Emulated.Ipv4 class
	
	Emulated ipv4 protocol
	"""
	def __init__(self, name, address, gateway, prefix):
		self.name = name
		self.address = address
		self.gateway = gateway
		self.prefix = prefix
