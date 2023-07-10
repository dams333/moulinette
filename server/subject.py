class Subject:
	def __init__(self, name, subject, complete_file):
		self.name = name
		self.subject = subject
		self.complete_file = complete_file

	def to_dict(self):
		return {
			"name": self.name,
			"subject": self.subject,
			"complete_file": self.complete_file
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
""",
	"rendu/ft_putchar.c")