class PortPattern(object):
	"""Flow.PortPattern class
	
	A pattern that is applied to a test port
	The name of the pattern will be reflected in the port results.
	"""
	def __init__(self, name, offset, pattern, mask):
		self.name = name
		self.offset = offset
		self.pattern = pattern
		self.mask = mask
