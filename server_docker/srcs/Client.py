from Subject import get_subject_for_level, is_subject_for_level

g_id = 0
def get_id():
		global g_id
		g_id += 1
		return g_id - 1

clients = []

def add_client(addr):
		global clients

		client = Client(addr)
		clients.append(client)
		return client

def get_client(addr):
		global clients

		for client in clients:
				if client.addr == addr:
						return client
		return None

class Client:		
		def __init__(self, addr):
				self.addr = addr
				self.id = get_id()
				self.current_subject = None
				self.current_level = 0
				self.current_try = 1
				self.is_grading = False

		def get_current_subject(self):
				if self.current_subject is None:
						if is_subject_for_level(self.current_level):
								self.current_subject = get_subject_for_level(self.current_level)
								print("Choosed subject " + self.current_subject.name + " for client " + str(self.id) + "(level " + str(self.current_level) + ", try " + str(self.current_try) + ")")
				return self.current_subject