#script.sh host port
if [ "$#" -ne 2 ]; then
		echo "Usage: $0 host port"
		exit 1
fi

docker run -it --network="host" -v ~/rendu:/tmp/rendu -v ~/subject:/tmp/subject -v ~/traces:/tmp/traces dhubleur/moulinette:client-latest $1 $2