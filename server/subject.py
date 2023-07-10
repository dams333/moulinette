class Subject:
	def __init__(self, name, subject):
		self.name = name
		self.subject = subject
		self.complete_file = "~/rendu/" + name + ".c"
		self.subject_file = "~/subject/" + name + ".txt"

	def to_dict(self):
		return {
			"name": self.name,
			"subject": self.subject,
			"complete_file": self.complete_file,
			"subject_file": self.subject_file
		}


def get_subject_for_level(level):
	return Subject("ft_putchar",
"""
Assignment name       : ft_putchar
Excepted files        : ft_putchar.c
Allowed functions     : write
------------------------------
Write a function that displays on the stdout the character passed as a parameter.

It will be prototyped as follows :
void    ft_putchar(char c);
""")