class Dscp(object):
	"""Flow.Ipv4.Dscp class
	
	Differentiated services code point (DSCP) packet field.
	Per hop bevaior (PHB) property constraint is 6 bits
	>=0 <=63
	The following are valid PHB values:
	  - PHB_DEFAULT = 0
	  - PHB_CS1 = 8
	  - PHB_CS2 = 16
	  - PHB_CS3 = 24
	  - PHB_CS4 = 32
	  - PHB_CS5 = 40
	  - PHB_CS6 = 48
	  - PHB_CS7 = 56
	  - PHB_EF46 = 46
	  - PHB_AF11 = 10
	  - PHB_AF12 = 12
	  - PHB_AF13 = 14
	  - PHB_AF21 = 18
	  - PHB_AF22 = 20
	  - PHB_AF23 = 22
	  - PHB_AF31 = 26
	  - PHB_AF32 = 28
	  - PHB_AF33 = 30
	  - PHB_AF41 = 24
	  - PHB_AF42 = 36
	  - PHB_AF43 = 38
	
	Explicit congestion notification (ECN) packet field
	ECN value constraint is 2 bits
	>=0 <=3 The following are valid explicit-congestion-notification (ECN) values:
	  - ECN_NON_CAPABLE = 0
	  - ECN_CAPABLE = 1
	  - ECN_CAPABLE = 2
	  - ECN_CONGESTION_ENCOUNTERED = 3
	"""
	def __init__(self, phb, ecn):
		if isinstance(phb, NumberPattern) is True:
			self.phb = phb
		else:
			raise TypeError('phb must be of type NumberPattern')
		if isinstance(ecn, NumberPattern) is True:
			self.ecn = ecn
		else:
			raise TypeError('ecn must be of type NumberPattern')
