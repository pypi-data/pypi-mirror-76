class Location(object):
	"""Port.Location class
	
	The location of a test resource.
	"""
	_CHOICE_MAP = {
		'Physical': 'physical',
		'Interface': 'interface',
		'Virtual': 'virtual',
		'Container': 'container',
	}
	def __init__(self, choice):
		if isinstance(choice, (Physical, Interface, Virtual, Container)) is False:
			raise TypeError('choice must be of type: Physical, Interface, Virtual, Container')
		self.__setattr__('choice',Location._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Location._CHOICE_MAP[choice.__class__.__name__], choice)
