

class Config(object):
	"""State.Config class
	
	placeholder
	"""
	def __init__(self, state=None, ports=None, devices=None, flows=None):
		self.state = state
		self.ports = ports
		self.devices = devices
		self.flows = flows


class Flow(object):
	"""State.Flow class
	
	Request for the traffic generator to move flows to a specific state.
	"""
	def __init__(self, state=None, flows=None):
		self.state = state
		self.flows = flows


class Capture(object):
	"""State.Capture class
	
	placeholder
	"""
	def __init__(self, requested_state=None, captures=None):
		self.requested_state = requested_state
		self.captures = captures


class Desired(object):
	"""State.Desired class
	
	The desired state of the traffic generator 
	"""
	def __init__(self, configuration=None, traffic=None, capture=None):
		if isinstance(configuration, (Config, type(None))) is True:
			self.configuration = configuration
		else:
			raise TypeError('configuration must be of type Config')
		if isinstance(traffic, (Flow, type(None))) is True:
			self.traffic = traffic
		else:
			raise TypeError('traffic must be of type Flow')
		if isinstance(capture, (Capture, type(None))) is True:
			self.capture = capture
		else:
			raise TypeError('capture must be of type Capture')


class Actual(object):
	"""State.Actual class
	
	The desired and actual state of the traffic generator
	"""
	def __init__(self, states=None, flow=None, capture=None):
		self.states = states
		self.flow = flow
		self.capture = capture
