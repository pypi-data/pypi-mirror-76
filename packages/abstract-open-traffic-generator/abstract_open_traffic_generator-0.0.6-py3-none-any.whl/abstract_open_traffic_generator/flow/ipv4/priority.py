class Priority(object):
	"""Flow.Ipv4.Priority class
	
	Ipv4 ip priority that can be one of RAW or DSCP.
	"""
	_CHOICE_MAP = {
		'Dscp': 'dscp',
		'NumberPattern': 'raw',
	}
	def __init__(self, choice):
		if isinstance(choice, (Dscp, NumberPattern)) is False:
			raise TypeError('choice must be of type: Dscp, NumberPattern')
		self.__setattr__('choice',Priority._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Priority._CHOICE_MAP[choice.__class__.__name__], choice)
