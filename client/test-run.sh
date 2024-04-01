docker build -t moulinette_client:latest .
docker run -it --network="host" -v ~/rendu:/tmp/rendu -v ~/subject:/tmp/subject -v ~/traces:/tmp/traces moulinette_client:latest localhost 4242