import socket
import select
import os
import base64
import sys
import json
import threading
import time

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m' 

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

def print_subject():
	global current_name
	global current_complete_file
	global current_subject_file

	print("=============================================================")
	print("Your current assignment is: " + style.GREEN + current_name + style.RESET)
	print("Your subject is located at: " + style.GREEN + current_subject_file + style.RESET)
	print("You must submit your work in the rendu folder (" + style.RED + current_complete_file + style.RESET + ")")
	print("=============================================================")
	print("You can now work on your assignment, when you are ready to be graded, type '" + style.GREEN + "grademe" + style.RESET + "' and press enter")

def treat_message(message, client_socket):
	global current_name
	global current_complete_file
	global current_subject_file
	global running
	global grading

	event = message.split('|', 1)[0]
	data = message.split('|', 1)[1]
	data = base64.b64decode(data)
	data = eval(data.decode())

	if event == "welcome":
		print("Server confirmed that you are a new client, id: " + str(data["id"]))
		send_data(client_socket, "welcome", {"id": data["id"], "reconnect": False})

	if event == "welcome_back":
		print("Server confirmed that you reconnected, id: " + str(data["id"]))
		send_data(client_socket, "welcome", {"id": data["id"], "reconnect": True})

	if event == "subject":
		subject_file = open(os.path.expanduser(data["subject_file"]), "w")
		subject_file.write(data["subject"])
		subject_file.close()
		current_name = data["name"]
		current_complete_file = data["complete_file"]
		current_subject_file = data["subject_file"]
		print_subject()

	if event == "grade_result":
		grading = False
		graded = data["grade"]
		trace_content = data["trace"]
		try_count = data["try"]

		if graded:
			print(style.GREEN + ">>>>>>>>>> SUCCESS <<<<<<<<<<" + style.RESET)
			if trace_content is None:
				print("No trace available for this exercice")
			else:
				trace_name = os.path.expanduser("~/traces/" + str(try_count) + "_" + current_name + ".txt")
				trace_file = open(trace_name, "w")
				trace_file.write(trace_content)
				trace_file.close()
				print("Trace saved (" + style.CYAN + trace_name + style.RESET + ")")
			print("You passed the exercice! Please wait for the next one...")


		else:
			print(style.RED + ">>>>>>>>>> FAILURE <<<<<<<<<<" + style.RESET)
			if trace_content is None:
				print("No trace available for this exercice")
			else:
				trace_name = os.path.expanduser("~/traces/" + str(try_count) + "_" + current_name + ".txt")
				trace_file = open(trace_name, "w")
				trace_file.write(trace_content)
				trace_file.close()
				print("Trace saved (" + style.CYAN + trace_name + style.RESET + ")")
			print("You failed the exercice! Please try again...")
			print_subject()

	if event == "terminate":
		print(style.MAGENTA + "You passed all levels, congratulations!" + style.RESET)
		running = False

	if event == "already-connected":
		print(style.RED + "You are already connected to the server, please disconnect first" + style.RESET)
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

ask_for_grade = False
grading = False

def wait_for_grade():
	global grading

	grading = True
	while grading:
		print("Waiting...")
		time.sleep(1)

def treat_stdin(client_socket):
	global ask_for_grade

	line = sys.stdin.readline().strip()
	cmd = line.split(' ', 1)[0]
	args = line.split(' ')[1:]

	if cmd == "help":
		print("The following commands are available:")
		print(style.GREEN + "\thelp" + style.RESET + ": display this help")
		print(style.GREEN + "\tgrademe" + style.RESET + ": send your work to the server for grading")
		return

	if cmd == "grademe":
		ask_for_grade = True
		print(style.RED + "Do you want to be graded?" + style.RESET + " (y/n) ", end="", flush=True)
		return

	yes_cmds = ["y", "yes", "Y", "Yes", "YES"]
	no_cmds = ["n", "no", "N", "No", "NO"]
	if cmd in yes_cmds or cmd in no_cmds:
		if ask_for_grade:
			ask_for_grade = False
			if cmd in no_cmds:
				print("Cancelled grading request")
				return
			if cmd in yes_cmds:
				files = {}
				for file in os.listdir(os.path.expanduser("~/rendu")):
					if file.endswith(".c"):
						files[file] = open(os.path.expanduser("~/rendu/" + file), "r").read()
				send_data(client_socket, "grade", {"files": files})
				print("You work has been sent to the server, waiting for the grade...")
				threading.Thread(target=wait_for_grade).start()
				return
	elif ask_for_grade:
		print(style.RED + "Do you want to be graded?" + style.RESET + " (y/n) ", end="", flush=True)
		return

	print("Unknown command, see '" + style.RED + "help" + style.RESET + "'")


def main():
	global running
	global grading

	if not os.path.isdir(os.path.expanduser("~/subject")):
		os.mkdir(os.path.expanduser("~/subject"))
	if not os.path.isdir(os.path.expanduser("~/rendu")):
		os.mkdir(os.path.expanduser("~/rendu"))
	if not os.path.isdir(os.path.expanduser("~/traces")):
		os.mkdir(os.path.expanduser("~/traces"))

	config = json.load(open("config.json", "r"))
	port = config["port"]
	host = socket.gethostname() if config["host"] == "localhost" else config["host"]

	client_socket = socket.socket()
	try:
		client_socket.connect((host, port))
	except ConnectionRefusedError as e:
		print(style.RED + "Connection failed: " + str(e) + style.RESET)
		return
	print("Connection established with the server")

	poll_obj = select.poll()
	poll_obj.register(client_socket, select.POLLIN)
	poll_obj.register(0, select.POLLIN)

	while running:
		if not grading and not ask_for_grade:
			print(style.YELLOW + "API's shell" + style.RESET + "> ", end="", flush=True)
		try:
			poll_state = poll_obj.poll()
		except KeyboardInterrupt:
			print("\r", end="")
			running = False
			break
		
		print("\r", end="")
		for fd, event in poll_state:
			if fd == client_socket.fileno():
				if event & select.POLLIN:
					if receive_data(client_socket) == 0:
						running = False
						break
			elif fd == 0:
				if event & select.POLLIN:
					treat_stdin(client_socket)

	print(style.RED + "Connection closed" + style.RESET)

if __name__ == '__main__':
	main()