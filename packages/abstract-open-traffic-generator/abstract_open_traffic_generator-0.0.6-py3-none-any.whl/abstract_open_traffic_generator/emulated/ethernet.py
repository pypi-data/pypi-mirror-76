class Ethernet(object):
	"""Emulated.Ethernet class
	
	Emulated ethernet protocol
	"""
	def __init__(self, name, mac, mtu):
		self.name = name
		self.mac = mac
		self.mtu = mtu
