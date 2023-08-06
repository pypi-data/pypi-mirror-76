class Custom(object):
	"""Flow.Custom class
	
	Custom packet header
	"""
	def __init__(self, bytes, patterns):
		self.bytes = bytes
		self.patterns = patterns
