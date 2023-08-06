class PfcPause(object):
	"""Flow.PfcPause class
	
	PFC Pause packet header
	"""
	def __init__(self, dst, src, ether_type, control_op_code, priority_enable_vector, pfc_queue_0, pfc_queue_1, pfc_queue_2, pfc_queue_3, pfc_queue_4, pfc_queue_5, pfc_queue_6, pfc_queue_7):
		if isinstance(dst, StringPattern) is True:
			self.dst = dst
		else:
			raise TypeError('dst must be of type StringPattern')
		if isinstance(src, StringPattern) is True:
			self.src = src
		else:
			raise TypeError('src must be of type StringPattern')
		if isinstance(ether_type, StringPattern) is True:
			self.ether_type = ether_type
		else:
			raise TypeError('ether_type must be of type StringPattern')
		if isinstance(control_op_code, StringPattern) is True:
			self.control_op_code = control_op_code
		else:
			raise TypeError('control_op_code must be of type StringPattern')
		if isinstance(priority_enable_vector, StringPattern) is True:
			self.priority_enable_vector = priority_enable_vector
		else:
			raise TypeError('priority_enable_vector must be of type StringPattern')
		if isinstance(pfc_queue_0, StringPattern) is True:
			self.pfc_queue_0 = pfc_queue_0
		else:
			raise TypeError('pfc_queue_0 must be of type StringPattern')
		if isinstance(pfc_queue_1, StringPattern) is True:
			self.pfc_queue_1 = pfc_queue_1
		else:
			raise TypeError('pfc_queue_1 must be of type StringPattern')
		if isinstance(pfc_queue_2, StringPattern) is True:
			self.pfc_queue_2 = pfc_queue_2
		else:
			raise TypeError('pfc_queue_2 must be of type StringPattern')
		if isinstance(pfc_queue_3, StringPattern) is True:
			self.pfc_queue_3 = pfc_queue_3
		else:
			raise TypeError('pfc_queue_3 must be of type StringPattern')
		if isinstance(pfc_queue_4, StringPattern) is True:
			self.pfc_queue_4 = pfc_queue_4
		else:
			raise TypeError('pfc_queue_4 must be of type StringPattern')
		if isinstance(pfc_queue_5, StringPattern) is True:
			self.pfc_queue_5 = pfc_queue_5
		else:
			raise TypeError('pfc_queue_5 must be of type StringPattern')
		if isinstance(pfc_queue_6, StringPattern) is True:
			self.pfc_queue_6 = pfc_queue_6
		else:
			raise TypeError('pfc_queue_6 must be of type StringPattern')
		if isinstance(pfc_queue_7, StringPattern) is True:
			self.pfc_queue_7 = pfc_queue_7
		else:
			raise TypeError('pfc_queue_7 must be of type StringPattern')
