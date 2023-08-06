class Flow(object):
	"""Flow class
	
	A high level data plane traffic flow
	Acts as a container for endpoints, frame size, frame rate, duration and packet headers.
	"""
	def __init__(self, name, endpoint, packet, size, rate):
		self.name = name
		if isinstance(endpoint, Endpoint) is True:
			self.endpoint = endpoint
		else:
			raise TypeError('endpoint must be of type Endpoint')
		self.packet = packet
		if isinstance(size, Size) is True:
			self.size = size
		else:
			raise TypeError('size must be of type Size')
		if isinstance(rate, Rate) is True:
			self.rate = rate
		else:
			raise TypeError('rate must be of type Rate')
