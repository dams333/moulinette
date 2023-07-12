import server as server
import subject as subjects_module

def treat_command(command, clients):
	cmd = command.split(' ')[0]
	args = command.split(' ')[1:]

	if cmd == "help":
		print("Available commands:")
		print("\thelp: display this help")
		print("\tinfos: display server infos")
		print("\tclients: display connected clients")
		print("\tsubject <client id> <level> [subject name]: set the subject for a client. If no subject name is specified, a random one will be chosen")

	if cmd == "infos":
		print("Server infos:")
		print("\tPort: " + str(server.port))
		print("\tClients: " + str(len(clients)))
		print("\tLevels: " + str(len(subjects_module.subjects)))
		for level in subjects_module.subjects.keys():
			print("\t\tLevel " + str(level) + ": ", end="")
			for subject in subjects_module.subjects[level]:
				print(subject.name + " ", end="")
			print("")

	if cmd == "clients":
		if len(clients) == 0:
			print("No clients connected")
			return
		print("Connected clients:")
		for client in clients:
			print("\t- Client " + str(client.id) + " | Level " + str(client.level) + " | Subject " + client.subject.name + " | Tries " + str(client.tries))

def cli_routine(clients):
	while True:
		cmd = input()
		treat_command(cmd, clients)