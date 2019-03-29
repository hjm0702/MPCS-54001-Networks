#!/usr/bin/env python3

import sys
import socket
from _thread import *
import threading

def threaded(conn):
	while True:
		
		#try : 
		method_not_allowed = ['POST', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

		#Creating a redirecting-address map
		with open('www/redirect.defs') as red_f:
			red_file = red_f.read()
			#red_file.split("\n")
			redirect_map ={}
			for line in red_file.split("\n")[:2]:
				redirect_map[line.split(" ")[0]] = line.split(" ")[1]

		data = conn.recv(4096)
		rd = data.decode('utf-8')
		
		#print("!!!This is what received")
		print(rd)
		#print("!!!This is what received")
		#Get Method
		request = list(rd.split('\r\n'))[0].split(' ')[0]

		#Check file / extension name
		try: 
			file = list(rd.split('\r\n'))[0].split(' ')[1]
		except IndexError:
			file = ""			
		try : 
			extension = file.split(".")[1]
		except IndexError: 
			extension = ""

		#print("-----This is the request :", request)
		#print("-----This is the file :", file)
		#print("-----This is the extension :", extension)

		sys.stdout.write(rd)

		username = "jungmin"
		directory = '/home/{}/54001/project2/www'.format(username)
		full_file = directory+file

		#If GET request
		if request == 'GET':

			#if redirect request
			if file in redirect_map:
				header = "HTTP/1.1 301 Moved Permanently\r\n"
				header += "Location: "+redirect_map[file]+"\r\n"
				print(header)		
				conn.sendall(header.encode())
	
			else:
				#If requested file exists
				try : 
					if file == "/redirect.defs":
						body = "<html><body>File Not Found</body></html>"
						header = "HTTP/1.1 404 Not Found\r\n"
						header += "Content-Length: {}\r\n".format(len(body))
						header += "Content-Type: text/html; charset=utf-8\r\n"
						header += "\r\n"
						header += body
						print(header.encode())
						conn.sendall(header.encode())

					else:
						with open(full_file, 'rb') as f:
							data = f.read()

						header = "HTTP/1.1 200 OK\r\n"
						if extension == "html":
							extension_adj = "text/html"
						elif extension == "pdf":
							extension_adj = "application/pdf"
						elif extension == "png":
							extension_adj = "image/png"
						elif extension == "jpeg":
							extension_adj = "image/jpeg"
						else:
							extension_adj = "text/plain"

						header += "Content-Length: {}\r\n".format(len(data))
						header += "Content-Type: "+extension_adj+"; charset=utf-8\r\n"
						header += ""
						header += "\r\n"

						print(header.encode()+data)
						conn.sendall(header.encode()+data)
						#if not data:
						#	break

				#If requested file does not exists
				except FileNotFoundError :
					body = "<html><body>File Not Found</body></html>"
					header = "HTTP/1.1 404 Not Found\r\n"
					header += "Content-Length: {}\r\n".format(len(body))
					header += "Content-Type: text/html; charset=utf-8\r\n"
					header += "\r\n"
					header += body
					print(header.encode())
					conn.sendall(header.encode())

		elif request == "HEAD": 
	
			#if redirect request
			if file in redirect_map:
				header = "HTTP/1.1 301 Moved Permanently\r\n"
				header += "Location: "+redirect_map[file]+"\r\n"
				print(header)		
				conn.sendall(header.encode())

			else:

				if file == "/redirect.defs":
					body = "<html><body>File Not Found</body></html>"
					header = "HTTP/1.1 404 Not Found\r\n"
					header += "Content-Length: {}\r\n".format(len(body))
					header += "Content-Type: text/html; charset=utf-8\r\n"
					header += "\r\n"
					header += body
					print(header.encode())
					conn.sendall(header.encode())

				else:
	 
					#If requested file exists
					try : 
						with open(full_file, 'rb') as f:
							data = f.read()

						header = "HTTP/1.1 200 OK\r\n"
						if extension == "html":
							extension_adj = "text/html"
						elif extension == "pdf":
							extension_adj = "application/pdf"
						elif extension == "png":
							extension_adj = "image/png"
						elif extension == "jpeg":
							extension_adj = "image/jpeg"
						else:
							extension_adj = "text/plain"

						header += "Content-Length: {}\r\n".format(len(data))
						header += "Content-Type: "+extension_adj+"; charset=utf-8\r\n"
						header += ""
						header += "\r\n"

						print(header.encode()+data)
						conn.sendall(header.encode()+data)
						#if not data:
						#	break

					#If requested file does not exists
					except FileNotFoundError : 

						body = "<html><body>File Not Found</body></html>"
						header = "HTTP/1.1 404 Not Found\r\n"
						header += "Content-Length: {}\r\n".format(len(body))
						header += "Content-Type: text/html; charset=utf-8\r\n"
						header += "\r\n"
						header += body
						print(header.encode())
						conn.sendall(header.encode())

		#If request is not allowed to response
		elif request in method_not_allowed :

			body = "<html><body>405 Method Not Allowed</body></html>"
			header = "HTTP/1.1 405 Method Not Allowed\r\n"
			header += "Content-Length: {}\r\n".format(len(body))
			header += "Content-Type: text/html; charset=utf-8\r\n"
			header += "\r\n"
			header += body
			print(header.encode())
			conn.sendall(header.encode())

		#If request if malformed
		elif not request:
			#print("~~~problem?")
			break
		
		elif request:	
			body = "<html><body>400 Bad Request</body></html>"
			header = "HTTP/1.1 400 Bad Request\r\n"
			header += "Content-Length: {}\r\n".format(len(body))
			header += "Content-Type: text/html; charset=utf-8\r\n"
			header += "\r\n"
			header += body
			print(header.encode())
			conn.sendall(header.encode())

					
		#except OSError as e:
		#	break
	conn.shutdown(socket.SHUT_WR)
	conn.close()

def main():

	try :

		linux1 = '128.135.164.171'
		linux2 = '128.135.164.172'
		linux3 = '128.135.164.173'
		local = '127.0.0.1' 

		#Intiate the server
		host = local
		port = int(sys.argv[1])

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(5)

		print('Initiating the server!')
			
		while True:
			conn, addr = s.accept()
			start_new_thread(threaded, (conn,))
		s.close()

	except OSError :
		print("Please try another port as the port is in use.")

if __name__ == "__main__":
	main()
