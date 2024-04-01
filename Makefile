NETWORK_SCRIPT = scripts/create_codemachine_network.sh
CODEMACHINE_SCRIPT = scripts/spawn_c_codemachine.sh
SERVER_SCRIPT = scripts/spawn_server.sh

CODEMACHINE_NETWORK = codemachine_network
CODEMACHINE_HOST = moulinette_codemachine
SERVER_PORT = 3333
SUBJECTS_FOLDER = /tmp/subjects

all: server

network:
	@sh $(NETWORK_SCRIPT) $(CODEMACHINE_NETWORK)
	@echo "Network $(CODEMACHINE_NETWORK) created"

codemachine: network
	@sh $(CODEMACHINE_SCRIPT) $(CODEMACHINE_HOST) $(CODEMACHINE_NETWORK)
	@echo "Codemachine $(CODEMACHINE_HOST) created"

server: codemachine
	@sh $(SERVER_SCRIPT) $(SERVER_PORT) $(CODEMACHINE_NETWORK) $(SUBJECTS_FOLDER) $(CODEMACHINE_HOST)
	@echo "Server container created"

stop:
	@echo "Stopping codemachine..."
	@docker stop $(CODEMACHINE_HOST)
	@echo "Stopped codemachine"
	@echo "Stopping server..."
	@docker stop moulinette_server
	@echo "Stopped server"

clean: stop
	@echo "Removing network..."
	@docker network rm $(CODEMACHINE_NETWORK)
	@echo "Network removed"
	@echo "Removing codemachine..."
	@docker rm $(CODEMACHINE_HOST)
	@echo "Codemachine removed"
	@echo "Removing server..."
	@docker rm moulinette_server
	@echo "Server removed"

.PHONY: all network codemachine server stop clean