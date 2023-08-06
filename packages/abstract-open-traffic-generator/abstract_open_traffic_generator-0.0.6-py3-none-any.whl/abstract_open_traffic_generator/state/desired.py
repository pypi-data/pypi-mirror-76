class Desired(object):
	"""State.Desired class
	
	The desired state of the traffic generator 
	"""
	def __init__(self, configuration, traffic, capture):
		if isinstance(configuration, Config) is True:
			self.configuration = configuration
		else:
			raise TypeError('configuration must be of type Config')
		if isinstance(traffic, Flow) is True:
			self.traffic = traffic
		else:
			raise TypeError('traffic must be of type Flow')
		if isinstance(capture, Capture) is True:
			self.capture = capture
		else:
			raise TypeError('capture must be of type Capture')
