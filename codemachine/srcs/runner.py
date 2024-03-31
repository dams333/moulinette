from TraceUtil import TraceUtil
import subprocess
import os
import clang.cindex
from clang.cindex import Config

Config.set_library_path('/usr/lib/llvm-11/lib')
Config.set_library_file('/usr/lib/llvm-11/lib/libclang-11.so.1')

def finish(traceUtil, result, reason):
		traceUtil.end(reason)
		return {
			'success': result,
			'reason': reason,
			'trace': traceUtil.get()
		}

def run_codemachine(work_folder, execution_folder, data):
		traceUtil = TraceUtil()

		traceUtil.add('Grading ' + data['run']['subject'] + ' for client ' + str(data['run']['client']) + ', try ' + str(data['run']['try']))
		src_filename = data['run']['subject'] + '.c'

		traceUtil.add_section('Files')
		traceUtil.add('Collected files:')
		found_exercise = False
		for file in data['content']['files']:
			traceUtil.add('\t- ' + file)
			if file == src_filename:
				found_exercise = True
		if not found_exercise:
			return finish(traceUtil, False, 'no file named ' + src_filename)
		
		code_file = work_folder + '/' + src_filename
		with open(code_file, 'w') as f:
			f.write(data['content']['files'][src_filename])
			f.close()
		
		traceUtil.add_section('Norminette')
		norm_cmd = "norminette -R CheckForbiddenSourceHeader " + code_file
		traceUtil.add_command(norm_cmd)
		norm_subprocess = subprocess.Popen(norm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		norm_subprocess.wait()
		norm_result = norm_subprocess.stdout.read().decode()
		traceUtil.add(norm_result)

		if "Error!" in norm_result:
			return finish(traceUtil, False, 'norminette failed')
		
		main_file = work_folder + '/main.c'
		with open(main_file, 'w') as f:
			f.write(data['content']['main'])
			f.close()
		function_file = work_folder + '/function.c'
		with open(function_file, 'w') as f:
			f.write(data['content']['function'])
			f.close()

		traceUtil.add_section('Functions')
		if len(data['functions']) == 0:
			traceUtil.add('No unauthorized functions, skipping')
		else:
			code = open(code_file, "r").read()
			index = clang.cindex.Index.create()
			tu = index.parse('tmp.c', args=['-std=c11'], unsaved_files=[('tmp.c', code)])
			function_definitions = []
			for node in tu.cursor.walk_preorder():
				if node.kind == clang.cindex.CursorKind.FUNCTION_DECL and node.location.file.name == "tmp.c":
					function_name = node.mangled_name
					if function_name[0] == '_':
						function_name = function_name[1:]
					function_definitions.append(function_name)

			functions_used = []
			for node in tu.cursor.walk_preorder():
				if node.kind == clang.cindex.CursorKind.CALL_EXPR and node.location.file.name == "tmp.c":
					function_name = node.displayname
					if function_name not in function_definitions:
						functions_used.append(function_name)

			if len(functions_used) == 0:
				traceUtil.add('No unauthorized functions used')
			else:
				traceUtil.add("Functions used:")
				for function in functions_used:
					traceUtil.add("\t- " + function)
				for function in functions_used:
					if function not in data['functions']:
						return finish(traceUtil, False, 'unauthorized function used: ' + function)

		traceUtil.add_section('Compilation')
		our_exe = work_folder + '/our_exe'
		compile_subject_cmd = "gcc " + data['flags'] + " -o " + our_exe + " " + main_file + " " + function_file
		traceUtil.add_command(compile_subject_cmd)
		compile_subject_subprocess = subprocess.Popen(compile_subject_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		compile_subject_subprocess.wait()
		compile_subject_result = compile_subject_subprocess.stdout.read().decode()
		traceUtil.add(compile_subject_result)

		user_exe = execution_folder + '/user_exe'
		compile_user_cmd = "gcc " + data['flags'] + " -o " + user_exe + " " + main_file + " " + code_file
		traceUtil.add_command(compile_user_cmd)
		compile_user_subprocess = subprocess.Popen(compile_user_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		compile_exit_code = compile_user_subprocess.wait()
		compile_user_result = compile_user_subprocess.stdout.read().decode()
		traceUtil.add(compile_user_result)
		if (compile_exit_code != 0):
			return finish(traceUtil, False, 'compilation failed')

		traceUtil.add_section('Execution')
		our_result_file = work_folder + '/our_result'
		our_execution_cmd = our_exe
		traceUtil.add_command(our_execution_cmd + ' > ' + our_result_file)
		execution_subprocess = subprocess.Popen(our_execution_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		execution_subprocess.wait()
		with open(our_result_file, 'w') as f:
			f.write(execution_subprocess.stdout.read().decode())
			f.close()
		
		os.system('chown -R codemachine:codemachine ' + execution_folder)

		user_execution_cmd = user_exe
		user_result_file = work_folder + '/user_result'
		traceUtil.add_command(user_execution_cmd + ' > ' + user_result_file)
		try:
			execution_subprocess = subprocess.Popen('runuser -l codemachine -c ' + user_execution_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			execution_exit_code = execution_subprocess.wait(timeout=5)
			with open(user_result_file, 'w') as f:
				f.write(execution_subprocess.stdout.read().decode())
				f.close()
			if execution_exit_code != 0:
				traceUtil.add('Execution ended with exit code ' + str(execution_exit_code))
				return finish(traceUtil, False, 'execution failed')
		except subprocess.TimeoutExpired:
			return finish(traceUtil, False, 'timed out')
		
		traceUtil.add_section('Output')
		diff_cmd = 'diff -U 3 ' + user_result_file + ' ' + our_result_file
		traceUtil.add_command(diff_cmd)
		diff_subprocess = subprocess.Popen(diff_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		diff_exit_code = diff_subprocess.wait()
		diff_result = diff_subprocess.stdout.read().decode()
		traceUtil.add(diff_result)
		if diff_exit_code != 0:
			return finish(traceUtil, False, 'not the same output')

		return finish(traceUtil, True, 'all tests passed')