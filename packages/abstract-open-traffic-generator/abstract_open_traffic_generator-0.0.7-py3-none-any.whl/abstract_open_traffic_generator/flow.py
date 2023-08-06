

class Flow(object):
	"""Flow.Flow class
	
	A high level data plane traffic flow
	Acts as a container for endpoints, frame size, frame rate, duration and packet headers.
	"""
	def __init__(self, name=None, endpoint=None, packet=None, size=None, rate=None):
		self.name = name
		if isinstance(endpoint, (Endpoint, type(None))) is True:
			self.endpoint = endpoint
		else:
			raise TypeError('endpoint must be of type Endpoint')
		self.packet = packet
		if isinstance(size, (Size, type(None))) is True:
			self.size = size
		else:
			raise TypeError('size must be of type Size')
		if isinstance(rate, (Rate, type(None))) is True:
			self.rate = rate
		else:
			raise TypeError('rate must be of type Rate')


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
		self.__setattr__('choice', Endpoint._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Endpoint._CHOICE_MAP[choice.__class__.__name__], choice)


class PortEndpoint(object):
	"""Flow.PortEndpoint class
	
	An endpoint that contains a transmit port and 0..n receive ports.
	"""
	def __init__(self, tx_port=None, rx_ports=None, tx_patterns=None):
		self.tx_port = tx_port
		self.rx_ports = rx_ports
		self.tx_patterns = tx_patterns


class DeviceEndpoint(object):
	"""Flow.DeviceEndpoint class
	
	An endpoint that contains 1..n emulated transmit devices and 1..n  emulated receive devices.
	"""
	def __init__(self, tx_devices=None, rx_devices=None):
		self.tx_devices = tx_devices
		self.rx_devices = rx_devices


class PortPattern(object):
	"""Flow.PortPattern class
	
	A pattern that is applied to a test port
	The name of the pattern will be reflected in the port results.
	"""
	def __init__(self, name=None, offset=None, pattern=None, mask=None):
		self.name = name
		self.offset = offset
		self.pattern = pattern
		self.mask = mask


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
		self.__setattr__('choice', Header._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Header._CHOICE_MAP[choice.__class__.__name__], choice)


