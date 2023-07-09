import socket
import threading
import base64

client_count = 0

class Client:
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

def on_new_client(client_socket, client_address):
	# while True:
	# 	msg = client_socket.recv(1024)
	# 	if not msg:
	# 		break
	# 	msg = msg.decode()
	# 	print(client_address, ' >> ', msg)
	client = Client(client_socket, client_address)
	print("New client identified as client " + str(client.id))
	client.send("welcome", {"id": client.id})
	# client_socket.close()

def main():
	print("Starting server...")

	host = socket.gethostname()
	port = 4242

	server_socket = socket.socket()
	server_socket.bind((host, port))

	server_socket.listen(100)
	print("Server listening on port " + str(port) + "...")

	while True:
		client_socket, client_address = server_socket.accept()
		threading.Thread(target=on_new_client, args=(client_socket, client_address)).start()

	conn.close()

if __name__ == '__main__':
	main()