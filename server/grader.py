import os
import subprocess
import time

def get_trace_file(subject, client):
	if not os.path.exists("traces"):
		os.mkdir("traces")
	if not os.path.exists("traces/" + str(client.id)):
		os.mkdir("traces/" + str(client.id))
	if not os.path.exists("traces/" + str(client.id) + "/" + subject.name):
		os.mkdir("traces/" + str(client.id) + "/" + subject.name)
	return open("traces/" + str(client.id) + "/" + subject.name + "/" + str(client.tries) + ".txt", "w")

def create_file(subject, client, content):
	if not os.path.exists("codes"):
		os.mkdir("codes")
	if not os.path.exists("codes/" + str(client.id)):
		os.mkdir("codes/" + str(client.id))
	if not os.path.exists("codes/" + str(client.id) + "/" + subject.name):
		os.mkdir("codes/" + str(client.id) + "/" + subject.name)
	dirname = "codes/" + str(client.id) + "/" + subject.name
	os.chdir(dirname)
	if not os.path.exists("main.c"):
		file = open("main.c", "w")
		file.write(subject.main)
		file.close()
	if not os.path.exists("function.c"):
		file = open("function.c", "w")
		file.write(subject.function)
		file.close()
	filename = str(client.tries) + '_' + subject.name + ".c"
	file = open(filename, "w")
	file.write(content)
	file.close()
	return filename

def get_trace_content(trace_name):
	trace_file = open(trace_name, "r")
	content = trace_file.read()
	trace_file.close()
	return content

