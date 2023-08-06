class StringPattern(object):
	"""Flow.StringPattern class
	
	A string pattern
	"""
	_CHOICE_MAP = {
		'str': 'fixed',
		'list': 'list',
		'StringCounter': 'counter',
	}
	def __init__(self, choice):
		if isinstance(choice, (str, list, StringCounter)) is False:
			raise TypeError('choice must be of type: str, list, StringCounter')
		self.__setattr__('choice',StringPattern._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(StringPattern._CHOICE_MAP[choice.__class__.__name__], choice)
