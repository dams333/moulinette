import sys
import requests
import os

server_url = ''
current_subject = None

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

def print_subject():
	global current_subject

	print("=============================================================")
	print("Your current assignment is: " + style.GREEN + current_subject['name'] + style.RESET)
	print("Your subject is located at: " + style.GREEN + current_subject['subject_file'] + style.RESET)
	print("You must submit your work in the rendu folder (" + style.RED + current_subject['complete_file'] + style.RESET + ")")
	print("=============================================================")
	print("You can now work on your assignment, when you are ready to be graded, type '" + style.GREEN + "grademe" + style.RESET + "' and press enter")

def get_subjet():
	global server_url
	global current_subject

	res = requests.get(server_url + '/subject')
	if not res.ok:
		print('Failed to get subject')
		sys.exit(1)

	data = res.json()
	if data['status'] != 'success':
		print('Failed to get subject')
		sys.exit(1)

	current_subject = data['subject']
	subject_file = current_subject['subject_file'].replace('~/subject/', '/tmp/subject/')
	with open(subject_file, "w") as file:
		file.write(current_subject["subject"])

def login():
	global server_url

	res = requests.post(server_url + '/join')
	if not res.ok:
		print('Failed to connect to server')
		sys.exit(1)
	
	data = res.json()
	id = data['id']
	if data['status'] == 'welcome':
		print('Server confirmed that you are a new client, id: ' + str(id))
	elif data['status'] == 'welcome back':
		print('Server confirmed that you are a returning client, id: ' + str(id))
	else:
		print('Unknown status')
		sys.exit(1)

def save_trace(try_count, subject_name, trace_content):
	trace_file = '/tmp/traces/' + str(try_count) + '_' + subject_name + '.txt'
	with open(trace_file, 'w') as file:
		file.write(trace_content)
	trace_file_name = trace_file.replace('/tmp/traces/', '~/traces/')
	print("Trace saved (" + style.CYAN + trace_file_name + style.RESET + ")")

def grade():
	global server_url
	global current_subject

	files = {}
	for file in os.listdir('/tmp/rendu'):
		if file.endswith(".c"):
			files[file] = open('/tmp/rendu/' + file, 'r').read()
	print("You work has been sent to the server, waiting for the grade...")
	res = requests.post(server_url + '/submit', json=files)
	if not res.ok:
		print('Failed to submit work')
		sys.exit(1)
	data = res.json()
	if data['status'] == 'error':
		print('Failed to submit work: ' + data['message'])
	else:
		graded = True if data['status'] == 'success' else False
		trace_content = data['trace']
		try_count = data['try_count']

		if graded:
			print(style.GREEN + ">>>>>>>>>> SUCCESS <<<<<<<<<<" + style.RESET)
			if trace_content is None:
				print("No trace available for this exercice")
			else:
				save_trace(try_count, current_subject['name'], trace_content)
			print("You passed the exercice! Please wait for the next one...")
			get_subjet()
			print_subject()

		else:
			print(style.RED + ">>>>>>>>>> FAILURE <<<<<<<<<<" + style.RESET)
			if trace_content is None:
				print("No trace available for this exercice")
			else:
				save_trace(try_count, current_subject['name'], trace_content)
			print("You failed the exercice! Please try again...")
			print_subject()

def treat_command(cmd):
	if cmd == 'help':
		print("The following commands are available:")
		print(style.GREEN + "\thelp" + style.RESET + ": display this help")
		print(style.GREEN + "\tgrademe" + style.RESET + ": send your work to the server for grading")
	elif cmd == 'grademe':
		confirm = input(style.RED + "Do you want to be graded?" + style.RESET + " (y/n) ").lower()
		if confirm == 'y' or confirm == 'yes':
			grade()
		else:
			print("Cancelled grading request")
	else:
		print("Unknown command")

if __name__ == "__main__":
		if len(sys.argv) != 3:
			print("Usage: python client.py <server_ip> <server_port>")
			sys.exit(1)
		server_url = 'http://' + sys.argv[1] + ':' + sys.argv[2]
		login()
		get_subjet()
		print_subject()

		while True:
			try:
				cmd = input(style.YELLOW + "Moulinette's shell" + style.RESET + "> ")
				treat_command(cmd)
			except KeyboardInterrupt or EOFError:
				print("\rExiting...")
				sys.exit(0)