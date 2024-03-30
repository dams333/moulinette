from flask import Flask, request, jsonify
import uuid
import os
import runner

app = Flask('codemachine')

@app.route('/', methods=['POST'])
def start_process():
		data = request.json

		# verify format of data
		if 'content' not in data:
			return jsonify({'error': 'content is required'}), 400
		if 'files' not in data['content']:
			return jsonify({'error': 'content.files is required'}), 400
		if 'function' not in data['content']:
			return jsonify({'error': 'content.function is required'}), 400
		if 'main' not in data['content']:
			return jsonify({'error': 'content.main is required'}), 400
		if 'flags' not in data:
			return jsonify({'error': 'flags is required'}), 400
		if 'functions' not in data:
			return jsonify({'error': 'functions is required'}), 400
		if 'run' not in data:
			return jsonify({'error': 'run is required'}), 400
		if 'subject' not in data['run']:
			return jsonify({'error': 'run.subject is required'}), 400
		if 'client' not in data['run']:
			return jsonify({'error': 'run.client is required'}), 400
		if 'try' not in data['run']:
			return jsonify({'error': 'run.try is required'}), 400
		
		process_id = str(uuid.uuid4())
		work_folder = '/usr/runner/' + process_id
		os.mkdir(work_folder)
		execution_folder = '/codemachine/' + process_id
		os.mkdir(execution_folder)

		return jsonify(runner.run_codemachine(work_folder, execution_folder, data))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000)