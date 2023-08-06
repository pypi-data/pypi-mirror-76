class Port(object):
	"""Port class
	
	An abstract test port used to associate a unique name with the location of a physical or virtual test location.
	Some different types of test locations are:
	  - physical appliance with multiple ports
	  - physical chassis with multiple cards and ports
	  - local interface
	  - virtual machine
	  - docker container
	"""
	def __init__(self, name, location):
		self.name = name
		if isinstance(location, Location) is True:
			self.location = location
		else:
			raise TypeError('location must be of type Location')