def grade(subject, files, client):
	time.sleep(2)
	trace_file = get_trace_file(subject, client)

	trace_file.write("Grading " + subject.name + " for client " + str(client.id) + ", try " + str(client.tries) + "\n")

	trace_file.write("\n================= Files =================\n")
	trace_file.write("Collected files:\n")
	found_exercise = False
	for f in files:
		trace_file.write("\t- " + f + "\n")
		if f == subject.name + ".c":
			found_exercise = True

	if not found_exercise:
		trace_file.write("END OF GRADING: no file named " + subject.name + ".c\n")
		trace_file.close()
		trace = get_trace_content(trace_file.name)
		client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (no file named " + subject.name + ".c)")
		return 0
	
	save_current_dir = os.getcwd()

	src_file = create_file(subject, client, files[subject.name + ".c"])
	trace_file.write("\n================= Norm =================\n")
	norm_cmd = "norminette -R CheckForbiddenSourceHeader " + src_file
	trace_file.write("> " + norm_cmd + "\n")
	norm_subprocess = subprocess.Popen(norm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	norm_subprocess.wait()
	norm_result = norm_subprocess.stdout.read().decode()
	trace_file.write(norm_result)
	trace_file.write("\n")

	if "Error!" in norm_result:
		trace_file.write("END OF GRADING: norminette failed\n")
		trace_file.close()
		os.chdir(save_current_dir)
		trace = get_trace_content(trace_file.name)
		client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (norminette failed)")
		return 0

	trace_file.write("\n================= Compilation =================\n")
	compile_subject_cmd = subject.compiler + " " + subject.compiler_flags + " -o our_exe main.c function.c"
	trace_file.write("> " + compile_subject_cmd + "\n")
	compile_subject_subprocess = subprocess.Popen(compile_subject_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	compile_subject_subprocess.wait()
	compile_subject_result = compile_subject_subprocess.stdout.read().decode()
	trace_file.write(compile_subject_result)
	trace_file.write("\n")

	compile_user_cmd = subject.compiler + " " + subject.compiler_flags + " -o user_exe main.c " + src_file
	trace_file.write("> " + compile_user_cmd + "\n")
	compile_user_subprocess = subprocess.Popen(compile_user_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	compile_exit_code = compile_user_subprocess.wait()
	compile_user_result = compile_user_subprocess.stdout.read().decode()
	trace_file.write(compile_user_result)
	trace_file.write("\n")
	if (compile_exit_code != 0):
		trace_file.write("END OF GRADING: compilation failed\n")
		trace_file.close()
		os.chdir(save_current_dir)
		trace = get_trace_content(trace_file.name)
		client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (compilation failed)")
		return 0

	trace_file.write("\n================= Functions =================\n")
	compile_for_nm_cmd = subject.compiler + " " + subject.compiler_flags + " -c " + src_file + " -o nm_obj"
	trace_file.write("> " + compile_for_nm_cmd + "\n")
	compile_for_nm_subprocess = subprocess.Popen(compile_for_nm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	compile_for_nm_subprocess.wait()
	compile_for_nm_result = compile_for_nm_subprocess.stdout.read().decode()
	trace_file.write(compile_for_nm_result)
	trace_file.write("\n")

	nm_cmd = "nm -u nm_obj"
	trace_file.write("> " + nm_cmd + "\n")
	nm_subprocess = subprocess.Popen(nm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	nm_subprocess.wait()
	nm_result = nm_subprocess.stdout.read().decode()
	trace_file.write(nm_result)
	trace_file.write("\n")

	for symbol in nm_result.split("\n"):
		if symbol == "":
			continue
		if not symbol in subject.authorized_functions:
			trace_file.write("END OF GRADING: unauthorized function " + symbol + "\n")
			trace_file.close()
			os.chdir(save_current_dir)
			trace = get_trace_content(trace_file.name)
			client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
			print("Client " + str(client.id) + " failed exercise " + subject.name + " (unauthorized function " + symbol + ")")
			return 0

	trace_file.write("\n================= Execution =================\n")
	execute_subject_cmd = "./our_exe > our_output"
	execute_subject_subprocess = subprocess.Popen(execute_subject_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	execute_subject_subprocess.wait()

	execute_user_cmd = "./user_exe > user_output"
	try:
		execute_user_subprocess = subprocess.Popen(execute_user_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		execute_exit_code = execute_user_subprocess.wait(timeout=5)
		if (execute_exit_code != 0):
			trace_file.write("> " + execute_user_cmd + "\n")
			execute_user_result = execute_user_subprocess.stdout.read().decode()
			trace_file.write(execute_user_result)
			trace_file.write("\n")
			trace_file.close()
			os.chdir(save_current_dir)
			trace = get_trace_content(trace_file.name)
			client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
			print("Client " + str(client.id) + " failed exercise " + subject.name + " (execution failed)")
			return 0
	except subprocess.TimeoutExpired:
		trace_file.write("> " + execute_user_cmd + "\n")
		trace_file.write("Program took too long to execute\n\n")
		trace_file.write("END OF GRADING: timed out\n")
		trace_file.close()
		os.chdir(save_current_dir)
		trace = get_trace_content(trace_file.name)
		client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (timed out)")
		return 0

	diff_cmd = "diff -U 3 user_output our_output"
	trace_file.write("> " + diff_cmd + "\n")
	diff_subprocess = subprocess.Popen(diff_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	diff_exit_code = diff_subprocess.wait()
	diff_result = diff_subprocess.stdout.read().decode()
	trace_file.write(diff_result)
	trace_file.write("\n")
	if (diff_exit_code != 0):
		trace_file.write("END OF GRADING: not the same output\n")
		trace_file.close()
		os.chdir(save_current_dir)
		trace = get_trace_content(trace_file.name)
		client.send("grade_result", {"grade": False, "trace": trace if subject.send_trace else None, "try": client.tries})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (not the same output)")
		return 0

	trace_file.write("END OF GRADING: All tests passed\n")
	trace_file.close()
	os.chdir(save_current_dir)
	trace = get_trace_content(trace_file.name)
	client.send("grade_result", {"grade": True, "trace": trace if subject.send_trace else None, "try": client.tries})
	print("Client " + str(client.id) + " passed exercise " + subject.name)

	client.tries = 0
	client.level += 1;
	client.send_subject(False)

	return 1