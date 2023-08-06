class Flow(object):
	"""State.Flow class
	
	Request for the traffic generator to move flows to a specific state.
	"""
	def __init__(self, state, flows):
		self.state = state
		self.flows = flows
