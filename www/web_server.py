import socket
import threading
import argparse
import sys
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 47656 # My available ports are 47656 or 47657
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)
parser = argparse.ArgumentParser()
parser.add_argument('--root', '-R', metavar = 'PORT', default = os.getcwd())
args = parser.parse_args()
SERVER_ROOT = args.root

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind(SERVER_ADDR)
connection.listen(10)

class HandlerThread(threading.Thread):
		"""This is the class for the HandlerThread object
				It's used to create multiple threads to enable concurrency"""

		def __init__(self, client, address):
				"""HandlerThread Constructor"""
				threading.Thread.__init__(self)
				self.client = client
				self.address = address

		def run(self):
				"""Server code"""
				finalHeader = b''
				#Receives GET request from client 
				data = client.recv(1024).decode().strip()
				file_requested = data.split(' ')[1]
				defaultCheck = SERVER_ROOT + '/index.html'
				if file_requested == "/":
					if os.path.isfile(defaultCheck):
						file_requested += 'index.html'
					else:
						file_requested += 'index.txt'
				httpType = data.split(' ')[2]
				#Checks if file type is not supported
				if file_requested.endswith(".html") == 0 and file_requested.endswith(".txt") == 0 and file_requested.endswith(".png") == 0:
					finalHeader = b'400 Bad Request'
					self.client.send(finalHeader)
				else:
					responseCode = b''
					responseBody = b''
					finalHeader = b''
					path = SERVER_ROOT + file_requested
					#If file path exists
					if os.path.isfile(path):
						#try catch checks for permissions
						try:
							f = open(path, 'rb')
							responseBody = f.read()
							f.close()
							contentType = b''
							if file_requested.endswith("html"):
								contentType = b'text/html'
							elif file_requested.endswith("png"):
								contentType = b'image/png'
							else:
								contentType = b'text/plain'
							if httpType == 'HTTP/1.0':
								responseCode = b'HTTP/1.0 200 OK'
								finalHeader = responseCode + b'\r\n' + contentType + b'\r\n\r\n' + responseBody
								self.client.send(finalHeader)
							else:
								responseCode = b'HTTP/1.1 200 OK'
								finalHeader = responseCode + b'\r\n' + contentType + b'\r\n\r\n' + responseBody
								self.client.send(finalHeader)
						#If not correct permission, then send a 403 message
						except Exception as e:
							finalHeader = b'403 Forbidden\r\n\r\n'
							self.client.send(finalHeader)
					else:
						finalHeader = b'404 Not Found\r\n\r\n'
						self.client.send(finalHeader)
					#self.client.shutdown(socket.SHUT_RDWR)
				self.client.close()					
while True:
		#Accept Connection and takes care of concurrency
		client, address = connection.accept()
		th = HandlerThread(client, address)
		th.start()
