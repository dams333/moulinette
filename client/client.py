import socket
import threading
import base64
import signal
import sys

client_id = -1
client_socket = None

def sigint_handler(sig, frame):
	global client_socket

	print("Stopping client...")
	client_socket.close()
	print("Client stopped")
	sys.exit(0)

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
		try:
			msg = client_socket.recv(1024)
			if not msg:
				print("Server closed connection")
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

		except:
			break


	client_socket.close()

def main():
	global client_socket

	signal.signal(signal.SIGINT, sigint_handler)

	host = socket.gethostname()
	port = 4241

	client_socket = socket.socket()
	client_socket.connect((host, port))
	print("Connection established with the server, waiting for confirmation...")

	threading.Thread(target=receive_data).start()

	while True:
		pass

if __name__ == '__main__':
	main()