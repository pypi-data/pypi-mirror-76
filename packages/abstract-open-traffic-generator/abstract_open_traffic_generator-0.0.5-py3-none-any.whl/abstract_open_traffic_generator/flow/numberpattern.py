class NumberPattern(object):
	"""Flow.NumberPattern class
	
	A string pattern
	"""
	_CHOICE_MAP = {
		'list': 'list',
		'NumberCounter': 'counter',
	}
	def __init__(self, choice):
		if isinstance(choice, (list, NumberCounter)) is False:
			raise TypeError('choice must be of type: list, NumberCounter')
		self.__setattr__('choice',NumberPattern._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(NumberPattern._CHOICE_MAP[choice.__class__.__name__], choice)
