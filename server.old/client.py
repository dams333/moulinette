import subject as subject_module
import grader as grader_module

import base64
import threading

client_count = 0
clients = []

def get_clients_status():
	res = []

	for client in clients:
		res.append({
			"id": client.id,
			"level": client.level,
			"tries": client.tries,
			"subject": client.subject.name if client.subject else "Undefined",
			"connected": client.connected,
		})
	
	return res

def get_client_by_id(id):
	global clients
	for client in clients:
		if client.id == id:
			return client
	return None

def get_client_by_address(address):
	global clients
	for client in clients:
		if client.address[0] == address[0]:
			return client
	return None

def get_client_by_socket(fd):
	global clients
	for client in clients:
		if client.socket.fileno() == fd:
			return client
	return None

def register_client(socket, address):
	global clients
	client = Client(socket, address)
	clients.append(client)
	return client

def get_connected_clients_count():
	global clients
	return len(clients)

class Client:
	level = 0
	tries = 0
	subject = None
	connected = True

	def __init__(self, socket, address):
		global client_count
		global clients

		self.id = client_count
		client_count += 1
		self.socket = socket
		self.buffer = ""
		self.address = address
		print("Client " + str(self.id) + " connected")

	def read_data(self):
		content = self.socket.recv(1024)
		if not content:
			return 0
		content = content.decode()
		self.buffer += content
		while "\r\n" in self.buffer:
			line, self.buffer = self.buffer.split("\r\n", 1)
			if self.treat_message(line) == 0:
				return 0
		return 1

	def treat_message(self, message):
		event = message.split('|', 1)[0]
		data = message.split('|', 1)[1]
		data = base64.b64decode(data)
		data = eval(data.decode())

		if event == "welcome":
			if data["id"] != self.id:
				print("Receive invalid welcome message from client " + str(self.id) + ", disconnecting")
				return 0
			print("Confirmed handshake with client " + str(self.id))
			self.send_subject(data["reconnect"])

		if event == "grade":
			self.tries += 1
			print("Client " + str(self.id) + " sent files for grading (Try " + str(self.tries) + " on exercise " + str(self.subject.name) + ")")
			threading.Thread(target=grader_module.grade, args=(self.subject, data["files"], self)).start()			

		return 1

	def disconnect(self):
		print("Client " + str(self.id) + " disconnected")
		self.socket.close()
		self.socket = None
		self.connected = False

	def send(self, event, data):
		if not self.connected:
			return
		data = str(data).encode()
		data = base64.b64encode(data)
		msg = bytes(event, 'utf-8') + b'|' + data + b'\r\n'
		self.socket.send(msg)

	def send_subject(self, reconnect):
		if not reconnect:
			if not subject_module.is_subject_for_level(self.level):
				print("Client " + str(self.id) + " passed all levels")
				self.send("terminate", {})
				return
			self.subject = subject_module.get_subject_for_level(self.level)
		print("Sending subject " + self.subject.name + " to client " + str(self.id))
		self.send("subject", self.subject.to_dict())

	def set_subject(self, level, subject, reset):
		if reset:
			self.tries = 0
		self.level = level
		self.subject = subject
		print("Sending subject " + self.subject.name + " to client " + str(self.id))
		self.send("subject", self.subject.to_dict())