import config

bs = config.source_to_switch_push_speed
bss = config.switch_to_sink_push_speed

class Packet(object):
	"""docstring for Packet"""
	pkt_size = config.pkt_size
	status = 0

	def __init__(self, source_id, pkt_id, creation_time):
		self.source_id = source_id
		self.pkt_id = pkt_id
		self.creation_time = creation_time
		self.status = 0

	def setSwitchReachingTime(self, time):
		self.switchReachingTime = time
		self.status = 1

	def setSwitchLeavingTime(self, time):
		self.switchLeavingTime = time
		self.status = 2

	def setSinkReachingTime(self, time):
		self.sinkReachingTime = time
		self.status = 3

class Source(object):
	pkt_per_sec = config.source_packets_per_sec
	push_speed = config.source_to_switch_push_speed
	tot_pkts_generated = 0
	last_generated_time = -1
	source_id = 0
	start_time = 0.

	packets = {}

	def __init__(self, source_id, start_time):
		self.source_id = source_id
		self.start_time = start_time

	def generatePacket(self):
		if self.last_generated_time == -1:
			self.last_generated_time = self.start_time
		else:
			self.last_generated_time += 1./self.pkt_per_sec

		self.tot_pkts_generated += 1
		pkt_id = self.tot_pkts_generated
		pkt = Packet(self.source_id, pkt_id, self.last_generated_time)
		self.packets[self.tot_pkts_generated] = pkt
		return pkt_id, self.last_generated_time

class Event(object):
	"""docstring for Event"""
	def __init__(self, source_id, pkt_id, time, state=0):
		self.source_id = source_id
		self.pkt_id = pkt_id
		self.time = time
		self.state = state
