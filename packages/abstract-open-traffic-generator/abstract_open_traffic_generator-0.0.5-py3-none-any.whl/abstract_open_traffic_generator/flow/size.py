class Size(object):
	"""Flow.Size class
	
	The frame size which overrides the total length of the packet
	"""
	_CHOICE_MAP = {
		'Increment': 'increment',
		'Random': 'random',
	}
	def __init__(self, choice):
		if isinstance(choice, (Increment, Random)) is False:
			raise TypeError('choice must be of type: Increment, Random')
		self.__setattr__('choice',Size._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Size._CHOICE_MAP[choice.__class__.__name__], choice)
