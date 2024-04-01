import client as client_module
import subject as subject_module

import sys

def treat_stdin(port):

	line = sys.stdin.readline().strip()
	cmd = line.split(' ', 1)[0]
	args = line.split(' ')[1:]

	if cmd == "help":
		print("Available commands:")
		print("\thelp: display this help")
		print("\tinfos: display server infos")
		print("\tclients: display connected clients")
		print("\tsubject <client id> <level> [subject name]: set the subject for a client. If no subject name is specified, a random one will be chosen")

	if cmd == "infos":
		print("Server infos:")
		print("\tPort: " + str(port))
		print("\tConnected clients: " + str(client_module.get_connected_clients_count()))
		print("\tSubjects:")
		for level in subject_module.get_subjects().keys():
			print("\t\tLevel " + str(level) + ": ", end="")
			for subject in subject_module.get_subjects()[level]:
				print(subject.name + " ", end="")
			print("")
		
	if cmd == "clients":
		if client_module.get_connected_clients_count() == 0:
			print("No connected clients")
			return
		
		print("Connected clients:")
		for info in client_module.get_clients_status():
			print("\tClient " + str(info["id"]) + " | Level " + str(info["level"]) + " | Tries " + str(info["tries"]) + " | Subject " + info["subject"] + " | " + ("ONLINE" if info["connected"] else "OFFLINE"))

	if cmd == "subject":
		if len(args) < 2 or len(args) > 3:
			print("Usage: subject <client id> <level> [subject name]")
			return
		try:
			client_id = int(args[0])
			level = int(args[1])
		except:
			print("Usage: subject <client id> <level> [subject name]")
			return

		client = client_module.get_client_by_id(client_id)
		if not client:
			print("Client " + str(client_id) + " not found, see 'clients'")
			return
		
		if not subject_module.is_subject_for_level(level):
			print("Level " + str(level) + " not found, see 'infos'")
			return

		if len(args) == 2:
			subject = subject_module.get_subject_for_level(level)
			client.set_subject(level, subject, level != client.level)
		else:
			subject = subject_module.get_subject_by_name(level, args[2])
			if not subject:
				print("Subject " + args[2] + " not found, see 'infos'")
				return
			client.set_subject(level, subject, level != client.level)
