class TraceUtil:
		def __init__(self):
				self.trace = ''

		def add(self, content):
				self.trace += content + '\n'

		def add_section(self, section):
				self.trace += '\n================= ' + section + ' =================\n'

		def end(self, reason):
				self.trace += '\nEND OF GRADING: ' + reason + '\n'

		def get(self):
				return self.trace