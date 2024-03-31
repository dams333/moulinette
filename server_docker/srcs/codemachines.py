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
		
		res = requests.post(codemachine_host, json=data)
		print(res.json())