class Custom(object):
	"""Flow.Custom class
	
	Custom packet header
	"""
	def __init__(self, bytes=None, patterns=None):
		self.bytes = bytes
		self.patterns = patterns


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
		self.__setattr__('choice', BitPattern._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(BitPattern._CHOICE_MAP[choice.__class__.__name__], choice)


class BitList(object):
	"""Flow.BitList class
	
	A pattern which is a list of values.
	"""
	def __init__(self, offset=None, length=None, count=None, values=None):
		self.offset = offset
		self.length = length
		self.count = count
		self.values = values


class BitCounter(object):
	"""Flow.BitCounter class
	
	An incrementing pattern
	"""
	def __init__(self, offset=None, length=None, count=None, start=None, step=None):
		self.offset = offset
		self.length = length
		self.count = count
		self.start = start
		self.step = step


class Ethernet(object):
	"""Flow.Ethernet class
	
	Ethernet packet header
	"""
	def __init__(self, dst=None, src=None, ether_type=None):
		if isinstance(dst, (StringPattern, type(None))) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be of type StringPattern')
		if isinstance(src, (StringPattern, type(None))) is True:
			self.src = src
		else:
			raise TypeError('src must be of type StringPattern')
		if isinstance(ether_type, (StringPattern, type(None))) is True:
			self.ether_type = ether_type
		else:
			raise TypeError('ether_type must be of type StringPattern')


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
		self.__setattr__('choice', StringPattern._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(StringPattern._CHOICE_MAP[choice.__class__.__name__], choice)


class StringCounter(object):
	"""Flow.StringCounter class
	
	TBD
	"""
	def __init__(self, start=None, step=None, direction=None, count=None):
		self.start = start
		self.step = step
		self.direction = direction
		self.count = count


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
		self.__setattr__('choice', NumberPattern._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(NumberPattern._CHOICE_MAP[choice.__class__.__name__], choice)


class NumberCounter(object):
	"""Flow.NumberCounter class
	
	TBD
	"""
	def __init__(self, start=None, step=None, direction=None, count=None):
		self.start = start
		self.step = step
		self.direction = direction
		self.count = count


class Vlan(object):
	"""Flow.Vlan class
	
	Vlan packet header
	"""
	def __init__(self, priority=None, cfi=None, id=None, protocol=None):
		if isinstance(priority, (StringPattern, type(None))) is True:
			self.priority = priority
		else:
			raise TypeError('priority must be of type StringPattern')
		if isinstance(cfi, (StringPattern, type(None))) is True:
			self.cfi = cfi
		else:
			raise TypeError('cfi must be of type StringPattern')
		if isinstance(id, (StringPattern, type(None))) is True:
			self.id = id
		else:
			raise TypeError('id must be of type StringPattern')
		if isinstance(protocol, (StringPattern, type(None))) is True:
			self.protocol = protocol
		else:
			raise TypeError('protocol must be of type StringPattern')


class Ipv4(object):
	"""Flow.Ipv4 class
	
	Ipv4 packet header
	"""
	def __init__(self, priority=None, src=None, dst=None):
		if isinstance(priority, (Priority, type(None))) is True:
			self.priority = priority
		else:
			raise TypeError('priority must be of type Priority')
		if isinstance(src, (StringPattern, type(None))) is True:
			self.src = src
		else:
			raise TypeError('src must be of type StringPattern')
		if isinstance(dst, (StringPattern, type(None))) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be of type StringPattern')


class PfcPause(object):
	"""Flow.PfcPause class
	
	PFC Pause packet header
	"""
	def __init__(self, dst=None, src=None, ether_type=None, control_op_code=None, priority_enable_vector=None, pfc_queue_0=None, pfc_queue_1=None, pfc_queue_2=None, pfc_queue_3=None, pfc_queue_4=None, pfc_queue_5=None, pfc_queue_6=None, pfc_queue_7=None):
		if isinstance(dst, (StringPattern, type(None))) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be of type StringPattern')
		if isinstance(src, (StringPattern, type(None))) is True:
			self.src = src
		else:
			raise TypeError('src must be of type StringPattern')
		if isinstance(ether_type, (StringPattern, type(None))) is True:
			self.ether_type = ether_type
		else:
			raise TypeError('ether_type must be of type StringPattern')
		if isinstance(control_op_code, (StringPattern, type(None))) is True:
			self.control_op_code = control_op_code
		else:
			raise TypeError('control_op_code must be of type StringPattern')
		if isinstance(priority_enable_vector, (StringPattern, type(None))) is True:
			self.priority_enable_vector = priority_enable_vector
		else:
			raise TypeError('priority_enable_vector must be of type StringPattern')
		if isinstance(pfc_queue_0, (StringPattern, type(None))) is True:
			self.pfc_queue_0 = pfc_queue_0
		else:
			raise TypeError('pfc_queue_0 must be of type StringPattern')
		if isinstance(pfc_queue_1, (StringPattern, type(None))) is True:
			self.pfc_queue_1 = pfc_queue_1
		else:
			raise TypeError('pfc_queue_1 must be of type StringPattern')
		if isinstance(pfc_queue_2, (StringPattern, type(None))) is True:
			self.pfc_queue_2 = pfc_queue_2
		else:
			raise TypeError('pfc_queue_2 must be of type StringPattern')
		if isinstance(pfc_queue_3, (StringPattern, type(None))) is True:
			self.pfc_queue_3 = pfc_queue_3
		else:
			raise TypeError('pfc_queue_3 must be of type StringPattern')
		if isinstance(pfc_queue_4, (StringPattern, type(None))) is True:
			self.pfc_queue_4 = pfc_queue_4
		else:
			raise TypeError('pfc_queue_4 must be of type StringPattern')
		if isinstance(pfc_queue_5, (StringPattern, type(None))) is True:
			self.pfc_queue_5 = pfc_queue_5
		else:
			raise TypeError('pfc_queue_5 must be of type StringPattern')
		if isinstance(pfc_queue_6, (StringPattern, type(None))) is True:
			self.pfc_queue_6 = pfc_queue_6
		else:
			raise TypeError('pfc_queue_6 must be of type StringPattern')
		if isinstance(pfc_queue_7, (StringPattern, type(None))) is True:
			self.pfc_queue_7 = pfc_queue_7
		else:
			raise TypeError('pfc_queue_7 must be of type StringPattern')


class GroupBy(object):
	"""Flow.GroupBy class
	
	Group results 
	"""
	def __init__(self, field=None, label=None):
		self.field = field
		self.label = label


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
		self.__setattr__('choice', Size._CHOICE_MAP[choice.__class__.__name__])
		self.__setattr__(Size._CHOICE_MAP[choice.__class__.__name__], choice)


class Rate(object):
	"""Flow.Rate class
	
	The rate of packet transmission
	"""
	def __init__(self, type=None, value=None):
		self.type = type
		self.value = value
