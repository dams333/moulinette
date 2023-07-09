import socket
import threading
import base64

client_id = -1
client_socket = None

def send(event, data):
	global client_id

	data = str(data).encode()
	data = base64.b64encode(data)
	msg = bytes(event, 'utf-8') + b'|' + data + b'\n'
	client_socket.send(msg)

def receive_data():
	global client_id
	global client_socket

	while True:
		msg = client_socket.recv(1024)
		if not msg:
			break
		msg = msg.decode()
		event = msg.split('|', 1)[0]
		data = msg.split('|', 1)[1]
		data = base64.b64decode(data)
		data = eval(data.decode())
		
		if event == "welcome":
			client_id = data["id"]
			print("Server confirmed connection, waiting for it")
			send("confirm_connection", {"id": client_id})

def main():
	global client_socket

	host = socket.gethostname()
	port = 4241

	client_socket = socket.socket()
	client_socket.connect((host, port))
	print("Connection established with the server, waiting for confirmation...")

	threading.Thread(target=receive_data).start()

	while True:
		pass

	client_socket.close()

if __name__ == '__main__':
	main()