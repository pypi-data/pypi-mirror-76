class Ethernet(object):
	"""Flow.Ethernet class
	
	Ethernet packet header
	"""
	def __init__(self, dst, src, ether_type):
		if isinstance(dst, StringPattern) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be of type StringPattern')
		if isinstance(src, StringPattern) is True:
			self.src = src
		else:
			raise TypeError('src must be of type StringPattern')
		if isinstance(ether_type, StringPattern) is True:
			self.ether_type = ether_type
		else:
			raise TypeError('ether_type must be of type StringPattern')
