class Physical(object):
	"""Port.Physical class
	
	A physical test port
	"""
	def __init__(self, address, board, port, fanout):
		self.address = address
		self.board = board
		self.port = port
		self.fanout = fanout
