class Endpoint(object):
	"""Flow.Endpoint class
	
	An endpoint that dictates the type of flow.
	"""
	_CHOICE_MAP = {
		'PortEndpoint': 'port',
		'DeviceEndpoint': 'device',
	}
	def __init__(self, choice):
		if isinstance(choice, (PortEndpoint, DeviceEndpoint)) is False:
			raise TypeError('choice must be of type: PortEndpoint, DeviceEndpoint')
		self.__setattr__('choice',Endpoint._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Endpoint._CHOICE_MAP[choice.__class__.__name__], choice)
