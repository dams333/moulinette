import os

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
	filename = str(client.tries) + '_' + subject.name + ".c"
	file = open(filename, "w")
	file.write(content)
	file.close()
	return filename

def grade(subject, files, client):
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
		client.send("grade_result", {"grade": False})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (no file named " + subject.name + ".c)")
	
	save_current_dir = os.getcwd()

	src_file = create_file(subject, client, files[subject.name + ".c"])
	trace_file.write("\n================= Norm =================\n")
	norm_cmd = "norminette -R CheckForbiddenSourceHeader " + src_file
	trace_file.write("> " + norm_cmd + "\n")
	norm_result = os.popen(norm_cmd).read()
	trace_file.write(norm_result)

	if "Error!" in norm_result:
		trace_file.write("END OF GRADING: norminette failed\n")
		trace_file.close()
		os.chdir(save_current_dir)
		client.send("grade_result", {"grade": False})
		print("Client " + str(client.id) + " failed exercise " + subject.name + " (norminette failed)")
		return

	trace_file.write("\n================= Compilation =================\n")

	trace_file.close()
	os.chdir(save_current_dir)
