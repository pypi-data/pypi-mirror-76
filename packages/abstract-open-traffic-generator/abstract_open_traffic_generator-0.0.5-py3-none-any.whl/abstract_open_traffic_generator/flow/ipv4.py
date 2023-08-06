class Ipv4(object):
	"""Flow.Ipv4 class
	
	Ipv4 packet header
	"""
	def __init__(self, priority, src, dst):
		if isinstance(priority, Priority) is True:
			self.priority = priority
		else:
			raise TypeError('priority must be of type Priority')
		if isinstance(src, StringPattern) is True:
			self.src = src
		else:
			raise TypeError('src must be of type StringPattern')
		if isinstance(dst, StringPattern) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be of type StringPattern')
