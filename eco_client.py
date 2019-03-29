#!/usr/bin/env python3

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server = input("Please input a server host name: ")
#port = int(input("Please input a port number: "))
server = sys.argv[1]
port = int(sys.argv[2])
#print(server)
#print(port)


while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		print("Input a message to send the server:")
		#for line in sys.stdin.readlines():
		line = sys.stdin.readline()		
		s.connect((server,port))
		s.send(line.encode())
		result = s.recv(4096).decode()
		print("hi")
		sys.stdout.write(result)


