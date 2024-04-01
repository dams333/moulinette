# script.sh container_name codemachine_network_name
if [ "$#" -ne 2 ]; then
		echo "Usage: $0 container_name codemachine_network_name"
		exit 1
fi

docker run -d --name $1 --network $2 dhubleur/moulinette:c_codemachine-latest