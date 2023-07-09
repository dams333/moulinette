import socket
import threading
import base64

client_count = 0

class Client:
	available = True

	def __init__(self, socket, address):
		global client_count
		self.id = client_count
		client_count += 1
		self.socket = socket
		self.address = address

	def send(self, event, data):
		data = str(data).encode()
		data = base64.b64encode(data)
		msg = bytes(event, 'utf-8') + b'|' + data + b'\n'
		self.socket.send(msg)

	def receive_data(self):
		msg = self.socket.recv(1024)
		if not msg:
			return
		msg = msg.decode()
		event = msg.split('|', 1)[0]
		data = msg.split('|', 1)[1]
		data = base64.b64decode(data)
		data = eval(data.decode())
		
		if event == "confirm_connection":
			if data["id"] == self.id:
				print("Client " + str(self.id) + " confirmed connection")
			else:
				print("Client " + str(self.id) + " failed to confirm connection")
				self.available = False

def on_new_client(client_socket, client_address):
	client = Client(client_socket, client_address)
	print("New client identified as client " + str(client.id) + ". Sending welcome message...")
	client.send("welcome", {"id": client.id})

	while client.available:
		client.receive_data()

	client_socket.close()

def main():
	print("Starting server...")

	host = socket.gethostname()
	port = 4241

	server_socket = socket.socket()
	server_socket.bind((host, port))

	server_socket.listen(100)
	print("Server started, listening on port " + str(port) + "...")

	while True:
		client_socket, client_address = server_socket.accept()
		threading.Thread(target=on_new_client, args=(client_socket, client_address)).start()

	conn.close()

if __name__ == '__main__':
	main()