docker build -t moulinette:latest .
docker run -p 4242:4242 -v /tmp/subjects:/tmp/subjects --network codemachine moulinette:latest http://codemachine:3000