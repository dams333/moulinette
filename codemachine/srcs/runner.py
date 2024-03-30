from TraceUtil import TraceUtil

def finish(traceUtil, result, reason):
		traceUtil.end(reason)
		return {
			'success': result,
			'trace': traceUtil.get()
		}

def run_codemachine(work_folder, execution_folder, data):
		traceUtil = TraceUtil()

		traceUtil.add('Grading ' + data['run']['subject'] + ' for client ' + str(data['run']['client']) + ', try ' + str(data['run']['try']))

		traceUtil.add_section('Files')
		traceUtil.add('Collected files:')
		found_exercise = False
		for file in data['content']['files']:
			traceUtil.add('\t- ' + file)
			if file == data['run']['subject'] + '.c':
				found_exercise = True
		if not found_exercise:
			return finish(traceUtil, False, 'no file named ' + data['run']['subject'] + '.c')

		return finish(traceUtil, True, 'success')