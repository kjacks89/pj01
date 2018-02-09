import socket
import threading
import argparse
import sys
from pathlib import Path
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 47656 # My available ports are 47656 or 47657
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)
path = Path('./www')
parser = argparse.ArgumentParser()
parser.add_argument("--root")
args = parser.parse_args()
if args.root:
	path = Path(args.root)


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
				data = client.recv(1024).decode()
				file_requested = data.split(' ')[1]
				if file_requested == "/":
						file_requested = "/index.html"
				pathToFile = path / file_requested
				httptype = data.split(' ')[2]
				if file_requested.endswith(".html") == -1 or file_requested.endswith(".txt") == -1 or file_requested.endswith(".png") == -1:
					if httpType == 'HTTP/1.0':
						self.client.send(b'HTTP/1.0 400 Bad Request')
					else:
						self.client.send(b'HTTP/1.1 400 Bad Request')
				if os.path.isfile(pathToFile):
					try:
						f = open(pathToFile, 'rb')
						responseBody = f.read()
						f.close()
						contentType = b''
						if file_requested.endswith("html"):
							contentType = b"text/html"
						elif file_requested.endswith("png"):
							contentType = b"image/png"
						else:
							contentType = b"text/plain"
						if httpType == 'HTTP/1.0':
							self.client.send(b'HTTP/1.0 200 OK\r\n' + contentType + '\r\n' + responseBody)
						else:
							self.client.send(b'HTTP/1.1 200 OK\r\n' + contentType + '\r\n' + responseBody)
					except Exception as e:
						if httpType == 'HTTP/1.0':
							self.client.send(b'HTTP/1.0 403 Forbidden')
						else:
							self.client.send(b'HTTP/1.1 403 Forbidden')
				else:
					if httpType == 'HTTP/1.0':
						self.client.send(b'HTTP/1.0 404 Not Found')
					else:
						self.client.send(b'HTTP/1.1 404 Not Found')
								
while True:
		#Accept Connection
		client, address = connection.accept()
		th = HandlerThread(client, address)
		th.start()
