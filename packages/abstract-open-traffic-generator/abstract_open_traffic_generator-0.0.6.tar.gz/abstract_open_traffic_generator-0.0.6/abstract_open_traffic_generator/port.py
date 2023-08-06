

class Port(object):
	"""Port.Port class
	
	An abstract test port used to associate a unique name with the location of a physical or virtual test location.
	Some different types of test locations are:
	  - physical appliance with multiple ports
	  - physical chassis with multiple cards and ports
	  - local interface
	  - virtual machine
	  - docker container
	"""
	def __init__(self, name=None, location=None):
		self.name = name
		if isinstance(location, (Location, type(None))) is True:
			self.location = location
		else:
			raise TypeError('location must be of type Location')


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
		self.__setattr__('choice', Location._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Location._CHOICE_MAP[choice.__class__.__name__], choice)


class Physical(object):
	"""Port.Physical class
	
	A physical test port
	"""
	def __init__(self, address=None, board=None, port=None, fanout=None):
		self.address = address
		self.board = board
		self.port = port
		self.fanout = fanout


class Interface(object):
	"""Port.Interface class
	
	An interface test port
	"""
	def __init__(self, name=None):
		self.name = name


class Virtual(object):
	"""Port.Virtual class
	
	A virtual test port
	"""
	def __init__(self, address=None):
		self.address = address


class Container(object):
	"""Port.Container class
	
	A container test port
	"""
	def __init__(self, address=None, port=None):
		self.address = address
		self.port = port
