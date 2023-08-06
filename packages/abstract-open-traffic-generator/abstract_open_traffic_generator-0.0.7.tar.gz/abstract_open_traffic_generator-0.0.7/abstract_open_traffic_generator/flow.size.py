

class Increment(object):
	"""Flow.Size.Increment class
	
	Frame size that increments from a starting size to  an ending size incrementing by a step size
	"""
	def __init__(self, start=None, end=None, step=None):
		self.start = start
		self.end = end
		self.step = step


class Random(object):
	"""Flow.Size.Random class
	
	Random frame size
	"""
	def __init__(self, min=None, max=None):
		self.min = min
		self.max = max
