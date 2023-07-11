import socket
import threading
import base64
import signal
import sys

import subject as subject_module
import grader as grader_module

client_count = 0
server_socket = None
clients = []

def sigint_handler(sig, frame):
	global server_socket
	global clients

	print("\rStopping server...")

	for client in clients:
		if client.available:
			client.disconnect()
			print("Closed connection with client " + str(client.id))

	server_socket.close()
	print("Server stopped")
	sys.exit(0)

class Client:
	available = True
	level = 0
	subject = None
	tries = 0

	def __init__(self, socket, address):
		global client_count
		self.id = client_count
		client_count += 1
		self.socket = socket
		self.address = address

	def send(self, event, data):
		data = str(data).encode()
		data = base64.b64encode(data)
		msg = bytes(event, 'utf-8') + b'|' + data
		self.socket.send(msg)

	def disconnect(self):
		self.socket.close()
		self.available = False

	def receive_data(self):
		try:
			msg = self.socket.recv(4096)
			if not msg:
				self.available = False
				print("Client " + str(self.id) + " closed connection")
				return
			msg = msg.decode()
			event = msg.split('|', 1)[0]
			data = msg.split('|', 1)[1]
			data = base64.b64decode(data)
			data = eval(data.decode())
			
			if event == "confirm_connection":
				if data["id"] == self.id:
					print("Client " + str(self.id) + " confirmed connection")
					self.send_subject()
				else:
					print("Client " + str(self.id) + " failed to confirm connection")
					self.available = False

			if event == "grade":
				self.tries += 1
				print("Client " + str(self.id) + " sent files for grading (Try " + str(self.tries) + " on exercise " + str(self.subject.name) + ")")
				files = data["files"]
				grader_module.grade(self.subject, files, self)

		except:
			self.available = False
			return

	def send_subject(self):
		self.tries = 0
		self.subject = subject_module.get_subject_for_level(self.level)
		print("Sending subject " + self.subject.name + " to client " + str(self.id) + "...")
		self.send("subject", self.subject.to_dict())

def on_new_client(client_socket, client_address):
	global clients

	client = Client(client_socket, client_address)
	clients.append(client)
	print("New client identified as client " + str(client.id) + ". Sending welcome message...")
	client.send("welcome", {"id": client.id})

	while client.available:
		client.receive_data()

	client_socket.close()

def main():
	global server_socket

	signal.signal(signal.SIGINT, sigint_handler)
	print("Starting server...")

	host = socket.gethostname()
	port = 4241

	server_socket = socket.socket()
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((host, port))

	server_socket.listen(100)
	print("Server started, listening on port " + str(port) + "...")

	while True:
		client_socket, client_address = server_socket.accept()
		threading.Thread(target=on_new_client, args=(client_socket, client_address)).start()

	conn.close()

if __name__ == '__main__':
	main()