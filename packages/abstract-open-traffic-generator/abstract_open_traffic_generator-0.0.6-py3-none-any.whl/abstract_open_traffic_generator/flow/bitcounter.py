class BitCounter(object):
	"""Flow.BitCounter class
	
	An incrementing pattern
	"""
	def __init__(self, offset, length, count, start, step):
		self.offset = offset
		self.length = length
		self.count = count
		self.start = start
		self.step = step
