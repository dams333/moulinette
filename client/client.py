import socket
import select
import os
import base64
import sys
import json

buffer = ""
current_name = ""
current_complete_file = ""
current_subject_file = ""
running = True

def send_data(client_socket, event, data):
	data = str(data).encode()
	data = base64.b64encode(data)
	msg = bytes(event, 'utf-8') + b'|' + data + b'\r\n'
	client_socket.send(msg)

def treat_message(message, client_socket):
	global current_name
	global current_complete_file
	global current_subject_file
	global running

	event = message.split('|', 1)[0]
	data = message.split('|', 1)[1]
	data = base64.b64decode(data)
	data = eval(data.decode())

	if event == "welcome":
		print("Server confirmed connection, id: " + str(data["id"]))
		send_data(client_socket, "welcome", {"id": data["id"]})

	if event == "subject":
		subject_file = open(os.path.expanduser(data["subject_file"]), "w")
		subject_file.write(data["subject"])
		subject_file.close()

		print("====================== New Subject ======================")
		print("Assignment name: " + data["name"])
		print("Excepted file: " + data["complete_file"])
		print("Subject: " + data["subject_file"])
		print("")
		print("When you want to be graded, type 'grademe' and press enter")
		print("=========================================================")

		current_name = data["name"]
		current_complete_file = data["complete_file"]
		current_subject_file = data["subject_file"]

	if event == "grade_result":
		graded = data["grade"]
		if graded:
			print("You passed the exercice! Please wait for the next one...")
		else:
			print("You failed the exercice! Please try again...")
			print("====================== Subject ======================")
			print("Assignment name: " + current_name)
			print("Excepted file: " + current_complete_file)
			print("Subject: " + current_subject_file)
			print("")
			print("When you want to be graded, type 'grademe' and press enter")
			print("=====================================================")

	if event == "terminate":
		print("You passed all levels, congratulations!")
		running = False
	

def receive_data(client_socket):
	global buffer

	content = client_socket.recv(1024)
	if not content:
		return 0
	content = content.decode()
	buffer += content
	while "\r\n" in buffer:
		line, buffer = buffer.split("\r\n", 1)
		treat_message(line, client_socket)
	return 1

def treat_stdin(client_socket):
	line = sys.stdin.readline().strip()
	cmd = line.split(' ', 1)[0]
	args = line.split(' ')[1:]

	if cmd == "help":
		print("Available commands:")
		print("\thelp: display this help")
		print("\tgrademe: send your work to the server for grading")

	if cmd == "grademe":
		files = {}
		for file in os.listdir(os.path.expanduser("~/rendu")):
			if file.endswith(".c"):
				files[file] = open(os.path.expanduser("~/rendu/" + file), "r").read()
		send_data(client_socket, "grade", {"files": files})
		print("You work has been sent to the server, waiting for the grade...")

def main():
	global running

	print("Initializing client...")
	if not os.path.isdir(os.path.expanduser("~/subject")):
		os.mkdir(os.path.expanduser("~/subject"))
	if not os.path.isdir(os.path.expanduser("~/rendu")):
		os.mkdir(os.path.expanduser("~/rendu"))
	print("Created subject and rendu directories")

	config = json.load(open("config.json", "r"))
	port = config["port"]
	host = socket.gethostname() if config["host"] == "localhost" else config["host"]

	client_socket = socket.socket()
	try:
		client_socket.connect((host, port))
	except ConnectionRefusedError as e:
		print("Connection failed: " + str(e))
		return
	print("Connection established with the server")

	poll_obj = select.poll()
	poll_obj.register(client_socket, select.POLLIN)
	poll_obj.register(0, select.POLLIN)

	while running:
		try:
			poll_state = poll_obj.poll()
		except KeyboardInterrupt:
			print("\r", end="")
			running = False
			break
		
		for fd, event in poll_state:
			if fd == client_socket.fileno():
				if event & select.POLLIN:
					if receive_data(client_socket) == 0:
						running = False
						break
			elif fd == 0:
				if event & select.POLLIN:
					treat_stdin(client_socket)

	print("Connection closed")

if __name__ == '__main__':
	main()