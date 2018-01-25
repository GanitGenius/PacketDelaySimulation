import config
import models
from random import uniform

number_of_sources = config.number_of_sources
pkt_size = config.pkt_size
pkt_per_sec = config.source_packets_per_sec
bs = config.source_to_switch_push_speed
bss = config.switch_to_sink_push_speed

sources = []
events = {}
total_pkt_in_queue = 1

def validate():
	assert bs > pkt_size * pkt_per_sec 

def pushEvent(ev):
	global events
	time = ev.time
	if time not in events.keys():
		events[time] = [ev]
	else:
		events[time].append(ev)

delay = 0.0

def processEvent(ev):
	global pkt_size, bs, bss, total_pkt_in_queue, sources, delay

	source_id = ev.source_id
	pkt_id = ev.pkt_id
	time = ev.time
	state = ev.state
	if ev.state == 0:
		time += pkt_size / bs
	elif ev.state == 1:
		sources[source_id].packets[pkt_id].setSwitchReachingTime(time)
		delay -= time
		time += total_pkt_in_queue * pkt_size / bss
		delay += time
		total_pkt_in_queue += 1
		new_pkt_id, new_pkt_gen_time = sources[source_id].generatePacket()
		pushEvent(models.Event(source_id, new_pkt_id, new_pkt_gen_time))
	elif ev.state == 2:
		sources[source_id].packets[pkt_id].setSwitchLeavingTime(time)
		total_pkt_in_queue -= 1
		time += pkt_size / bss
	elif ev.state == 3:
		sources[source_id].packets[pkt_id].setSinkReachingTime(time)

	if state != 3:
		new_ev = models.Event(source_id, pkt_id, time, state + 1)
		pushEvent(new_ev)

def main():
	global src_count, number_of_sources, total_pkt_in_queue, sources

	validate()
	for i in range(number_of_sources):
		start_time = uniform(0., 10.)
		new_src = models.Source(i, start_time)
		sources.append(new_src)
		pkt_id, gen_time = new_src.generatePacket()
		# print "Source ", i, "at ", start_time, pkt_id, gen_time

		ev = models.Event(i, pkt_id, gen_time, 0)
		pushEvent(ev)

	for i in range(1000):
		global events

		keys = events.keys()
		keys.sort()
		key = keys[0]
		values = events[key]
		del events[key]
		values.sort()
		for evv in values:
			processEvent(evv)
	
	global delay

	for src in sources:
		packets = src.packets
		for pkt_id in packets.keys():
			if packets[pkt_id].status < 2:
				continue
			pkt = packets[pkt_id]
			delay += pkt.switchLeavingTime - pkt.switchReachingTime


	print delay

if __name__ == '__main__':

	while bss > 1:
		# bss = config.source_to_switch_push_speed + i
		sources = []
		events = {}
		total_pkt_in_queue = 1
		main()
		bss -= 1
