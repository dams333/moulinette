class Subject:
	def __init__(self, folder_path):
		self.name = folder_path.split("/")[-1]
		self.complete_file = "~/rendu/" + self.name + ".c"
		self.subject_file = "~/subject/" + self.name + ".txt"
		self.subject = open(folder_path + "/subject.txt", "r").read()
		self.main = open(folder_path + "/main.c", "r").read()
		self.function = open(folder_path + "/function.c", "r").read()

	def to_dict(self):
		return {
			"name": self.name,
			"subject": self.subject,
			"complete_file": self.complete_file,
			"subject_file": self.subject_file
		}


def get_subject_for_level(level):
	return Subject("subjects/level00/ft_putchar")