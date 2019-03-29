#!/usr/bin/env python3

import sys
import socket
from _thread import *

host = '127.0.0.1'
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(5)

print('Waiting!')

def threaded_client(conn):
	conn.send(str.encode('Welcome\n'))
	while True:
		data = conn.recv(2048)
		reply = 'Server output :'+data.decode('utf-8')
		sys.stdout.write(data.decode('utf-8'))
		if not data:
			break
		conn.sendall(str(reply).encode())
	conn.close()

while True:
	conn, addr = s.accept()
	#sys.stdout.write('connected to: '+addr[0]+':'+str(addr[1]))
	start_new_thread(threaded_client, (conn,))
	print('Message received:')
s.close()

