import socket
import threading
import base64
import signal
import sys

client_id = -1
client_socket = None
running = True

def sigint_handler(sig, frame):
	global client_socket

	print("\rStopping client...")
	client_socket.close()
	print("Client stopped")
	sys.exit(0)

def send(event, data):
	global client_id

	data = str(data).encode()
	data = base64.b64encode(data)
	msg = bytes(event, 'utf-8') + b'|' + data
	client_socket.send(msg)

def receive_data():
	global client_id
	global client_socket
	global running

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
				print("Server confirmed connection, waiting for exercice...")
				send("confirm_connection", {"id": client_id})

			if event == "subject":
				print("====================== New Subject ======================")
				print("Assignment name: " + data["name"])
				print("Excepted file: " + data["complete_file"])
				print("")
				print("When you want to be graded, type 'grademe' and press enter")
				print("=========================================================")

		except:
			break

	client_socket.close()
	running = False

def main():
	global client_socket

	signal.signal(signal.SIGINT, sigint_handler)

	host = socket.gethostname()
	port = 4241

	client_socket = socket.socket()
	client_socket.connect((host, port))
	print("Connection established with the server, waiting for confirmation...")

	threading.Thread(target=receive_data).start()

	while running:
		pass

	print("Client stopped")

if __name__ == '__main__':
	main()