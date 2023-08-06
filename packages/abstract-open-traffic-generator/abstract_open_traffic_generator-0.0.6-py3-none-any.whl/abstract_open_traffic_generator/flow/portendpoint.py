class PortEndpoint(object):
	"""Flow.PortEndpoint class
	
	An endpoint that contains a transmit port and 0..n receive ports.
	"""
	def __init__(self, tx_port, rx_ports, tx_patterns):
		self.tx_port = tx_port
		self.rx_ports = rx_ports
		self.tx_patterns = tx_patterns
