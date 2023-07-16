import subject as subject_module
import client as client_module
import cli as cli_module

import json
import socket
import select
import base64

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
	poll_obj.register(0, select.POLLIN)

	running = True
	while running:
		try:
			poll_state = poll_obj.poll()
		except KeyboardInterrupt:
			print("\r", end="")
			running = False
			break
		for fd, event in poll_state:

			if fd == server_socket.fileno():
				if event & select.POLLIN:
					client_socket, addr = server_socket.accept()
					already_connected_client = client_module.get_client_by_address(addr)
					if already_connected_client == None:
						client = client_module.register_client(client_socket, addr)
						client.send("welcome", {"id": client.id})
						poll_obj.register(client_socket, select.POLLIN | select.POLLOUT)
					else:
						if already_connected_client.connected:
							data = str({}).encode()
							data = base64.b64encode(data)
							client_socket.send(bytes('already-connected', 'utf-8') + b'|' + data + b'\r\n')
							client_socket.close()
						else:
							already_connected_client.socket = client_socket
							already_connected_client.connected = True
							already_connected_client.send("welcome_back", {"id": already_connected_client.id})
							print("Client " + str(already_connected_client.id) + " reconnected")
							poll_obj.register(client_socket, select.POLLIN | select.POLLOUT)
			
			elif fd == 0:
				if event & select.POLLIN:
					cli_module.treat_stdin(port)
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