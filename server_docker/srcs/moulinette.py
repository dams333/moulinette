from flask import Flask, request, jsonify
from Client import add_client, get_client
from Subject import load_subjects
from codemachines import register_codemachine, use_codemachine
import sys

app = Flask('moulinette')

@app.route('/join', methods=['POST'])
def join():
	client = request.client
	if client is None:
		client = add_client(request.remote_addr)
		return jsonify({'status': 'welcome', 'id': client.id})
	return jsonify({'status': 'welcome back', 'id': client.id})

@app.route('/subject', methods=['GET'])
def subject():
	if request.client is None:
		return jsonify({'status': 'error', 'message': 'You must join first'})
	subject = request.client.get_current_subject()
	if subject is None:
		return jsonify({'status': 'error', 'message': 'No subject available for your level'})
	return jsonify({'status': 'success', 'subject': subject.to_dict()})

@app.route('/submit', methods=['POST'])
def submit():
	if request.client is None:
		return jsonify({'status': 'error', 'message': 'You must join first'})
	
	if request.client.is_grading:
		return jsonify({'status': 'error', 'message': 'You are already grading a subject'})
	
	if request.client.current_subject is None:
		return jsonify({'status': 'error', 'message': 'You must get a subject first'})
	
	res = use_codemachine(request.client, request.json)

	if res['success']:
		request.client.current_try = 1
		request.client.current_level += 1
		request.client.current_subject = None
	else:
		request.client.current_try += 1

	data = {
		'status': 'success' if res['success'] else 'failure',
		'trace': res['trace'] if request.client.current_subject.send_trace else None
	}
	return jsonify(data)

@app.before_request
def before_request():
		ip = request.remote_addr
		request.client = get_client(ip)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: python3 moulinette.py codemachine1 [codemachine2, ...] ")
		exit(1)
	for i in range(1, len(sys.argv)):
		register_codemachine(sys.argv[i])
	load_subjects()
	app.run(host='0.0.0.0', port=4242, debug=True)