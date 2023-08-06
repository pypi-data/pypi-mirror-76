class Increment(object):
	"""Flow.Size.Increment class
	
	Frame size that increments from a starting size to  an ending size incrementing by a step size
	"""
	def __init__(self, start, end, step):
		self.start = start
		self.end = end
		self.step = step
