import socket
import threading
import base64

def receive_data(client_socket):
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
			print("Welcome! Your ID is ", data["id"])

def main():
	print("Starting client...")

	host = socket.gethostname()
	port = 4242

	client_socket = socket.socket()
	client_socket.connect((host, port))
	print("Connected to server on port " + str(port))

	threading.Thread(target=receive_data, args=(client_socket,)).start()

	# client_socket.close()

if __name__ == '__main__':
	main()