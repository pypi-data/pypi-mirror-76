class BitList(object):
	"""Flow.BitList class
	
	A pattern which is a list of values.
	"""
	def __init__(self, offset, length, count, values):
		self.offset = offset
		self.length = length
		self.count = count
		self.values = values
