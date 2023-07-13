import subject as subject_module
import client as client_module

import json
import socket
import select

def main():
	print("Starting server...")

	subject_module.load_subjects()

	print("Loading server config...")
	config = json.load(open("config.json", "r"))
	port = config["port"]
	print("Server config loaded")

	print("Preparing server socket...")
	host = socket.gethostname()
	server_socket = socket.socket()
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((host, port))
	server_socket.listen(100)
	print("Server started, listening on port " + str(port))

	poll_obj = select.poll()
	poll_obj.register(server_socket, select.POLLIN)

	running = True
	while running:
		try:
			poll_state = poll_obj.poll()
		except KeyboardInterrupt:
			print("\r")
			running = False
			break

		for fd, event in poll_state:

			if fd == server_socket.fileno():
				if event & select.POLLIN:
					client_socket, addr = server_socket.accept()
					client = client_module.register_client(client_socket)
					poll_obj.register(client_socket, select.POLLIN | select.POLLOUT)
					client.send("welcome", {"id": client.id})
			else:
				client = client_module.get_client_by_socket(fd)
				if not client:
					print("Undefined behaviour: client socket not found")
					continue
				if event & select.POLLIN or event & select.POLLPRI:
					if client.read_data() == 0:
						poll_obj.unregister(client.socket)
						client.disconnect()

	print("Server stopped")


if __name__ == '__main__':
	main()