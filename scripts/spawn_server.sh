if [ "$#" -lt 4 ]; then
		echo "Usage: $0 port codemachine_network_name subjects_folder moulinette_host1, [moulinette_host2, ...]"
		exit 1
fi

hosts_string=""
for host in "${@:4}"
do
	hosts_string="$hosts_string http://$host:3000 "
done
docker run -p $1:4242 -d --name moulinette_server --network $2 -v $3:/tmp/subjects dhubleur/moulinette:server-latest $hosts_string