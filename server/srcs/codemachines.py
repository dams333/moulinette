import requests

codemachines_hostname = []
next_codemachine = 0

def register_codemachine(hostname):
		global codemachines_hostname

		codemachines_hostname.append(hostname)

def use_codemachine(client, data):
		global codemachines_hostname
		global next_codemachine

		client.is_grading = True

		codemachine_host = codemachines_hostname[next_codemachine]
		next_codemachine = (next_codemachine + 1) % len(codemachines_hostname)
		
		payload = {
			"content": {
				"files": data,
				"function": client.current_subject.function,
				"main": client.current_subject.main,
			},
			"flags": client.current_subject.compiler_flags,
			"functions": client.current_subject.authorized_functions,
			"run": {
				"subject": client.current_subject.name,
				"client": client.id,
				"try": client.current_try
			}
		}

		print("Grading client {} on subject {} (try {}) on codemachine {}".format(client.id, client.current_subject.name, client.current_try, codemachine_host))
		res = requests.post(codemachine_host, json=payload).json()
		print("{} for client {} on subject {} (try {}): {}".format("Success" if res['success'] else "Failure", client.id, client.current_subject.name, client.current_try, res['reason']))

		client.is_grading = False
		return res