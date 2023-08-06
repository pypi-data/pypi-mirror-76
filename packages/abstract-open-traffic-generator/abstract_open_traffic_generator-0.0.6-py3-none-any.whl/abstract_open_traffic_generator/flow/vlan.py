class Vlan(object):
	"""Flow.Vlan class
	
	Vlan packet header
	"""
	def __init__(self, priority, cfi, id, protocol):
		if isinstance(priority, StringPattern) is True:
			self.priority = priority
		else:
			raise TypeError('priority must be of type StringPattern')
		if isinstance(cfi, StringPattern) is True:
			self.cfi = cfi
		else:
			raise TypeError('cfi must be of type StringPattern')
		if isinstance(id, StringPattern) is True:
			self.id = id
		else:
			raise TypeError('id must be of type StringPattern')
		if isinstance(protocol, StringPattern) is True:
			self.protocol = protocol
		else:
			raise TypeError('protocol must be of type StringPattern')
