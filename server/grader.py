import os

def get_trace_file(subject, client):
	if not os.path.exists("traces"):
		os.mkdir("traces")
	if not os.path.exists("traces/" + str(client.id)):
		os.mkdir("traces/" + str(client.id))
	if not os.path.exists("traces/" + str(client.id) + "/" + subject.name):
		os.mkdir("traces/" + str(client.id) + "/" + subject.name)
	return open("traces/" + str(client.id) + "/" + subject.name + "/" + str(client.tries) + ".txt", "w")

def grade(subject, files, client):
	file = get_trace_file(subject, client)

	file.write("Grading " + subject.name + " for client " + str(client.id) + ", try " + str(client.tries) + "\n")

	file.write("\n================= Files =================\n")
	file.write("Collected files:\n")
	found_exercise = False
	for f in files:
		file.write("\t- " + f + "\n")
		if f == subject.name + ".c":
			found_exercise = True

	if not found_exercise:
		file.write("Error: no file named " + subject.name + ".c\n")
		file.close()
		client.send("grade_result", {"grade": false, "message": "No trace available"})
	
	file.write("\n================= Compilation =================\n")

	file.close()
