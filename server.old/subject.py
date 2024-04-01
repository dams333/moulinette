import os
import random
import json

subjects = {}

def get_subjects():
	global subjects
	return subjects

class Subject:
	def __init__(self, folder_path):
		self.name = folder_path.split("/")[-1]
		self.complete_file = "~/rendu/" + self.name + ".c"
		self.subject_file = "~/subject/" + self.name + ".txt"
		self.subject = open(folder_path + "/subject.txt", "r").read()
		self.main = open(folder_path + "/main.c", "r").read()
		self.function = open(folder_path + "/function.c", "r").read()
		self.send_trace = False
		self.authorized_functions = []
		self.compiler = "gcc"
		self.compiler_flags = "-Wall -Wextra -Werror"
		if os.path.exists(folder_path + "/config.json"):
			config = json.load(open(folder_path + "/config.json", "r"))
			if "send_trace" in config.keys():
				self.send_trace = config["send_trace"]
			if "authorized_functions" in config.keys():
				self.authorized_functions = config["authorized_functions"]
			if "compiler" in config.keys():
				self.compiler = config["compiler"]
			if "compiler_flags" in config.keys():
				self.compiler_flags = config["compiler_flags"]

	def to_dict(self):
		return {
			"name": self.name,
			"subject": self.subject,
			"complete_file": self.complete_file,
			"subject_file": self.subject_file
		}

def load_subjects():
	global subjects
	print("Loading subjects...")

	if os.path.isdir("subjects") == False:
		print("Error: no subjects folder found")
		exit(1)
	
	count = 0
	for folder in os.listdir("subjects"):
		if folder.startswith("level"):
			level = int(folder.split("level")[1])
			subjects[level] = []
			for subject in os.listdir("subjects/" + folder):
				subjects[level].append(Subject("subjects/" + folder + "/" + subject))
				print("Loaded subject " + subject + " for level " + str(level))
				count += 1
	subjects = dict(sorted(subjects.items()))

	print("Loaded " + str(count) + " subjects")

def is_subject_for_level(level):
	global subjects

	return level in subjects.keys()

def get_subject_for_level(level):
	global subjects

	return subjects[level][random.randint(0, len(subjects[level]) - 1)]

def get_subject_by_name(level, name):
	global subjects

	for subject in subjects[level]:
		if subject.name == name:
			return subject
	return None