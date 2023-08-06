class Header(object):
	"""Flow.Header class
	
	Container for all traffic packet headers
	"""
	_CHOICE_MAP = {
		'Custom': 'custom',
		'Ethernet': 'ethernet',
		'Vlan': 'vlan',
		'Ipv4': 'ipv4',
		'PfcPause': 'pfcpause',
	}
	def __init__(self, choice):
		if isinstance(choice, (Custom, Ethernet, Vlan, Ipv4, PfcPause)) is False:
			raise TypeError('choice must be of type: Custom, Ethernet, Vlan, Ipv4, PfcPause')
		self.__setattr__('choice',Header._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Header._CHOICE_MAP[choice.__class__.__name__], choice)
