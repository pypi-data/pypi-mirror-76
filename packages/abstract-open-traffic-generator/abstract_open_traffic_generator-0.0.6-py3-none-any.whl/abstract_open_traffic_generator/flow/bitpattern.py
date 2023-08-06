class BitPattern(object):
	"""Flow.BitPattern class
	
	Container for a bit pattern
	"""
	_CHOICE_MAP = {
		'BitList': 'bitlist',
		'BitCounter': 'bitcounter',
	}
	def __init__(self, choice):
		if isinstance(choice, (BitList, BitCounter)) is False:
			raise TypeError('choice must be of type: BitList, BitCounter')
		self.__setattr__('choice',BitPattern._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(BitPattern._CHOICE_MAP[choice.__class__.__name__], choice)
