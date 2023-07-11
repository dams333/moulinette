import socket
import threading
import base64
import signal
import sys
import os
import time

client_id = -1
client_socket = None
running = True
grading = False
current_name = ""
current_complete_file = ""
current_subject_file = ""

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
	global grading
	global current_name
	global current_complete_file
	global current_subject_file

	while True:
		try:
			msg = client_socket.recv(4096)
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
				grading = False


		except:
			break

	client_socket.close()
	running = False
	grading = False

def wait_for_grade():
	global grading

	grading = True
	print("Sending your works. Please wait for the grade (it can take a while)...")
	while grading:
		print("Waiting...")
		time.sleep(3)

def treat_command(command):
	cmd = command.split(' ')[0]
	args = command.split(' ')[1:]

	if cmd == "help":
		print("Available commands:")
		print("\thelp: display this help")
		print("\tgrademe: send your work to the server and wait for the grade")

	if cmd == "grademe":
		choice = input("Are you sure you want to be graded? (y/n) ")
		if choice == "y" or choice == "Y" or choice == "yes" or choice == "Yes":
			files = {}
			for file in os.listdir(os.path.expanduser("~/rendu")):
				if file.endswith(".c"):
					files[file] = open(os.path.expanduser("~/rendu/" + file), "r").read()
			send("grade", {"files": files})
			wait_for_grade()

def main():
	global client_socket

	signal.signal(signal.SIGINT, sigint_handler)

	if not os.path.isdir(os.path.expanduser("~/subject")):
		os.mkdir(os.path.expanduser("~/subject"))
	if not os.path.isdir(os.path.expanduser("~/rendu")):
		os.mkdir(os.path.expanduser("~/rendu"))

	host = socket.gethostname()
	port = 2121

	client_socket = socket.socket()
	client_socket.connect((host, port))
	print("Connection established with the server, waiting for confirmation...")

	threading.Thread(target=receive_data).start()

	while running:
		command = input()
		treat_command(command)

	print("Client stopped")

if __name__ == '__main__':
	main()