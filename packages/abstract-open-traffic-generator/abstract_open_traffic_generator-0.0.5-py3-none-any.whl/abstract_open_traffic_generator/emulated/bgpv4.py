class Bgpv4(object):
	"""Emulated.Bgpv4 class
	
	Emulated bgpv4 protocol
	"""
	def __init__(self, name, as_number_2_byte, dut_as_number_2_byte, as_number_4_byte, as_number_set_mode, type, hold_time_interval, keep_alive_interval, graceful_restart, authentication, ttl, dut_ipv4_address):
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
