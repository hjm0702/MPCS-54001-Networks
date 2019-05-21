#!/usr/bin/env python3

import socket
import sys
import time
from _thread import *
import threading

#Read command-line operations
inputs = sys.argv[1:]
settings = {}
for item in inputs:
	settings[item.split("=")[0].strip("--")] = item.split("=")[1]

try : 
	#Parse command-line options		
	server_ip = settings["server_ip"]	
	server_port = int(settings["server_port"])
	counter = int(settings["count"])
	period = int(settings["period"])/1000
	time_out = int(settings["timeout"])/1000


#print error message if options are not specified
except KeyError as e:
	print("Please enter {} option".format(e))

seq = 0
min_rtt = 10000000000
max_rtt = 0
avg_rtt = 0
total_rtt = 0
packets_dropped = 0
total_packets = 0
packets_received = 0
print("PING {}".format(server_ip))
top_start = time.time()

def main():
	global seq
	global min_rtt
	global max_rtt
	global avg_rtt
	global packets_dropped
	global total_packets
	global packets_received
	global total_rtt
	global top_start

	while seq < counter:
		seq = seq+1
		threading.Timer(period, main).start() #Key
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.settimeout(time_out) #Key
		raw_message = "PING {} {}\r\n".format(seq, time.time())
		message = raw_message.encode()
		addr = (server_ip, server_port)
		start = time.time()
		client_socket.sendto(message,addr) 
		total_packets += 1
		
		#Receive a message
		try:
			data, server = client_socket.recvfrom(1024)
			data_decoded = data.decode()
			received_seq = data_decoded.split()[1]
			end = time.time()
			elapsed = end - start
			total_rtt += elapsed
			if min_rtt > elapsed:
				min_rtt = elapsed
			if max_rtt < elapsed:
				max_rtt = elapsed
			print(f'PONG {server_ip}: seq={received_seq} time={round(elapsed*1000)} ms')
			packets_received += 1
						
			if packets_received == counter:
				summary()
		except socket.timeout: #Key
			packets_dropped += 1
			if counter == packets_received+packets_dropped:
				summary()
		time.sleep(period) #Key

#Summarize stats
def summary():
	global seq
	global min_rtt
	global max_rtt
	global avg_rtt
	global packets_dropped
	global total_packets
	global packets_received
	global total_rtt
	global top_start

	top_end = time.time()
	total = 100-round(packets_received/total_packets*100)
	print("")
	print('--- {} ping statistics ---'.format(server_ip))
	print('{} transmitted, {} received, {}% loss, time {}ms'.format(total_packets, packets_received, total, round((top_end-top_start)*1000)))
	if packets_received != 0:
		print('rtt min/avg/max = {}/{}/{} ms'.format(round(min_rtt*1000), round(total_rtt/packets_received*1000), round(max_rtt*1000)))
	else:
		print('rtt min/avg/max = {}/{}/{} ms'.format(0, 0, round(max_rtt*1000)))
if __name__ == "__main__":
	main()
	
