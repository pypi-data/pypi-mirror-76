class Actual(object):
	"""State.Actual class
	
	The desired and actual state of the traffic generator
	"""
	def __init__(self, states, flow, capture):
		self.states = states
		self.flow = flow
		self.capture = capture
