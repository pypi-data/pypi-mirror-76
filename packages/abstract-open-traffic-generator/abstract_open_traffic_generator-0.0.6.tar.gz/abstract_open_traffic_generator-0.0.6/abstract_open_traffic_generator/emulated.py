

class DeviceGroup(object):
	"""Emulated.DeviceGroup class
	
	An abstract container for emulated device containers.
	"""
	def __init__(self, name=None, ports=None, devices=None):
		self.name = name
		self.ports = ports
		self.devices = devices


class Device(object):
	"""Emulated.Device class
	
	An abstract container for emulated protocols.
	"""
	def __init__(self, name=None, devices_per_port=None, parent=None, protocols=None):
		self.name = name
		self.devices_per_port = devices_per_port
		self.parent = parent
		self.protocols = protocols


class Ethernet(object):
	"""Emulated.Ethernet class
	
	Emulated ethernet protocol
	"""
	def __init__(self, name=None, mac=None, mtu=None):
		self.name = name
		self.mac = mac
		self.mtu = mtu


class Vlan(object):
	"""Emulated.Vlan class
	
	Emulated vlan protocol
	"""
	def __init__(self, name=None, parent=None, tpid=None, priority=None, id=None):
		self.name = name
		self.parent = parent
		self.tpid = tpid
		self.priority = priority
		self.id = id


class Ipv4(object):
	"""Emulated.Ipv4 class
	
	Emulated ipv4 protocol
	"""
	def __init__(self, name=None, address=None, gateway=None, prefix=None):
		self.name = name
		self.address = address
		self.gateway = gateway
		self.prefix = prefix


class Bgpv4(object):
	"""Emulated.Bgpv4 class
	
	Emulated bgpv4 protocol
	"""
	def __init__(self, name=None, as_number_2_byte=None, dut_as_number_2_byte=None, as_number_4_byte=None, as_number_set_mode=None, type=None, hold_time_interval=None, keep_alive_interval=None, graceful_restart=None, authentication=None, ttl=None, dut_ipv4_address=None):
		self.name = name
		self.as_number_2_byte = as_number_2_byte
		self.dut_as_number_2_byte = dut_as_number_2_byte
		self.as_number_4_byte = as_number_4_byte
		self.as_number_set_mode = as_number_set_mode
		self.type = type
		self.hold_time_interval = hold_time_interval
		self.keep_alive_interval = keep_alive_interval
		self.graceful_restart = graceful_restart
		self.authentication = authentication
		self.ttl = ttl
		self.dut_ipv4_address = dut_ipv4_address
