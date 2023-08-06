class Vlan(object):
	"""Emulated.Vlan class
	
	Emulated vlan protocol
	"""
	def __init__(self, name, parent, tpid, priority, id):
		self.name = name
		self.parent = parent
		self.tpid = tpid
		self.priority = priority
		self.id = id
