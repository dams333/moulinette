#script.sh network_name
if [ "$#" -ne 1 ]; then
		echo "Usage: $0 network_name"
		exit 1
fi

docker network create --driver bridge $1